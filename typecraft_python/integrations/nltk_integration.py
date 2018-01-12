import sys

from typecraft_python.models import Phrase, Word

# try:
import nltk
# except ImportError:
#    nltk = None
#    sys.stderr.write("Unable to load NLTK, are you sure it is installed?")


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

