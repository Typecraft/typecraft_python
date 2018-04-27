import sys

try:
    import nltk
except ImportError:
    nltk = None
    sys.stderr.write("Unable to load NLTK, are you sure it is installed?")

from typecraft_python.models import Word, Morpheme

lemmatizer = nltk.WordNetLemmatizer()


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
