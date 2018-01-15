import sys

import six

from typecraft_python.models import Phrase, Word

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
