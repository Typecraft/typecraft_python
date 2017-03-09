import xml.etree.ElementTree as ElementTree
from xml.dom import minidom

from typecraft_python.exceptions.parsing import TypecraftParseException
from typecraft_python.models import Text, Phrase, Word, Morpheme
from typecraft_python.globals import *

"""
The typecraft namespace
"""
ns = '{http://typecraft.org/typecraft}'

"""
Tag-strings that define what the expected element-tags of the xml-files are.
"""
tag_typecraft = ns + 'typecraft'
tag_text = ns + 'text'
tag_phrase = ns + 'phrase'
tag_word = ns + 'word'
tag_morpheme = ns + 'morpheme'

XML_HEADER = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"


def prettify(string):
    """
    Helper method.

    Return a pretty-printed XML string for the Element.
    """
    reparsed = minidom.parseString(string)
    return reparsed.toprettyxml(indent="\t")


class _ParserHelper:
    """
    This class contains static methods that assist us in the parsing process, and
    de-clutters the primary Parser-class.
    """

    def __init__(self):
        """
        Empty constructor
        """
        pass


    @staticmethod
    def check_text_for_conformity(text_root):
        """
        Checks if a text-element is conformant to the Typecraft-XML model.

        It must have the following attributes:
            None

        It must have the following elements:
            title
            titleTranslation
            extraMetadata


        :param text_root:
        :return:
        """

        if not STRICT_MODE:
            return

        if text_root.find(ns + 'title') is None:
            raise TypecraftParseException("Element  " + tag_text + " is missing field 'title'")

        if text_root.find(ns + 'titleTranslation') is None:
            raise TypecraftParseException("Element " + tag_text + " is missing field 'titleTranslation'")

        if text_root.find(ns + 'extraMetadata') is None:
            raise TypecraftParseException("Element " + tag_text + " is missing field 'extraMetadata'")

        return

    @staticmethod
    def check_phrase_for_conformity(phrase_root):
        """
        Checks if a phrase-element is conformant to the Typecraft XML-model

        It must have the following attributes:
            None

        It must have the following elements:
            original

        :param phrase_root:
        :return:
        """
        if not STRICT_MODE:
            return

        if phrase_root.find(ns + 'original') is None:
            raise TypecraftParseException("Element " + tag_phrase + " is missing field 'original'")

        return

    @staticmethod
    def check_word_for_conformity(word_root):
        """
        Checks if a word-element is conformant to the Typecraft XML-model

        It must have the following attributes:
            text

        It must have the following elements:
            None

        :param word_root:
        :return:
        """

        if not STRICT_MODE:
            return

        if word_root.attrib.get('text') is None:
            raise TypecraftParseException("Element " + tag_word + " is missing attribute 'text'")

        return

    @staticmethod
    def check_morpheme_for_conformity(morpheme_root):
        """
        Checks if a morpheme-element is conformant to the Typecraft XML-model.

        It must have the following attributes:
            None

        It must have the following elements:
            None

        :param morpheme_root:
        :return:
        """
        return True

    @staticmethod
    def add_obligatory_fields_to_text(text, text_root):
        """
        Adds the obligatory fields of a text-object. It assumes they exist.

        If they do not, undefined behaviour may occur

        :param text: A Text-object
        :param text_root: An ElementTree representing a text-object
        :return:
        """

        title = text_root.find(ns + 'title').text
        title_translation = text_root.find(ns + 'titleTranslation').text

        text.title = title
        text.title_translation = title_translation

        metadata_tree = text_root.find(ns + 'extraMetadata')

        for metadata in metadata_tree.findall(ns + 'metadata'):
            key = metadata.attrib['name']
            value = metadata.text

            text.add_metadata(key, value)

        return

    @staticmethod
    def check_and_add_optional_fields_to_text(text, text_root):
        """
        Adds any expected optional fields (that are not phrases) of a text-element to a text-object.

        :param text: A Text-object
        :param text_root: An ElementTree representing a text-object
        :return:
        """

        body = text_root.find(ns + 'body')
        id = text_root.attrib.get('id')
        lang = text_root.attrib.get('lang')

        if body is not None:
            text.body = body

        if id is not None:
            text.id = id

        if lang is not None:
            text.language = lang

        return

    @staticmethod
    def add_phrase_children_to_text(text, text_root):
        """
        Discovers the phrase-children of a text-element, parses them into Phrase-objects
        and adds them to a text.

        :param text: A Text-object
        :param text_root: A Text-ElementTree
        :return:
        """

        for phrase in text_root.findall(ns + 'phrase'):
            text.add_phrase(Parser.convert_etree_to_phrase(phrase))

        return

    @staticmethod
    def add_obligatory_fields_to_phrase(phrase, phrase_root):
        """
        Adds the obligatory fields of a phrase-object. The method assumes they exist.

        :param phrase: A Phrase-object
        :param phrase_root: An ElementTree representation of a Phrase
        :return:
        """
        original = phrase_root.find(ns + 'original').text

        phrase.phrase = original if original is not None else ""
        return

    @staticmethod
    def check_and_add_optional_fields_to_phrase(phrase, phrase_root):
        """
        Adds any expected optional fields (that are not words) to the Phrase-object.

        :param phrase:
        :param phrase_root:
        :return:
        """

        id = phrase_root.attrib.get('id')
        validity = phrase_root.attrib.get('valid')
        translation_tree = phrase_root.find(ns + 'translation')
        globaltags_tree = phrase_root.find(ns + 'globaltags')

        if id is not None:
            phrase.id = id

        if validity is not None:
            phrase.validity = validity

        if translation_tree is not None:
            phrase.translation = translation_tree.text if translation_tree.text is not None else ""

        if globaltags_tree is not None:
            phrase.global_tags = {'id': globaltags_tree.attrib.get('id'),
                                  'tagset': globaltags_tree.attrib.get('tagset')}

        return

    @staticmethod
    def add_word_children_to_phrase(phrase, phrase_root):
        """
        Discovers, parses and adds a phrases word-children.
        :param phrase:
        :param phrase_root:
        :return:
        """

        for word in phrase_root.findall(ns + 'word'):
            phrase.add_word(Parser.convert_etree_to_word(word))

        return

    @staticmethod
    def add_obligatory_fields_to_word(word, word_root):
        """
        Adds the obligatory fields of a word. Assumes they exist.

        :param word:
        :param word_root:
        :return:
        """

        word_text = word_root.attrib.get('text')
        word.word = word_text if word_text is not None else ""

        return

    @staticmethod
    def check_and_add_optional_fields_to_word(word, word_root):
        """
        Adds any expected optional field to the text.

        :param word:
        :param word_root:
        :return:
        """

        id = word_root.attrib.get('id')
        head = word_root.attrib.get('head')
        pos_tree = word_root.find(ns + 'pos')

        if id is not None:
            word.id = id

        if head is not None:
            word.head = (head == 'true')

        if pos_tree is not None:
            word.pos = pos_tree.text if pos_tree.text is not None else ""

        return

    @staticmethod
    def add_morpheme_children_to_word(word, word_root):
        """
        Discovers, parses and adds the morpheme children of a word.

        :param word:
        :param word_root:
        :return:
        """
        for morpheme in word_root.findall(ns + 'morpheme'):
            word.add_morpheme(Parser.convert_etree_to_morpheme(morpheme))

        return

    @staticmethod
    def add_obligatory_fields_to_morpheme(morpheme, morpheme_root):
        """
        Adds the obligatory fields of a morpheme. Assumes them to exist.

        Does nothing.

        :param morpheme:
        :param morpheme_root:
        :return:
        """
        return

    @staticmethod
    def check_and_add_optional_fields_to_morpheme(morpheme, morpheme_root):
        """
        Adds any expected optional fields of a morpheme-object.

        :param morpheme:
        :param morpheme_root:
        :return:
        """

        morpheme_text = morpheme_root.attrib.get('text')
        baseform = morpheme_root.attrib.get('baseform')
        meaning = morpheme_root.attrib.get('meaning')

        gloss_tree = morpheme_root.findall(ns + 'gloss')

        if baseform is not None:
            morpheme.baseform = baseform

        if meaning is not None:
            morpheme.meaning = meaning

        if morpheme_text is not None:
            morpheme.morpheme = morpheme_text

        for gloss in gloss_tree:
            morpheme.add_gloss(gloss.text)

        return


