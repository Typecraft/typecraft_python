from yaml import dump

"""
This file contains all models.
"""


class Corpus:
    """
    The class representing a corpus files.

    This class represents the 1-1 mapping to and from the tc-xml files.
    """
    def __init__(self):
        self.texts = []

    def __iter__(self):
        return self.texts.__iter__()

    def to_dict(self):
        return {
            'texts': self.texts
        }


class Text:
    """
    The class representing a text-object.

    A text is formally a collection of sentences with some extra metadata.
    """

    def __init__(self):
        """
        Default constrcutor
        """
        self.title = ""
        self.title_translation = ""
        self.language = "und"  # Und is the default for the undefined language
        self.plain_text = ""
        self.rich_text = ""
        self.delta = {}
        self.metadata = {}
        self.phrases = []

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
            'delta': self.delta,
            'metadata': self.metadata,
        }

    def to_dict(self):
        return {
            'title': self.title,
            'title_translation': self.title_translation,
            'language': self.language,
            'plain_text': self.plain_text,
            'rich_text': self.rich_text,
            'delta': self.delta,
            'metadata': self.metadata,
            'phrases': list(map(lambda phr: phr.to_dict(), self.phrases))
        }

    def __str__(self):
        return dump(self.to_dict())

    def __iter__(self):
        return self.phrases.__iter__()


class Phrase:
    """
    The class representing a phrase-object.

    A phrase is a collection of words.
    """

    def __init__(self):
        """
        Default constructor.
        """
        self.phrase = ""
        self.free_translation = ""
        self.free_translation2 = ""
        self.comment = ""
        self.offset = 0
        self.duration = 0
        self.senses = []
        self.words = []

    def add_word(self, word):
        """
        Adds a word to the phrase.

        :param word:
        :return: Nothing
        """
        if not (isinstance(word, Word)):
            raise Exception("Bad argument to add_word, expected a word instance")

        self.words.append(word)

    def add_words(self, words):
        """
        Adds an iterable of words to the phrase.

        :param words:
        :return: Nothing
        """
        for word in words:
            self.add_word(word)

    def attributes(self):
        """
        Gets all non-children attributes of the phrase.
        :return:
        """
        return {
            'phrase': self.phrase,
            'free_translation': self.free_translation,
            'free_translation2': self.free_translation2,
            'comment': self.comment,
            'offset': str(self.offset),
            'duration': str(self.duration),
            'senses': self.senses
        }

    def to_dict(self):
        return {
            'phrase': self.phrase,
            'free_translation': self.free_translation,
            'free_translation2': self.free_translation2,
            'comment': self.comment,
            'offset': str(self.offset),
            'duration': str(self.duration),
            'senses': self.senses,
            'words': list(map(lambda wrd: wrd.to_dict(), self.words))
        }

    def __str__(self):
        return dump(self.to_dict())

    def __iter__(self):
        return self.words.__iter__()


class Word:
    """
    The class representing a Word.

    A word is a collection of morphemes and an associated POS-tag.
    """

    def __init__(self):
        """
        Default constructor.
        """
        self.word = ""
        self.ipa = ""
        self.pos = ""
        self.stem_morpheme = None
        self.morphemes = []

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

        :param morpheme:
        :return: Nothing
        """
        for morpheme in morphemes:
            self.add_morpheme(morpheme)

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
            'morphemes': list(map(lambda mrph: mrph.to_dict(), self.morphemes))
        }

    def __str__(self):
        return dump(self.to_dict())

    def __iter__(self):
        return self.morphemes.__iter__()

    @staticmethod
    def from_text(word):
        obj = Word()
        obj.word = word
        return obj


class Morpheme:
    """
    The class representing a morpheme.

    A morpheme is the tiniest building block of the typecraft xml-format.

    It is comprised of a text-content and a set of glosses.
    """

    def __init__(self):
        self.morpheme = ""
        self.meaning = ""
        self.baseform = ""
        self.glosses = []

    def add_gloss(self, gloss):
        """
        Adds a gloss in string-form to this morpheme.

        :param gloss:
        :return:
        """
        self.glosses.append(gloss)

    def add_glosses(self, glosses):
        """
        Adds an iterable of glosses in string-form to this morpheme
        :param glosses:
        :return:
        """
        for gloss in glosses:
            self.add_gloss(gloss)

    def add_concatenated_glosses(self, glosses):
        """
        Adds an iterable of glosses in concatenated form to this morpheme.

        Example input: 3SG.FEM.INDEF => add_glosses([3SG, FEM, INDEF])

        :param glosses:
        :return:
        """
        if not isinstance(glosses, basestring):
            raise Exception("Erroneous input to add_concatenated_glosses: Expected string, got " + type(glosses))

        for gloss in glosses.split("."):
            self.add_gloss(gloss)

    def get_glosses_concatenated(self, sort=False):
        """
        Gets the glosses of this morpheme in concatenated form:

        Example:
        [SG, MASC, DEF] => SG.MASC.DEF

        :param sort: If sort is true, the glosses will be sorted before concatenation
        :return:
        """
        if sort:
            return ".".join(sorted(self.glosses))
        else:
            return ".".join(self.glosses)

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
