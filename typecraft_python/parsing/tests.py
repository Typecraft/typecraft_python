# coding: utf-8
from typecraft_python.parsing.parallell import parse_continuous_parallel_text_to_tuples, parse_continuous_parallel_text_to_phrases


class TestParseContinuousParallelTextToTuples(object):

    def test__two_langs__return__tuples(self):
        raw_text = u"""This is the first sentence.
        Dette er den første setningen.
        This is the second sentence.
        Dette er den andre setningen."""
        tuples = list(parse_continuous_parallel_text_to_tuples(raw_text, 2))
        assert len(tuples) == 2

        assert tuples[0][0] == u"This is the first sentence."
        assert tuples[0][1] == u"Dette er den første setningen."

        assert tuples[1][0] == u"This is the second sentence."
        assert tuples[1][1] == u"Dette er den andre setningen."

    def test__empty_intermediary_lines__should_be_ignored(self):
        raw_text = u"""This is the first sentence.
        Dette er den første setningen.
        
        This is the second sentence.
        
        
        
        
        Dette er den andre setningen."""
        tuples = list(parse_continuous_parallel_text_to_tuples(raw_text, 2))
        assert len(tuples) == 2

        assert tuples[0][0] == u"This is the first sentence."
        assert tuples[0][1] == u"Dette er den første setningen."

        assert tuples[1][0] == u"This is the second sentence."
        assert tuples[1][1] == u"Dette er den andre setningen."

    def test_three_langs__should_return_tuples(self):
        raw_text = u"""Sentence1 in lang1.
        Sentence1 in lang2. 
        Sentence1 in lang3.
        Sentence2 in lang1.
        Sentence2 in lang2.
        Sentence2 in lang3."""
        tuples = list(parse_continuous_parallel_text_to_tuples(raw_text, 3))
        assert len(tuples) == 2

        assert tuples[0][0] == u"Sentence1 in lang1."
        assert tuples[0][1] == u"Sentence1 in lang2."
        assert tuples[0][2] == u"Sentence1 in lang3."

        assert tuples[1][0] == u"Sentence2 in lang1."
        assert tuples[1][1] == u"Sentence2 in lang2."
        assert tuples[1][2] == u"Sentence2 in lang3."


class TestParseContinuousParallelTextToPhrases(object):
    def test__two_langs__should_return_phrase_and_translation(self):
        raw_text = u"""This is the first sentence.
        Dette er den første setningen.
        This is the second sentence.
        Dette er den andre setningen."""
        phrases = parse_continuous_parallel_text_to_phrases(raw_text, 2)
        assert len(phrases) == 2

        assert phrases[0].phrase == u"This is the first sentence."
        assert phrases[0].translation == u"Dette er den første setningen."

        assert phrases[1].phrase == u"This is the second sentence."
        assert phrases[1].translation == u"Dette er den andre setningen."

    def test__three_langs__should_set_both_translation_fields(self):
        raw_text = u"""Sentence1 in lang1.
        Sentence1 in lang2. 
        Sentence1 in lang3.
        Sentence2 in lang1.
        Sentence2 in lang2.
        Sentence2 in lang3."""
        phrases = list(parse_continuous_parallel_text_to_phrases(raw_text, 3))
        assert len(phrases) == 2

        assert phrases[0].phrase == u"Sentence1 in lang1."
        assert phrases[0].translation == u"Sentence1 in lang2."
        assert phrases[0].translation2 == u"Sentence1 in lang3."

        assert phrases[1].phrase == u"Sentence2 in lang1."
        assert phrases[1].translation == u"Sentence2 in lang2."
        assert phrases[1].translation2 == u"Sentence2 in lang3."

