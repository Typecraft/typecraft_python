import pytest
from typecraft_python.integrations.nltk_integration import tokenize_phrase
from typecraft_python.models import Phrase


class TestTokenize(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_simple_phrase(self):
        phrase = Phrase("This is a nice phrase.")
        tokenize_phrase(phrase)

        assert len(phrase.words) == 6
        assert phrase.words[0].word == "This"
        assert phrase.words[1].word == "is"
        assert phrase.words[2].word == "a"
        assert phrase.words[3].word == "nice"
        assert phrase.words[4].word == "phrase"
        assert phrase.words[5].word == "."

    def test_bad_phrase_should_throw(self):
        phrase = "This is a nice phrase."
        with pytest.raises(Exception):
            tokenize_phrase(phrase)


class TestPosTag(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_pos_phrase(self):
        phrase = Phrase("This is a nice phrase.")
        tokenize_phrase(phrase)
        pos_tag_phrase(phrase)

        for word in phrase:
            assert word.pos != ''

    def test_pos_phrase_without_words_does_nothing(self):
        pass

