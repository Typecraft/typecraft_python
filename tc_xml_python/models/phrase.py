

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
        self.freetranslation = ""
        self.freetranslation2 = ""
        self.comment = ""
        self.offset = 0
        self.duration = 0
        self.senses = []
        self.words = []
