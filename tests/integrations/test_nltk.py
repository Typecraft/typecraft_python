import pytest
from typecraft_python.integrations.nltk_integration import tokenize_phrase, pos_tag_phrase, \
    raw_phrase_to_tokenized_phrase, find_named_entities_for_phrase, raw_text_to_phrases, raw_text_to_tokenized_phrases
from typecraft_python.models import Phrase

# Ensure base modules is downloaded
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')


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


class TestNamedEntities(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_sentence_without_named_entities_adds_nothing(self):
        phrase = raw_phrase_to_tokenized_phrase("This has no named entities.")
        find_named_entities_for_phrase(phrase)

        assert 'Named entities' not in phrase.comment

    def test_sentence_with_named_entity_binary(self):
        phrase = raw_phrase_to_tokenized_phrase("Mike is a named entity")
        find_named_entities_for_phrase(phrase, binary=True)

        assert 'Named entities' in phrase.comment
        assert 'NE: Mike' in phrase.comment

    def test_sentence_with_named_entity_non_binary(self):
        phrase = raw_phrase_to_tokenized_phrase("Mike is a named entity")
        find_named_entities_for_phrase(phrase)
        assert 'Named entities' in phrase.comment
        assert 'PERSON: Mike' in phrase.comment

    def test_sentence_with_multiple_entities(self):
        phrase = raw_phrase_to_tokenized_phrase("Mike went travelling to Australia.")
        find_named_entities_for_phrase(phrase, binary=True)
        assert 'Named entities' in phrase.comment
        assert 'NE: Mike' in phrase.comment
        assert 'NE: Australia' in phrase.comment


class TestSentTokenize(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_raw_text_to_phrases(self):
        text = """
            This text contains two sentences. They are both very nice indeed.
        """
        phrases = raw_text_to_phrases(text)
        assert len(phrases) == 2
        assert isinstance(phrases[0], Phrase)
        assert isinstance(phrases[1], Phrase)
        assert len(phrases[0].words) == 0
        assert len(phrases[1].words) == 0

    def test_raw_text_to_tokenized_phrases(self):
        text = """
            This text contains two sentences. They are both very nice indeed.
        """
        phrases = raw_text_to_tokenized_phrases(text)
        assert len(phrases) == 2
        assert isinstance(phrases[0], Phrase)
        assert isinstance(phrases[1], Phrase)
        assert len(phrases[0].words) == 6
        assert len(phrases[1].words) == 7
