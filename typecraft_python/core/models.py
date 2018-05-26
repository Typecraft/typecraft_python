"""
This file contains all models.
"""

import six
from enum import Enum
from yaml import dump

from typecraft_python.parsing.mappings import get_pos_conversions, get_gloss_conversions
from typecraft_python.core.interfaces import TypecraftModel


class Corpus(TypecraftModel):
    """
    The class representing a corpus files.

    This class represents the 1-1 mapping to and from the tc-xml files.
    """

    def __init__(self):
        self.texts = []

    def detokenize(self):
        return "\n".join([text.detoknize for text in self.texts])

    def map_tags(self, tagset='tc'):
        for text in self.texts:
            text.detoknize(tagset)

    def attributes(self):
        return {}

    def merge(self, other):
        assert isinstance(other, Corpus)

        self.texts.extend(other.texts)

    def to_dict(self):
        return {
            'texts': self.texts
        }

    def __str__(self):
        return "Corpus with %d texts" % (len(self.texts),)

    def __getitem__(self, item):
        return self.texts[item]

    def __iter__(self):
        return self.texts.__iter__()


class Text(TypecraftModel):
    """
    The class representing a text-object.

    A text is formally a collection of sentences with some extra metadata.
    """

    def __init__(
        self,
        title="",
        title_translation="",
        language="und",
        plain_text="",
        rich_text="",
        metadata=None,
        phrases=None
    ):
        """
        Default constructor
        """
        self.title = title
        self.title_translation = title_translation
        self.language = language  # Und is the default for the undefined language
        self.plain_text = plain_text
        self.rich_text = rich_text
        self.metadata = {}
        self.phrases = []

        if phrases and hasattr(phrases, '__iter__'):
            self.add_phrases(phrases)

        if metadata and isinstance(metadata, dict):
            self.metadata.update(metadata)

    def add_phrase(self, phrase):
        """
        Adds a phrase to the text-object

        :param phrase:
        :return:
        """
        if not (isinstance(phrase, Phrase)):
            raise Exception("Wrong argument to add_phrase. Expected Phrase instance")

        self.phrases.append(phrase)

    def add_phrases(self, phrases):
        """
        Adds an iterable of phrases to this text.

        :param phrases:
        :return:
        """
        for phrase in phrases:
            self.add_phrase(phrase)

    def add_metadata(self, key, value):
        """
        Adds a metadata key-value pair.

        :param key:
        :param value:
        :return:
        """

        if key is not None and value is not None:
            self.metadata[key] = value
        else:
            raise Exception("Wrong argument to add_metadata. Expected a key-value pair as argument one and two")

    def remove_phrase(self, phrase):
        """
        Removes a phrase from the text if it exists.

        :param phrase:
        :return:
        """
        self.phrases.remove(phrase)

    def remove_metadata(self, key):
        """
        Deletes a metadata key from the texts metadata dict if it exists.
        :param key:
        :return:
        """
        if key in self.metadata:
            del self.metadata[key]

    def clear_phrases(self):
        """
        Clears all phrases of the text.

        :return:
        """
        self.phrases = []

    def clear_metadata(self):
        """
        Clears all metadata of the text.

        :return:
        """
        self.metadata = {}

    def clear_tags(self):
        """
        Clears all tags in the text. Specifically, call clear_tags on all the phrases of the text
        :return:
        """
        for phrase in self.phrases:
            phrase.clear_tags()

    def merge(
        self,
        other_text
    ):
        """
        Merges another text into this. Only the title and metadata of this text will be preserved.

        :param other_text:
        :return:
        """
        assert isinstance(other_text, Text)
        self.add_phrases(other_text.phrases)

        return self

    def detokenize(self):
        if self.plain_text and self.plain_text != "":
            return self.plain_text
        else:
            return "\n".join([phrase.detokenize() for phrase in self.phrases])

    def map_tags(self, tagset='tc'):
        for phrase in self.phrases:
            phrase.map_tags(tagset)

    def attributes(self):
        """
        Return all non-children attributes of the text.

        :return:
        """
        return {
            'title': self.title,
            'title_translation': self.title_translation,
            'language': self.language,
            'plain_text': self.plain_text,
            'rich_text': self.rich_text,
            'metadata': self.metadata
        }

    def to_dict(self):
        return {
            'title': self.title,
            'title_translation': self.title_translation,
            'language': self.language,
            'plain_text': self.plain_text,
            'rich_text': self.rich_text,
            'metadata': self.metadata,
            'phrases': list(map(lambda phr: phr.to_dict(), self.phrases))
        }

    def __getitem__(self, item):
        return self.phrases[item]

    def __str__(self):
        return dump(self.to_dict())

    def __iter__(self):
        return self.phrases.__iter__()


