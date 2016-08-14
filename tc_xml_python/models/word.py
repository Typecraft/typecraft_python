from tc_xml_python.models.morpheme import Morpheme


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
        if not (isinstance(morpheme, Morpheme)):
            raise Exception("Wrong argument to add_morpheme, expected Morpheme instance")

        self.morphemes.append(morpheme)