class Parser:
    """
    This class contains functionality for parsing Typecraft-xml files
    into Text objects.
    """

    def __init__(self):
        """
        Do nothing
        """
        pass

    @staticmethod
    def convert_etree_to_texts(root):
        """
        Takes an ElementTree instance representing a Typecraft-xml document and returns
        a list of texts from it.
        :return:
        """

        if not(tag_typecraft in root.tag):
            raise TypecraftParseException("Expect root of document to be element "
                                          + tag_typecraft +
                                          ", and not " + root.tag)

        texts = []

        for child in root:
            texts.append(Parser.convert_etree_to_text(child))

        return texts

    @staticmethod
    def convert_etree_to_text(text_root):
        if not(tag_text in text_root.tag):
            raise TypecraftParseException("Expect root of text to be element "
                                          + tag_text +
                                          ", and not " + text_root.tag)

        text = Text()

        # Will throw an exception if the text is not valid
        _ParserHelper.check_text_for_conformity(text_root)

        _ParserHelper.add_obligatory_fields_to_text(text, text_root)
        _ParserHelper.check_and_add_optional_fields_to_text(text, text_root)
        _ParserHelper.add_phrase_children_to_text(text, text_root)

        return text

    @staticmethod
    def convert_etree_to_phrase(phrase_root):
        if not(tag_phrase in phrase_root.tag):
            raise TypecraftParseException("Expect root of document to be element "
                                          + tag_phrase +
                                          ", and not " + phrase_root.tag)

        phrase = Phrase()

        # Will throw an exception if the phrase is not valid
        _ParserHelper.check_phrase_for_conformity(phrase_root)

        _ParserHelper.add_obligatory_fields_to_phrase(phrase, phrase_root)
        _ParserHelper.check_and_add_optional_fields_to_phrase(phrase, phrase_root)
        _ParserHelper.add_word_children_to_phrase(phrase, phrase_root)

        return phrase

    @staticmethod
    def convert_etree_to_word(word_root):
        if not(tag_word in word_root.tag):
            raise TypecraftParseException("Expect root of word to be element "
                                          + tag_word +
                                          ", and not " + word_root.tag)

        word = Word()

        # Will throw an exception if the word is not valid
        _ParserHelper.check_word_for_conformity(word_root)

        _ParserHelper.add_obligatory_fields_to_word(word, word_root)
        _ParserHelper.check_and_add_optional_fields_to_word(word, word_root)
        _ParserHelper.add_morpheme_children_to_word(word, word_root)

        return word

    @staticmethod
    def convert_etree_to_morpheme(morpheme_root):
        if not(tag_morpheme in morpheme_root.tag):
            raise TypecraftParseException("Expect root of morpheme to be element "
                                          + tag_morpheme +
                                          ", and not " + morpheme_root.tag)
        morpheme = Morpheme()

        # Will throw an exception if the word is not valid
        _ParserHelper.check_morpheme_for_conformity(morpheme_root)

        _ParserHelper.add_obligatory_fields_to_morpheme(morpheme, morpheme_root)
        _ParserHelper.check_and_add_optional_fields_to_morpheme(morpheme, morpheme_root)

        return morpheme

    @staticmethod
    def parse(string):
        """
        Will parse a Typecraft-xml string into a list of Text objects.

        :param string:
        :return:
        """
        return Parser.convert_etree_to_texts(ElementTree.fromstring(string))

    @staticmethod
    def parse_file(file_path):
        """
        Will parse a Typecraft-xml file into a list of Text objects.

        Will read the entire contents of the file into memory, and then call parse.
        :param file_path:
        :return:
        """
        tree = ElementTree.parse(file_path)
        return Parser.convert_etree_to_texts(tree.getroot())

    @staticmethod
    def convert_texts_to_etree(texts):
        root = ElementTree.Element("typecraft")
        root.set('xmlns', ns[1:-1])   # Strip brackets
        root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        root.set('xsi:schemaLocation', 'https://typecraft.org/typecraft.xsd')

        for text in texts:
            Parser.convert_text_to_etree(root, text)

        return root

    @staticmethod
    def convert_text_to_etree(root, text):
        assert isinstance(text, Text)

        text_el = ElementTree.SubElement(root, "text", {'lang': text.language})

        ElementTree.SubElement(text_el, 'title').text = text.title
        ElementTree.SubElement(text_el, 'titleTranslation').text = text.title_translation
        ElementTree.SubElement(text_el, 'body').text = text.rich_text

        for phrase in text:
            Parser.convert_phrase_to_etree(text_el, phrase)

    @staticmethod
    def convert_phrase_to_etree(root, phrase):
        assert isinstance(phrase, Phrase)

        phrase_el = ElementTree.SubElement(root, 'phrase', {'valid': 'UNKNOWN'})

        ElementTree.SubElement(phrase_el, 'original').text = phrase.phrase
        ElementTree.SubElement(phrase_el, 'translation').text = phrase.free_translation
        ElementTree.SubElement(phrase_el, 'translation2').text = phrase.free_translation2
        ElementTree.SubElement(phrase_el, 'globaltags', {'id': '1', 'tagset': 'Default'})
        ElementTree.SubElement(phrase_el, 'comment').text = phrase.comment

        for word in phrase:
            Parser.convert_word_to_etree(phrase_el, word)

    @staticmethod
    def convert_word_to_etree(root, word):
        assert isinstance(word, Word)

        word_el = ElementTree.SubElement(root, 'word', {'text': word.word, 'head': 'false'})

        ElementTree.SubElement(word_el, 'pos').text = word.pos

        for morpheme in word:
            Parser.convert_morpheme_to_etree(word_el, morpheme)

    @staticmethod
    def convert_morpheme_to_etree(root, morpheme):
        assert isinstance(morpheme, Morpheme)

        morpheme_el = ElementTree.SubElement(root, 'morpheme', {
            'text': morpheme.morpheme,
            'baseform': morpheme.baseform,
            'meaning': morpheme.meaning
        })

        for gloss in morpheme.glosses:
            ElementTree.SubElement(morpheme_el, 'gloss').text = gloss

    @staticmethod
    def write_to_file(file_name, texts):
        """
        Writes a text to a file
        :param texts:
        :param file_name:
        :return:
        """

        root = Parser.convert_texts_to_etree(texts)

        tree = ElementTree.ElementTree(root)
        tree.write(file_name, encoding="UTF-8")

    @staticmethod
    def write(texts):
        """
        Returns a string-xml-representation of a text
        :return:
        """
        return ElementTree.tostring(Parser.convert_texts_to_etree(texts), encoding="UTF-8")
