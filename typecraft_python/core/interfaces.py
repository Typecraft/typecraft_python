

class TypecraftTagger(object):
    """
    This class represents an interface that provides a number of
    methods which taggers that accept typecraft objects should have.
    """

    def is_parser(self):
        """
        This method should return true if the tagger supports morphological parsing
        and gloss-tagging.

        :return: True or false
        """
        raise NotImplementedError()

    def has_automatic_sentence_tokenization_support(self):
        """
        Returns true if the tagger is capable of automatically tokenizing sentences.
        from a raw text.
        :return:
        """
        raise NotImplementedError()

    def has_automatic_word_tokenization_support(self):
        """
        Returns true if the tagger is capable of automatically tokenizing words.
        :return:
        """
        raise NotImplementedError()

    def tag_raw(self, raw_text, language='en'):
        """
        Tags a raw text.

        :param language: The language of the text to be tagged.
        :param raw_text: A not-tokenized raw text.
        :return: A list of Typecraft Phrase objects with tagged words.
        """
        raise NotImplementedError()

    def tag_raw_phrases(self, phrases, language='en'):
        """
        Tags a list of phrasal tokens.

        :param language: The language of the text to be tagged.
        :param phrase_list: A list of
        :return:
a       """
        raise NotImplementedError()

    def tag_raw_words(self, word_list, language='en'):
        """
        Tags a list of words.

        :param language: The language of the text to be tagged.
        :param word_list: A single Typecraft Phrase object with tagged words.
        :return:
        """
        raise NotImplementedError()

    def tag_text(self, text, language='en'):
        """
        Tags a Typecraft Text object.

        Will iterate over all phrases and tag each individual phrase.

        :param language: The language of the text to be tagged.
        :param text:
        :return:
        """
        raise NotImplementedError()

    def tag_phrases(self, phrases, language='en'):
        """
        Tags a collection of phrases.

        :param phrases:
        :param language: The language of the text to be tagged.
        :return:
        """
        raise NotImplementedError()

    def tag_phrase(self, phrase, language='en'):
        """
        Tags a Typecraft Phrase object.

        :param language: The language of the text to be tagged.
        :param phrase:
        :return:
        """
        raise NotImplementedError()

    def tag_words(self, words, language='en'):
        """
        Tags a list of Typecraft Word objects.

        :param language: The language of the text to be tagged.
        :param words:
        :return:
        """
        raise NotImplementedError()

    def tag_word(self, word, language='en'):
        """
        Tags a single Typecraft Word object.

        :param language: The language of the text to be tagged.
        :param word:
        :return:
        """
        raise NotImplementedError()

