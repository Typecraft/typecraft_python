from typecraft_python.models import Phrase
from typecraft_python.parsing.convenience import detokenize, parse_slash_separated_phrase, parse_bar_separated_phrase


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
