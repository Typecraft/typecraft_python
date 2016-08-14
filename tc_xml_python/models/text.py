from tc_xml_python.models.phrase import Phrase


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
        self.language = "und" # Und is the default for the undefined language
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
            raise Exception("Wrong argaument to add_metadata. Expected a key-value pair as "
                            "argument one and two")
