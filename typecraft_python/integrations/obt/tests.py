# coding: utf-8
from __future__ import unicode_literals
import pytest

from typecraft_python.integrations.obt.tagger import ObtTagger, obt_available


@pytest.mark.skipif(not obt_available, reason="Obt is not enabled.")
class TestObtTagger(object):

    def test_parse_raw(self):
        raw_text = "Han kunne ikke løpe fortere enn meg, tror han (tror jeg). Dette er enda en setning. Jeg kjørte fort."
        tagger = ObtTagger()
        phrases = tagger.tag_raw(raw_text)

        assert len(phrases) == 3
        phrase_1 = phrases[0]
        phrase_2 = phrases[1]
        phrase_3 = phrases[2]

        assert phrase_1.phrase == "Han kunne ikke løpe fortere enn meg, tror han (tror jeg)."
        assert phrase_2.phrase == "Dette er enda en setning."
        assert phrase_3.phrase == "Jeg kjørte fort."

        assert len(phrase_1.words) == 15
        assert len(phrase_2.words) == 6
        assert len(phrase_3.words) == 4
