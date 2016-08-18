import pytest
import os
from tc_xml_python.parsing.parser import Parser
from tc_xml_python.models import Text

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class TestParser(object):
    @classmethod
    def setup_class(cls):
        cls.file_path = os.path.join(BASE_DIR, 'tests/resources/xml_1_test.xml')
        cls.small_tc_xml_string = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <typecraft xsi:schemaLocation="http://typecraft.org/typecraft.xsd" xmlns="http://typecraft.org/typecraft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <text id="3453" lang="und">
            <title>My name is Tormod.</title>
            <titleTranslation></titleTranslation>
            <extraMetadata setName="Default"/>
            <body>My name is Tormod.&lt;p&gt;&lt;/p&gt;</body>
            <phrase id="449800" valid="VALID">
            <original>My name is Tormod.</original>
            <translation>Jeg heter Tormod.</translation>
            <translation2></translation2>
            <description></description>
            <globaltags id="1" tagset="Default"/>
            <word id="449800-1" text="My" head="true">
            <pos>PREP</pos>
            <morpheme text="My" baseform="My" meaning="My">
            <gloss>1PL</gloss>
            </morpheme>
            </word>
            <word id="449800-2" text="name" head="false">
            <pos>N</pos>
            <morpheme text="name" baseform="name" meaning="name"/>
            </word>
            <word id="449800-3" text="is" head="false">
            <pos>V</pos>
            <morpheme text="is" baseform="is" meaning=""/>
            </word>
            <word id="449800-4" text="Tormod." head="false">
            <pos>NMASC</pos>
            <morpheme text="Tormod." baseform="Tormod." meaning="Name of the object">
            <gloss>NEUT</gloss>
            </morpheme>
            </word>
            </phrase>
            </text>
            </typecraft>"""

    def test_parse_file_does_not_crash(self):
        texts = Parser.parse_file(self.file_path)

        assert texts is not None

    def test_parse_string_does_not_crash(self):
        texts = Parser.parse(self.small_tc_xml_string)

        assert texts is not None

    def test_parse_returns_text(self):
        texts = Parser.parse(self.small_tc_xml_string)

        assert isinstance(texts, list)
        assert len(texts) == 1

        text = texts[0]

        assert text is not None
        assert isinstance(text, Text)

    def test_parse_preserves_phrases(self):
        texts = Parser.parse(self.small_tc_xml_string)

        assert isinstance(texts, list)
        assert len(texts) == 1

        text = texts[0]

        assert len(text.phrases) == 1

        phrase = text.phrases[0]

        assert phrase.phrase == "My name is Tormod."
        assert phrase.translation == "Jeg heter Tormod."

    def test_parse_preserves_words(self):
        texts = Parser.parse(self.small_tc_xml_string)
        text = texts[0]
        phrase = text.phrases[0]

        assert len(phrase.words) == 4

        word1 = phrase.words[0]
        word2 = phrase.words[1]
        word3 = phrase.words[2]
        word4 = phrase.words[3]

        assert word1.word == "My"
        assert word2.word == "name"
        assert word3.word == "is"
        assert word4.word == "Tormod."

        assert word1.pos == "PREP"
        assert word2.pos == "N"
        assert word3.pos == "V"
        assert word4.pos == "NMASC"

        assert word1.head is True
        assert word2.head is False
        assert word3.head is False
        assert word4.head is False

    def test_parse_preserves_morphemes(self):
        texts = Parser.parse(self.small_tc_xml_string)
        text = texts[0]
        phrase = text.phrases[0]
        word = phrase.words[0]

        assert len(word.morphemes) == 1

        morpheme = word.morphemes[0]

        assert morpheme is not None
        assert morpheme.morpheme == "My"
        assert len(morpheme.glosses) == 1
        assert morpheme.glosses[0] == "1PL"
