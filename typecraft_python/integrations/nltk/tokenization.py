import sys

import six

try:
    import nltk
except ImportError:
    nltk = None
    sys.stderr.write("Unable to load NLTK, are you sure it is installed?")

from typecraft_python.models import Phrase, Word


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
