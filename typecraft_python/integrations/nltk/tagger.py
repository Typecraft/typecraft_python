import sys

from typecraft_python.core.interfaces import TypecraftTagger
from typecraft_python.parsing.convenience import word_pos_tuples_to_phrase

try:
    import nltk
except ImportError:
    nltk = None
    sys.stderr.write("Unable to load NLTK, are you sure it is installed?")


class NltkTagger(TypecraftTagger):

    def is_parser(self):
        return False

    def has_automatic_sentence_tokenization_support(self, language='en'):
        return False

    def has_automatic_word_tokenization_support(self, language='en'):
        return False

    @staticmethod
    def _tag_and_add_to_words(words, language='en'):
        """
        Tags
        :param word_tokens:
        :param language:
        :return:
        """
        tokens = [word.word for word in words]
        tagged = nltk.pos_tag(tokens, lang=language)
        for tagged, word in zip(tagged, words):
            word.pos = tagged[1]
        return words

    def tag_raw(self, raw_text, language='en'):
        raise NotImplementedError("Nltk cannot tag raw text. Please tokenize first.")

    def tag_raw_phrases(self, phrases, language='en'):
        raise NotImplementedError("Nltk cannot tag raw phrases. Please tokenize first.")

    def tag_raw_words(self, word_list, language='en'):
        tagged = nltk.pos_tag(word_list, lang=language)
        return word_pos_tuples_to_phrase(tagged)

    def tag_text(self, text, language='en'):
        self.tag_phrases(text.phrases)
        return text

    def tag_phrases(self, phrases, language='en'):
        for phrase in phrases:
            self.tag_phrase(phrase)
        return phrases

    def tag_phrase(self, phrase, language='en'):
        self.tag_words(phrase.words, language)
        return phrase

    def tag_words(self, words, language='en'):
        self._tag_and_add_to_words(words, language)
        return words

    def tag_word(self, word, language='en'):
        self._tag_and_add_to_words([word])
        return word
