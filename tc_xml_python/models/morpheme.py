

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

