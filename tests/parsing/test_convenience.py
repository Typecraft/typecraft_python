import pytest

from typecraft_python.core.models import Phrase
from typecraft_python.parsing.convenience import detokenize, parse_slash_separated_phrase, parse_bar_separated_phrase, \
    words_to_phrase, word_pos_tuples_to_phrase


class TestDetokenize(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_detokenize_phrase_without_punctuation(self):
        tokens = [
            'This', 'is', 'cool'
        ]
        assert detokenize(tokens) == 'This is cool'

    def test_detokenize_phrase_with_end_punctuation(self):
        tokens = [
            'This', 'is', 'cool', '.'
        ]
        assert detokenize(tokens) == 'This is cool.'

    def test_detokenize_phrase_with_multiple_punctuation(self):
        tokens = [
            'And', 'so', 'he', 'said', ':', 'Give', 'me', 'milk', '!'
        ]
        assert detokenize(tokens) == 'And so he said: Give me milk!'

    def test_detokenize_with_single_quotation(self):
        tokens = [
            'I', '\'ve', 'sort', 'of', 'fallen', 'out', '.'
        ]
        assert detokenize(tokens) == 'I\'ve sort of fallen out.'


class TestParseSlashSeparated(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_parse_slash_separated(self):
        unparsed = "The/at Hartsfield/np home/nr is/bez at/in 637/cd E./np Pelham/np Rd./nn-tl Aj/nn ./."
        parsed = parse_slash_separated_phrase(unparsed)

        assert isinstance(parsed, Phrase)
        assert len(parsed.words) == 11

        assert parsed.phrase == "The Hartsfield home is at 637 E. Pelham Rd. Aj."

        assert parsed.words[0].word == "The"
        assert parsed.words[0].pos == "at"

        assert parsed.words[1].word == "Hartsfield"
        assert parsed.words[1].pos == "np"

        assert parsed.words[2].word == "home"
        assert parsed.words[2].pos == "nr"

        assert parsed.words[3].word == "is"
        assert parsed.words[3].pos == "bez"

        assert parsed.words[4].word == "at"
        assert parsed.words[4].pos == "in"

        assert parsed.words[5].word == "637"
        assert parsed.words[5].pos == "cd"

        assert parsed.words[6].word == "E."
        assert parsed.words[6].pos == "np"

        assert parsed.words[7].word == "Pelham"
        assert parsed.words[7].pos == "np"

        assert parsed.words[8].word == "Rd."
        assert parsed.words[8].pos == "nn-tl"

        assert parsed.words[9].word == "Aj"
        assert parsed.words[9].pos == "nn"

        assert parsed.words[10].word == "."
        assert parsed.words[10].pos == "."

    def test_should_only_split_at_last_occurrence(self):
        unparsed = "and/or/cc"
        parsed = parse_slash_separated_phrase(unparsed)
        assert len(parsed.words) == 1

        assert parsed.words[0].word == "and/or"
        assert parsed.words[0].pos == "cc"


class TestParseBarSeparated(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_parse_bar_separated(self):
        unparsed = "Aber|KON es|PPER gibt|VVFIN keine|PIAT Garantie|NN .|$."
        parsed = parse_bar_separated_phrase(unparsed)

        assert isinstance(parsed, Phrase)
        assert len(parsed.words) == 6
        assert parsed.phrase == "Aber es gibt keine Garantie."

        assert parsed.words[0].word == "Aber"
        assert parsed.words[0].pos == "KON"

        assert parsed.words[1].word == "es"
        assert parsed.words[1].pos == "PPER"

        assert parsed.words[2].word == "gibt"
        assert parsed.words[2].pos == "VVFIN"

        assert parsed.words[3].word == "keine"
        assert parsed.words[3].pos == "PIAT"

        assert parsed.words[4].word == "Garantie"
        assert parsed.words[4].pos == "NN"

        assert parsed.words[5].word == "."
        assert parsed.words[5].pos == "$."


class TestWordToPhrase(object):

    def test_words_to_phrase(self):
        words = ['Hello', 'this', 'is', 'nice', '.']
        phrase = words_to_phrase(words)
        assert isinstance(phrase, Phrase)
        assert len(phrase.words) == 5
        assert phrase.words[0].word == "Hello"
        assert phrase.words[1].word == "this"
        assert phrase.words[2].word == "is"
        assert phrase.words[3].word == "nice"
        assert phrase.words[4].word == "."

    def test_words_to_phrase_bad_input(self):
        with pytest.raises(Exception):
            words_to_phrase(2)

        class Something():
            pass
        with pytest.raises(Exception):
            words_to_phrase(Something())
        with pytest.raises(Exception):
            words_to_phrase(Something)


class TestWordPosTuplesToPhrase(object):
    def test_words_pos_tuples_to_phrase(self):
        word_pos_tuples = [
            ('Hello', 'pos1'),
            ('this', 'pos2'),
            ('is', 'pos3'),
            ('nice', 'pos4'),
            ('.', 'pos5'),
        ]
        phrase = word_pos_tuples_to_phrase(word_pos_tuples)
        assert isinstance(phrase, Phrase)
        assert len(phrase.words) == 5
        assert phrase.words[0].word == "Hello"
        assert phrase.words[1].word == "this"
        assert phrase.words[2].word == "is"
        assert phrase.words[3].word == "nice"
        assert phrase.words[4].word == "."

        assert phrase.words[0].pos == "pos1"
        assert phrase.words[1].pos == "pos2"
        assert phrase.words[2].pos == "pos3"
        assert phrase.words[3].pos == "pos4"
        assert phrase.words[4].pos == "pos5"

    def test_words_pos_tuples_to_phrase_bad_input(self):
        with pytest.raises(Exception):
            word_pos_tuples_to_phrase(2)

        class Something():
            pass
        with pytest.raises(Exception):
            word_pos_tuples_to_phrase(Something())
        with pytest.raises(Exception):
            word_pos_tuples_to_phrase(Something)

