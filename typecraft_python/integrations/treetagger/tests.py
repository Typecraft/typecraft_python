from __future__ import unicode_literals
import pytest
from treetaggerwrapper import TreeTaggerError
from treetaggerwrapper import TreeTagger as _TreeTagger

from typecraft_python.parsing.convenience import words_to_phrase
from typecraft_python.models import Text, Word
from typecraft_python.integrations.treetagger import TreeTagger

try:
    _TreeTagger(TAGLANG='en')
    treetagger_enabled = True
except TreeTaggerError:
    treetagger_enabled = False


@pytest.mark.skipif(not treetagger_enabled, reason="Treetagger is not enabled")
class TestTreeTagger(object):
    def test_tag_raw(self):
        raw_english_text = u"This is a short sentence."
        tagger = TreeTagger()
        phrase = tagger.tag_raw(raw_english_text, language='en')[0]

        assert phrase[0].word == "This"
        assert phrase[1].word == "is"
        assert phrase[2].word == "a"
        assert phrase[3].word == "short"
        assert phrase[4].word == "sentence"
        assert phrase[5].word == "."

        assert phrase[0].pos is not None
        assert phrase[1].pos is not None
        assert phrase[2].pos is not None
        assert phrase[3].pos is not None
        assert phrase[4].pos is not None
        assert phrase[5].pos is not None

        assert phrase[0].pos != ""
        assert phrase[1].pos != ""
        assert phrase[2].pos != ""
        assert phrase[3].pos != ""
        assert phrase[4].pos != ""
        assert phrase[5].pos != ""

    def test_tag_raw_non_english(self):
        raw_text = u"Ich bin sehr schnell. Wo bist du?"
        tagger = TreeTagger()
        phrases = tagger.tag_raw(raw_text, language='de')
        assert len(phrases) == 2

        phrase_1 = phrases[0]
        phrase_2 = phrases[1]

        assert phrase_1[0].word == 'Ich'
        assert phrase_1[1].word == 'bin'
        assert phrase_1[2].word == 'sehr'
        assert phrase_1[3].word == 'schnell'
        assert phrase_1[4].word == '.'

        assert phrase_1[0].pos != ''
        assert phrase_1[1].pos != ''
        assert phrase_1[2].pos != ''
        assert phrase_1[3].pos != ''
        assert phrase_1[4].pos != ''

        assert phrase_2[0].word == 'Wo'
        assert phrase_2[1].word == 'bist'
        assert phrase_2[2].word == 'du'
        assert phrase_2[3].word == '?'

        assert phrase_2[0].pos != ''
        assert phrase_2[1].pos != ''
        assert phrase_2[2].pos != ''
        assert phrase_2[3].pos != ''

    def test_tag_raw_words(self):
        words = [u"This", u"is", u"a", u"short", u"sentence", u"."]
        tagger = TreeTagger()
        phrase = tagger.tag_raw_words(words)

        assert phrase[0].word == "This"
        assert phrase[1].word == "is"
        assert phrase[2].word == "a"
        assert phrase[3].word == "short"
        assert phrase[4].word == "sentence"
        assert phrase[5].word == "."

        assert phrase[0].pos is not None
        assert phrase[1].pos is not None
        assert phrase[2].pos is not None
        assert phrase[3].pos is not None
        assert phrase[4].pos is not None
        assert phrase[5].pos is not None

        assert phrase[0].pos != ""
        assert phrase[1].pos != ""
        assert phrase[2].pos != ""
        assert phrase[3].pos != ""
        assert phrase[4].pos != ""
        assert phrase[5].pos != ""

    def test_tag_raw__multiple_sentences__is_tokenized(self):
        raw = "This is a sentence. This is another sentence. How about this one, hmm?"
        tagger = TreeTagger()
        phrases = tagger.tag_raw(raw)
        assert len(phrases) == 3
        assert phrases[0].phrase == "This is a sentence."
        assert phrases[1].phrase == "This is another sentence."
        assert phrases[2].phrase == "How about this one, hmm?"

        assert len(phrases[0].words) == 5
        assert len(phrases[1].words) == 5
        assert len(phrases[2].words) == 7

    def test_tag_text(self):
        text = Text()
        words_1 = ["My", "first", "sentence", "."]
        words_2 = ["Let", "'s", "write", "another", "one", ",", "or", "what", "?"]

        phrase_1 = words_to_phrase(words_1)
        phrase_2 = words_to_phrase(words_2)

        text.add_phrases([phrase_1, phrase_2])

        tagger = TreeTagger()
        tagger.tag_text(text)

        for phrase in text:
            for word in phrase.words:
                assert word.pos is not None
                assert word.pos is not ""

    def test_tag_phrase(self):
        words = ["Let", "'s", "write", "another", "one", ",", "or", "what", "?"]
        phrase = words_to_phrase(words)

        tagger = TreeTagger()
        tagger.tag_phrase(phrase)

        for word in phrase.words:
            assert word.pos is not None
            assert word.pos is not ""

    def test_tag_words(self):
        words = ["Let", "'s", "write", "another", "one", ",", "or", "what", "?"]
        words = [Word(word) for word in words]

        tagger = TreeTagger()
        tagger.tag_words(words)

        for word in words:
            assert word.pos is not None
            assert word.pos is not ""

    def test_tag_word(self):
        word = Word('hello')
        tagger = TreeTagger()
        tagger.tag_word(word)
