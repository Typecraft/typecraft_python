# coding: utf-8
import os
from typecraft_python.parsing.parser import Parser
from typecraft_python.core.models import Text, Phrase, Word, GlobalTag, PhraseValidity, Morpheme

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


file_path = os.path.join(BASE_DIR, 'parsing/resources/xml_1_test.xml')
file_path_2 = os.path.join(BASE_DIR, 'parsing/resources/xml_2_test.xml')
small_tc_xml_string = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <typecraft xsi:schemaLocation="http://typecraft.org/typecraft.xsd" xmlns="http://typecraft.org/typecraft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <text id="3453" lang="kri">
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


def test_parse_file_does_not_crash():
    texts = Parser.parse_file(file_path)
    texts_2 = Parser.parse_file(file_path_2)

    assert texts is not None


def test_parse_string_does_not_crash():
    texts = Parser.parse(small_tc_xml_string)

    assert texts is not None


def test_parse_returns_text():
    texts = Parser.parse(small_tc_xml_string)

    assert isinstance(texts, list)
    assert len(texts) == 1

    text = texts[0]

    assert text is not None
    assert isinstance(text, Text)


def test_parse_preserves_metadata():
    texts = Parser.parse(small_tc_xml_string)

    assert isinstance(texts, list)
    assert len(texts) == 1

    text = texts[0]

    assert text.language == "kri"
    assert text.id == "3453"


def test_parse_preserves_phrases():
    texts = Parser.parse(small_tc_xml_string)

    assert isinstance(texts, list)
    assert len(texts) == 1

    text = texts[0]

    assert len(text.phrases) == 1

    phrase = text.phrases[0]

    assert phrase.phrase == "My name is Tormod."
    assert phrase.translation == "Jeg heter Tormod."


def test_parse_preserves_words():
    texts = Parser.parse(small_tc_xml_string)
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


def test_parse_preserves_morphemes():
    texts = Parser.parse(small_tc_xml_string)
    text = texts[0]
    phrase = text.phrases[0]
    word = phrase.words[0]

    assert len(word.morphemes) == 1

    morpheme = word.morphemes[0]

    assert morpheme is not None
    assert morpheme.morpheme == "My"
    assert len(morpheme.glosses) == 1
    assert morpheme.glosses[0] == "1PL"


def test_write_xml():
    texts = Parser.parse(small_tc_xml_string)

    written = Parser.write(texts).decode("utf-8")

    # We just test some containments

    assert "word head=\"false\" text=\"My\"" in written
    assert "<gloss>NEUT</gloss>" in written
    assert "<globaltags id=\"1\" tagset=\"Default\"/>"


def test_write_xml_to_file():
    texts = Parser.parse(small_tc_xml_string)

    path = os.path.join(BASE_DIR, "parsing/resources/out_test.xml")
    Parser.write_to_file(path, texts)

    assert os.path.isfile(path)
    os.remove(path)


def test_unicode():
    text = Text()
    phrase = Phrase()
    phrase.phrase = u"æ e i a æ å"
    word_1 = Word.from_text(u'æ')
    word_2 = Word.from_text(u'e')
    word_3 = Word.from_text(u'i')
    word_4 = Word.from_text(u'a')
    word_5 = Word.from_text(u'æ')
    word_6 = Word.from_text(u'å')

    phrase.add_words([word_1, word_2, word_3, word_4, word_5, word_6])
    text.add_phrase(phrase)

    string = Parser.write([text])

    assert u'æ e i a æ å' in string.decode("utf-8")


def test_write_phrase_with_global_tags():
    text = Text()
    phrase = Phrase()
    text.add_phrase(phrase)

    phrase.phrase = "test"
    phrase.add_global_tag(GlobalTag("informative", 1))
    phrase.add_global_tag(GlobalTag("timitive", 2))

    result = Parser.write([text])

    assert "<globaltag level=\"1\">informative</globaltag>" in result.decode("utf-8")
    assert "<globaltag level=\"2\">timitive</globaltag>" in result.decode("utf-8")


