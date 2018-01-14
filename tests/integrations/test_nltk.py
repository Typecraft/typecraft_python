import pytest
from typecraft_python.integrations.nltk_integration import tokenize_phrase, pos_tag_phrase, \
    raw_phrase_to_tokenized_phrase
from typecraft_python.models import Phrase

# Ensure base modules is downloaded
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


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

    def test_tokenize_raw_phrase(self):
        raw_phrase = "This is a nice phrase."
        phrase = raw_phrase_to_tokenized_phrase(raw_phrase)

        assert isinstance(phrase, Phrase)
        assert phrase.phrase == "This is a nice phrase."

        assert len(phrase.words) == 6
        assert phrase.words[0].word == "This"
        assert phrase.words[1].word == "is"
        assert phrase.words[2].word == "a"
        assert phrase.words[3].word == "nice"
        assert phrase.words[4].word == "phrase"
        assert phrase.words[5].word == "."


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

