from tc_xml_python.models.word import Word


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
