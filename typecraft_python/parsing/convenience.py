"""
This file contains multiple convenience methods for different forms of parsing.
"""
import six
import string
from typecraft_python.core.models import Phrase, Word, Morpheme


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


def words_to_phrase(words):
    """
    Takes a list/iterable of tokens/words, and returns an instantiated phrase from the
    words.

    :param words: A list or iterable of words
    :return: A Phrase object instantiated from the words.
    """
    if not hasattr(words, '__iter__'):
        raise Exception("Invalid argument to words_to_phrase, expected iterable")

    return Phrase(detokenize(words), words=[Word(word) for word in words])


def word_pos_tuples_to_phrase(word_pos_iterable):
    """
    Take a list of (word, pos) tuples, and returns an instantiated phrase from them.

    :param word_pos_iterable: An iterable of (word, pos) tuples.
    :return: A Phrase object instantiated from the words and pos tags.
    """
    if not hasattr(word_pos_iterable, '__iter__'):
        raise Exception("Invalid argument to words_to_phrase, expected iterable")

    return Phrase(
        detokenize([word for word,_ in word_pos_iterable]),
        words=[Word(word, pos=pos) for word, pos in word_pos_iterable]
    )


def word_pos_lemma_tuples_to_phrase(word_pos_lemma_iterable):
    if not hasattr(word_pos_lemma_iterable, '__iter__'):
        raise Exception("Invalid argument to words_to_phrase, expected iterable")

    return Phrase(
        detokenize([word for word, _, _ in word_pos_lemma_iterable]),
        words=[Word(word, pos=pos, morphemes=[Morpheme(morpheme=word, baseform=lemma)]) for word, pos, lemma
               in word_pos_lemma_iterable]
    )


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
    slash_tokenized = list(map(lambda x: x.rsplit("/", 1), space_tokenized))

    return word_pos_tuples_to_phrase(slash_tokenized)


def parse_bar_separated_phrase(bar_separated_phrase):
    """
    Parses a vertical bar separated phrase into a Phrase object.

    The expect format is that used by e.g. the LCC:

        Aber|KON es|PPER gibt|VVFIN keine|PIAT Garantie|NN

    :param bar_separated_phrase:
    :return:
    """
    assert isinstance(bar_separated_phrase, six.string_types)

    space_tokenized = bar_separated_phrase.split(" ")
    bar_tokenized = list(map(lambda x: x.rsplit("|", 1), space_tokenized))

    return word_pos_tuples_to_phrase(bar_tokenized)


