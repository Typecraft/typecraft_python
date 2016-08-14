
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