class PhraseValidity(Enum):
    UNKNOWN = 'UNKNOWN'
    VALID = 'VALID'
    INVALID = 'INVALID'
    SPECIAL = 'SPECIAL'
    EMPTY = 'EMPTY'


class Phrase(TypecraftModel):
    """
    The class representing a phrase-object.

    A phrase is a collection of words.
    """

    def __init__(
        self,
        phrase="",
        translation="",
        translation2="",
        global_tag_set=None,
        global_tags=None,
        comment="",
        validity=PhraseValidity.EMPTY,
        offset=0,
        duration=0,
        senses=None,
        words=None
    ):
        """
        Constructor.
        """
        self.phrase = phrase
        self.translation = translation
        self.translation2 = translation2
        self.global_tag_set = DEFAULT_TAGSET
        self.comment = comment
        self.offset = offset
        self.duration = duration
        self.senses = []
        self.words = []
        self.global_tags = []

        if words:
            self.add_words(words)
        if senses:
            self.add_senses(senses)
        if global_tags:
            self.add_global_tags(global_tags)
        if global_tag_set:
            self.set_global_tagset(global_tag_set)

        if isinstance(validity, six.string_types):
            if not hasattr(PhraseValidity, validity):
                raise Exception("Error setting validity for phrase. Got an invalid validity tag '%s'" % validity)
            else:
                self.validity = PhraseValidity[validity]
        else:
            self.validity = validity

    def add_word(self, word):
        """
        Adds a word to the phrase.

        :param word:
        :return: Nothing
        """
        if not (isinstance(word, Word)):
            raise Exception("Bad argument to add_word, expected a word instance, got %s" % (type(word)))

        self.words.append(word)

    def add_words(self, words):
        """
        Adds an iterable of words to the phrase.

        :param words:
        :return: Nothing
        """
        for word in words:
            self.add_word(word)

    def add_sense(self, sense):
        """
        Adds a sense-tag to the phrase
        :param sense: A sense tag
        :return: Void
        """
        self.senses.append(sense)

    def add_senses(self, senses):
        """
        Adds an iterable of senses to the phrase.

        :param senses: An iterable of senses.
        :return: Void
        """
        for sense in senses:
            self.add_sense(sense)

    def add_global_tag(self, global_tag):
        """
        Adds a global tag to the phrase. Will raise an exception if argument is not a GlobalTag object.
        :param global_tag: GlobalTag object.
        :return: Void
        """
        if not isinstance(global_tag, GlobalTag):
            raise Exception("Bad argument to add_global_tag. Expected instance of GlobalTag, got %s"
                            % str(type(global_tag)))
        self.global_tags.append(global_tag)

    def add_global_tags(self, global_tags):
        """
        Adds an iterable of global tags. Will call `add_global_tag` with each object in the iterable.
        In turn this might raise an exception if either of the objects in the iterable is not a GlobalTag
        object.
        :param global_tags: An iterable.
        :return: Void
        """
        for tag in global_tags:
            self.add_global_tag(tag)

    def set_global_tagset(self, global_tag_set):
        """
        Sets the global tagset of the phrase. Will raise an exception if the passed in argument is not
        a GlobalTagSet object.

        :param global_tag_set: GlobalTagSet object.
        :return: Void
        """
        if not isinstance(global_tag_set, GlobalTagSet):
            raise Exception("Bad argument to set_global_tagset. Expected instance of GlobalTagSet, got %s"
                            % str(type(global_tag_set)))

        self.global_tag_set = global_tag_set

    def remove_word(self, word):
        """
        Removes a word from the phrase if it exists.

        :param word:
        :return:
        """
        self.words.remove(word)

    def remove_global_tag(self, global_tag):
        """
        Removes a global tag by reference.

        :param global_tag:
        :return:
        """
        self.global_tags.remove(global_tag)

    def remove_global_tag_by_level(self, global_tag_level):
        """
        Removes a global tag by the id of the global tag by level.

        :param global_tag_level:
        :return:
        """
        self.global_tags = list(map(lambda x: x.level != global_tag_level, self.global_tags))

    def clear_words(self):
        """
        Clears all words in phrase. This method does not touch on the "phrase" variable, but rather
        the Word children objects.
        :return:
        """
        self.words = []

    def clear_tags(self):
        """
        Clears all tags in phrase. This involves clearing all words and their constituent morphemes
        for any tag, as well as all global tags and sense tags for the phrase.

        :return: void
        """
        for word in self.words:
            word.clear_tags()

        self.global_tags = []
        self.senses = []

    def detokenize(self):
        if self.phrase:
            return self.phrase
        else:
            # Import detokenize here to avoid circular import
            from typecraft_python.parsing.convenience import detokenize
            return detokenize([word.word for word in self.words])

    def map_tags(self, tagset='tc'):
        for word in self.words:
            word.map_tags(tagset)

    def merge(self, other):
        assert isinstance(other, Phrase)
        # Merging phrases may or may not make sense.
        # But if this method is called, we assume that the phrase should just be
        # appended with a space in between. All other properties are merged
        # in the way which seems most reasonable.
        self.phrase = self.phrase + " " + other.phrase
        self.translation = self.translation + " " + other.translation
        self.translation2 = self.translation2 + " " + other.translation2
        self.comment = self.comment + "\n" + other.comment
        self.duration = self.duration + other.duration
        self.senses.extend(other.senses)
        self.words.extend(other.words)

    def attributes(self):
        """
        Gets all non-children attributes of the phrase.
        :return:
        """
        return {
            'phrase': self.phrase,
            'translation': self.translation,
            'translation2': self.translation2,
            'comment': self.comment,
            'offset': str(self.offset),
            'duration': str(self.duration),
            'senses': self.senses
        }

    def to_dict(self):
        return {
            'phrase': self.phrase,
            'translation': self.translation,
            'translation2': self.translation2,
            'comment': self.comment,
            'offset': str(self.offset),
            'duration': str(self.duration),
            'senses': self.senses,
            'words': list(map(lambda wrd: wrd.to_dict(), self.words))
        }

    def __getitem__(self, item):
        return self.words[item]

    def __str__(self):
        return dump(self.to_dict())

    def __iter__(self):
        return self.words.__iter__()


