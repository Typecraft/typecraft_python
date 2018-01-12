import sys

import six

from typecraft_python.models import Phrase, Word

# try:
import nltk
# except ImportError:
#    nltk = None
#    sys.stderr.write("Unable to load NLTK, are you sure it is installed?")


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
