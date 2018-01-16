import sys

import six

from typecraft_python.models import Phrase, Word, Morpheme

try:
    import nltk
except ImportError:
    nltk = None
    sys.stderr.write("Unable to load NLTK, are you sure it is installed?")


LEGAL_NE_TAGS = [
    'ORGANIZATION',
    'PERSON',
    'LOCATION',
    'DATE',
    'TIME',
    'MONEY',
    'PERCENT',
    'FACILITY',
    'GPE',
    'NE'
]

lemmatizer = nltk.WordNetLemmatizer()


def raw_phrase_to_tokenized_phrase(raw_phrase):
    """
    Takes a raw string representation of a phrase, instantiates
    a new Phrase-model object instance from the phrase, tokenizes it,
    and returns.

    :param raw_phrase: The raw string phrase
    :return: A new Phrase object with the raw_phrase tokenized.
    """
    assert isinstance(raw_phrase, six.string_types)

    return tokenize_phrase(Phrase(raw_phrase))


def raw_text_to_phrases(raw_phrases, language='english'):
    """
    Takes a raw string representation of one or more phrases, then sentence-tokenizes them.
    Typecraft Phrase objects are then instantiated with each.

    The supported languages can be found at:
    https://github.com/nltk/nltk_data/blob/gh-pages/packages/tokenizers/punkt.xml

    :param raw_phrases: A text with one or more phrases in raw form.
    :param language: The language of the phrases.
    :return: A list of Phrase objects
    """
    tokenized = nltk.sent_tokenize(raw_phrases, language)
    return [Phrase(phrase) for phrase in tokenized]


def raw_text_to_tokenized_phrases(raw_phrases, language='english'):
    """
    Takes a raw string representation of one or more phrase, and sentence-tokenizes them.
    Typecraft Phrase objects are then instantiated for each, which is further more word-tokenized.

    The supported languages can be found at:
    https://github.com/nltk/nltk_data/blob/gh-pages/packages/tokenizers/punkt.xml
    :param raw_phrases: A text with one or more phrases in raw form.
    :param language: The language of the phrases.
    :return:
    """
    tokenized = nltk.sent_tokenize(raw_phrases, language)
    return [tokenize_phrase(Phrase(phrase)) for phrase in tokenized]


def tokenize_phrase(phrase):
    """
    Tokenizes a phrase using the nltk tokenizer.
    If the phrase already has sub-words, these will be overwritten.

    :param phrase: A Phrase to be tokenized.
    :return: The phrase. Note that the tokenization is done in-place.
             Thus this return value need not be used.
    """
    assert isinstance(phrase, Phrase)

    tokens = nltk.word_tokenize(phrase.phrase)
    phrase.add_words([Word(word=word) for word in tokens])
    return phrase


def pos_tag_phrase(phrase):
    """
    Pos tags a phrase.

    The tagger used is the default nltk tagger.

    :param phrase: A Phrase to be tagged.
    :return: The phrase. Note that tagging is done in-place.
             Thus this return value need not be used.
    """
    words = [word.word for word in phrase]
    tagged = nltk.pos_tag(words)

    for i in range(len(tagged)):
        phrase.words[i].pos = tagged[i][1]

    return phrase


def _parse_entity_tree_to_string(tree, use_tags=False):
    return_string = ""
    for child in tree:
        if isinstance(child, nltk.tree.Tree):
            return_string += _parse_entity_tree_to_string(child) + " "
        else:
            return_string += child[0] + " "
    return return_string


def _parse_entity_tree_for_named_entities(tree):
    parsed_entity_names = []

    if hasattr(tree, 'label') and tree.label() in LEGAL_NE_TAGS:
        parsed_entity_names.append((tree.label(), _parse_entity_tree_to_string(tree)))
    # We might recurse down to the string level, in which case we simply return
    # So we check if it is in fact a tree
    elif isinstance(tree, nltk.tree.Tree):
        for child in tree:
            parsed_entity_names.extend(_parse_entity_tree_for_named_entities(child))
    return parsed_entity_names


def find_named_entities_for_phrase(phrase, binary=False):
    """
    Finds all the named entities of a phrase, and adds them to the
    phrases comment.

    :param phrase: A Phrase.
    :param binary: Should the returned named entity tags be of binary type?
    :return: The Phrase. Note that the alteration is done in-place.
             Thus this return value need not be used.
    """
    words = [word.word for word in phrase]
    tagged = nltk.pos_tag(words)
    entities = nltk.chunk.ne_chunk(tagged, binary)
    parsed = _parse_entity_tree_for_named_entities(entities)

    if len(parsed) == 0:
        return phrase

    phrase.comment += "\nNamed entities:\n%s" % ("\n".join(
        [("%s: %s" % (ne[0], ne[1])) for ne in parsed]
    ))
    return phrase


def lemmatize_word(word):
    """
    Lemmatizes a word, and saves the lemma as the words citation form.
    If the word has no morphemes, a single morpheme is created.

    :param word: The Word to lemmatize
    :type word: Word
    :return: Returns the word.
    """
    assert isinstance(word, Word)

    lemma = lemmatizer.lemmatize(word.word.lower())
    if len(word.morphemes) > 0:
        word.morphemes[0].baseform = lemma
    else:
        morpheme = Morpheme(word.word)
        morpheme.baseform = lemma
        word.add_morpheme(morpheme)
    return word


def lemmatize_phrase(phrase):
    """
    Lemmatizes a phrase. Calls the method lemmatize_word for each word in the phrase.

    :param phrase: A Phrase object.
    :return: The phrase.
    """
    for word in phrase:
        lemmatize_word(word)
    return phrase