class Word(TypecraftModel):
    """
    The class representing a Word.

    A word is a collection of morphemes and an associated POS-tag.
    """

    def __init__(
        self,
        word="",
        ipa="",
        pos="",
        stem_morpheme=None,
        morphemes=None
    ):
        """
        Default constructor.
        """
        self.word = word
        self.ipa = ipa
        self.pos = pos
        self.stem_morpheme = stem_morpheme
        self.morphemes = morphemes or []

    def add_morpheme(self, morpheme):
        """
        Adds a morpheme to this word.

        :param morpheme:
        :return: Nothing
        """
        if not (isinstance(morpheme, Morpheme)):
            raise Exception("Wrong argument to add_morpheme, expected Morpheme instance")

        self.morphemes.append(morpheme)

    def add_morphemes(self, morphemes):
        """
        Adds an iterable of morphemes to this word.

        :param morphemes:
        :return: void
        """
        for morpheme in morphemes:
            self.add_morpheme(morpheme)

    def remove_morpheme(self, morpheme):
        """
        Removes a morpheme from the word if it exists.

        :param morpheme:
        :return: void
        """
        self.morphemes.remove(morpheme)

    def clear_morphemes(self):
        """
        Clears all morphemes of the word.
        :return: void
        """
        self.morphemes = []

    def clear_tags(self):
        """
        Clears all tags of the word. This means resetting the pos tag
        as well as any morphemes gloss tag.

        :return: void
        """
        self.pos = ""
        for morpheme in self.morphemes:
            morpheme.clear_tags()

    def attributes(self):
        """
        Returns all non-children attributes of the word.

        :return:
        """
        return {
            'word': self.word,
            'ipa': self.ipa,
            'pos': self.pos,
            'stem_morpheme': self.stem_morpheme
        }

    def to_dict(self):
        return {
            'word': self.word,
            'ipa': self.ipa,
            'pos': self.pos,
            'stem_morpheme': self.stem_morpheme,
            'morphemes': list(map(lambda morpheme: morpheme.to_dict(), self.morphemes))
        }

    def detokenize(self):
        return self.word

    def map_tags(self, tagset='tc'):
        self.pos = get_pos_conversions(self.pos, tagset)
        for morpheme in self.morphemes:
            morpheme.map_tags(tagset)

    def merge(self, other):
        # Merging words does not seem to make sense
        raise NotImplementedError("Merge not implemented for the Word model: Why would you want to merge two words?")

    def __getitem__(self, item):
        return self.morphemes[item]

    def __str__(self):
        return dump(self.to_dict())

    def __iter__(self):
        return self.morphemes.__iter__()

    @staticmethod
    def from_text(word):
        obj = Word()
        obj.word = word
        return obj


