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
