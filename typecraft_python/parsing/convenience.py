"""
This file contains multiple convenience methods for different forms of parsing.
"""
import six
import string
from typecraft_python.models import Phrase, Word


def detokenize(tokens):
    """
    Detokenizes a list of tokens to a full phrase.

    For instance, given the arguments ['This', 'is', 'cool', '.'], the
    method returns "This is cool."

    This is a very simple algorithm, which may not cover all cases.
    For more sophisticated usage, the MosesDetokenizer from nltk should
    be used.

    Taken from: https://stackoverflow.com/questions/21948019/python-untokenize-a-sentence

    :param tokens: A list of tokens
    :return: A string with the untokenized phrase.
    """
    return "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()


def parse_slash_separated_phrase(slash_separated_phrase):
    """
    Parses a slash separated phrase into a Phrase object.

    The expected format is that used in e.g. the Brown corpus:

    "The/at Hartsfield/np home/nr is/bez at/in 637/cd E./np Pelham/np Rd./nn-tl Aj/nn ./."

    :param slash_separated_phrase:
    :return:
    """
    assert isinstance(slash_separated_phrase, six.string_types)

    space_tokenized = slash_separated_phrase.split(" ")
    slash_tokenized = map(lambda x: x.split("/"), space_tokenized)
    # Unpack arguments to zip, which will return an iterator with two elements

    word_objs = []
    words = []
    for word, pos in slash_tokenized:
        word_obj = Word(word)
        word_obj.pos = pos
        word_objs.append(word_obj)
        words.append(word)

    return Phrase(detokenize(words), words=[word_objs])