class Morpheme(TypecraftModel):
    """
    The class representing a morpheme.

    A morpheme is the tiniest building block of the typecraft xml-format.

    It is comprised of a text-content and a set of glosses.
    """

    def __getitem__(self, item):
        pass

    def __iter__(self):
        pass

    def __init__(
        self,
        morpheme="",
        meaning="",
        baseform="",
        glosses=[]
    ):
        self.morpheme = morpheme
        self.meaning = meaning
        self.baseform = baseform
        self.glosses = []

        if isinstance(glosses, six.string_types):
            self.add_concatenated_glosses(glosses)
        else:
            self.add_glosses(glosses)

    def add_gloss(self, gloss):
        """
        Adds a gloss in string-form to this morpheme.

        :param gloss:serialize_new_user
        :return:
        """
        self.glosses.append(gloss)

    def add_glosses(self, glosses):
        """
        Adds an iterable of glosses in string-form to this morpheme
        :param glosses:
        :return:
        """
        if isinstance(glosses, six.string_types):
            self.add_concatenated_glosses(glosses)
            return

        for gloss in glosses:
            self.add_gloss(gloss)

    def add_concatenated_glosses(self, glosses):
        """
        Adds an iterable of glosses in concatenated form to this morpheme.

        Example input: 3SG.FEM.INDEF => add_glosses([3SG, FEM, INDEF])

        :param glosses: A string representing one or more glosses in concatenated form.
        :return: Void
        """
        if not isinstance(glosses, six.string_types):
            raise Exception("Erroneous input to add_concatenated_glosses: Expected string, got " + str(type(glosses)))

        for gloss in glosses.split("."):
            self.add_gloss(gloss)

    def get_glosses_concatenated(self, sort=False):
        """
        Gets the glosses of this morpheme in concatenated form:

        Example:
        [SG, MASC, DEF] => SG.MASC.DEF

        :param sort: If sort is true, the glosses will be sorted before concatenation
        :return: A string with the glosses in concatenated form
        """
        if sort:
            return ".".join(sorted(self.glosses))
        else:
            return ".".join(self.glosses)

    def remove_gloss(self, gloss):
        """
        Removes a gloss from the morpheme if it exists.

        :param gloss:
        :return:
        """
        self.glosses.remove(gloss)

    def clear_glosses(self):
        """
        Removes all glosses from the morpheme.

        :return: void
        """
        self.glosses = []

    def clear_tags(self):
        """
        Clears the morpheme for all tags. This is the same as clearing for glosses,
        i.e. this method is an alias for clear_glosses.

        :return: void
        """
        self.clear_glosses()

    def detokenize(self):
        return self.morpheme

    def map_tags(self, tagset='tc'):
        return get_gloss_conversions(self.glosses)

    def merge(self, other):
        # Merging morphemes does not seem to make sense
        raise NotImplementedError("Merge not implemented for the Morpheme model: "
                                  "Why would you want to merge two morphemes?")

    def attributes(self):
        """
        Returns all non-children attributes of the morpheme.
        :return:
        """
        return {
            'morpheme': self.morpheme,
            'baseform': self.baseform,
            'meaning': self.meaning
        }

    def to_dict(self):
        return {
            'morpheme': self.morpheme,
            'baseform': self.baseform,
            'meaning': self.meaning,
            'glosses': self.glosses
        }

    def __str__(self):
        return dump(self.to_dict())


class GlobalTagSet(object):
    """
    Class representing meta-information about a global tagset.
    """
    def __init__(
        self,
        id=1,
        name="Default"
    ):
        self.id = id
        self.name = name


class GlobalTag(object):
    """
    Class representing a global tag.
    """
    def __init__(
        self,
        name="",
        level=0,
        description=""
    ):
        self.name = name
        self.level = level
        self.description = description  # Currently unused, but exists to mirror the implementation in TC-Core.


DEFAULT_TAGSET = GlobalTagSet(1, "DEFAULT")