def test_load_phrase_with_global_tags():
    # Text with a phrase that has 8 globaltags under the default tagset
    # The global tags are:
    # <globaltag level="5">passive+causative+applicative</globaltag>
    # <globaltag level="7">EXPL+NP+NP+S</globaltag>
    # <globaltag level="3">resultative</globaltag>
    # <globaltag level="6">motion</globaltag>
    # <globaltag level="4">PP:manner</globaltag>
    # <globaltag level="2">timitive</globaltag>
    # <globaltag level="1">informative</globaltag>
    # <globaltag level="0">habitual</globaltag>
    file = '<typecraft xmlns="http://typecraft.org/typecraft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://typecraft.org/typecraft.xsd"><text id="3361" lang="und"><title>Hello this is a sentence.</title><titleTranslation/><extraMetadata setName="Default"/><body>Hello this is a sentence.<p></p></body><phrase id="421987" valid="VALID"><original>Hello this is a sentence.</original><translation/><translation2/><description/><globaltags id="1" tagset="Default"><globaltag level="5">passive+causative+applicative</globaltag><globaltag level="7">EXPL+NP+NP+S</globaltag><globaltag level="3">resultative</globaltag><globaltag level="6">motion</globaltag><globaltag level="4">PP:manner</globaltag><globaltag level="2">timitive</globaltag><globaltag level="1">informative</globaltag><globaltag level="0">habitual</globaltag></globaltags><word id="421987-1" text="Hello" head="false"><pos>INTRJCT</pos><morpheme text="hello" baseform="hello"/></word><word id="421987-2" text="this" head="false"><pos>PN</pos><morpheme text="this" baseform="this"/></word><word id="421987-3" text="is" head="false"><pos>COP</pos><morpheme text="is" baseform="be" meaning=""><gloss>PRES</gloss></morpheme></word><word id="421987-4" text="a" head="false"><pos>DET</pos><morpheme text="a" meaning="the"><gloss>DEF</gloss></morpheme></word><word id="421987-5" text="sentence" head="false"><pos>N</pos><morpheme text="sentence" baseform="sentence" meaning="sentence@obj:await"/></word><word id="421987-6" text="." head="false"><pos>PUN</pos><morpheme/></word></phrase></text></typecraft>'
    text = Parser.parse(file)[0]

    phrase = text.phrases[0]
    assert len(phrase.global_tags) == 8
    assert phrase.global_tags[0].level == "5"
    assert phrase.global_tags[0].name == "passive+causative+applicative"


def test_load_and_write_preserves_translations():
    file = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <typecraft xsi:schemaLocation="http://typecraft.org/typecraft.xsd" xmlns="http://typecraft.org/typecraft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <text id="3123" lang="aka">
            <title>Political discourse on Ghanaian radio stations (1)</title>
            <titleTranslation></titleTranslation>
            <extraMetadata />
            <body />
            <phrase id="1">
                <original>Dette er en test</original> 
                <translation>This is a test</translation>
                <translation2>C'est un test</translation2>
            </phrase>
        </text>
    </typecraft>
    """
    text = Parser.parse(file)[0]

    assert text.phrases[0].translation == "This is a test"
    dumped = Parser.write([text])
    assert 'This is a test' in dumped.decode()
    assert 'C\'est un test' in dumped.decode()


def test_write_and_load_produces_semantically_similar_results():
    # We create a text with more or less all levels of annotation
    # to ensure we get everything
    text = Text()
    text.language = "nob"
    text.metadata = {
        'Source link': 'test@example.com'
    }
    text.rich_text = '<phrase>hello</phrase>'

    phrase = Phrase()
    phrase.phrase = 'This is a nice phrase'
    phrase.validity = PhraseValidity.UNKNOWN
    phrase.add_global_tag(GlobalTag('SAS', 'NP+PP'))
    phrase.comment = 'Some text comment'
    phrase.translation = 'Dette er en fin frase'
    phrase.translation2 = 'Das ist ein schoner Satz'

    word = Word()
    word.word = 'This'
    word.pos = 'DET'

    morpheme = Morpheme()
    morpheme.morpheme = 'This'
    morpheme.add_gloss('DET')
    morpheme.baseform = 'This'
    morpheme.meaning = 'This'

    word.add_morpheme(morpheme)
    phrase.add_word(word)
    text.add_phrase(phrase)

    string_representation = Parser.write([text])
    new_texts = Parser.parse(string_representation)
    new_text = new_texts[0]
    assert new_text.language == "nob"
    assert new_text.metadata == {'Source link': 'test@example.com'}
    assert new_text.rich_text == '<phrase>hello</phrase>'
    assert len(new_text.phrases) == 1
    new_phrase = new_text.phrases[0]
    assert new_phrase.phrase == 'This is a nice phrase'
    assert new_phrase.validity == PhraseValidity.UNKNOWN
    assert new_phrase.comment == 'Some text comment'
    assert new_phrase.translation == 'Dette er en fin frase'
    assert new_phrase.translation2 == 'Das ist ein schoner Satz'
    assert len(new_phrase.words) == 1
    new_word = new_phrase.words[0]
    assert new_word.word == 'This'
    assert new_word.pos == 'DET'
    assert len(new_word.morphemes)
    new_morpheme = new_word.morphemes[0]
    assert new_morpheme.morpheme == 'This'
    assert new_morpheme.baseform == 'This'
    assert new_morpheme.meaning == 'This'
