import logging

import treetaggerwrapper

from typecraft_python.models import Text, Morpheme
from typecraft_python.parsing.convenience import parse_slash_separated_phrase, word_pos_tuples_to_phrase, \
    word_pos_lemma_tuples_to_phrase, detokenize
from typecraft_python.core.interfaces import TypecraftTagger


class TreeTagger(TypecraftTagger):

    @staticmethod
    def _get_tagger_instance(language='en'):
        return treetaggerwrapper.TreeTagger(TAGLANG=language)

    @staticmethod
    def _convert_result_to_phrase(result):
        result = list(map(lambda x: x.split("\t"), result))
        return word_pos_lemma_tuples_to_phrase(result)

    def is_parser(self):
        return False

    def has_automatic_sentence_tokenization_support(self):
        return True

    def has_automatic_word_tokenization_support(self):
        return True

    def tag_raw(self, raw_text, language='en'):
        tagged = self._get_tagger_instance(language).tag_text(raw_text)
        tagged = list(map(lambda x: x.split("\t"), tagged))
        return word_pos_lemma_tuples_to_phrase(tagged)
        # return parse_slash_separated_phrase()

    def tag_raw_words(self, word_list, language='en'):
        detokenized = detokenize(word_list)
        tagged = self._get_tagger_instance(language).tag_text(detokenized)
        tagged = list(map(lambda x: x.split("\t"), tagged))
        return word_pos_lemma_tuples_to_phrase(tagged)

    def tag_text(self, text, language='en'):
        assert isinstance(text, Text)
        for phrase in text:
            self.tag_phrase(phrase, language)
        return text

    def tag_phrase(self, phrase, language='en'):
        detokenized = detokenize([word.word for word in phrase])
        tagged = self._get_tagger_instance(language).tag_text(detokenized)
        tagged = list(map(lambda x: x.split("\t"), tagged))
        if len(tagged) != len(phrase.words):
            logging.error("Error tagging phrase. The TreeTagger lemmatizer detected a different number"
                          " of words compared to what is already included in the Phrase."
                          "\nOriginal:%s\nFrom TreeTagger:%s" % (str([word.word for word in phrase.words]), str(tagged)))
            return phrase

        for i in range(len(tagged)):
            word = phrase[i]
            word.pos = tagged[i][1]
            # If the word has no morphemes, we add one with the
            # lemmatization
            if len(word.morphemes) == 0:
                word.add_morpheme(Morpheme(
                    morpheme=word,
                    baseform=tagged[i][2]
                ))
        return phrase

    def tag_words(self, words, language='en'):
        detokenized = detokenize([word.word for word in words])
        tagged = self._get_tagger_instance(language).tag_text(detokenized)
        tagged = list(map(lambda x: x.split("\t"), tagged))
        if len(tagged) != len(words):
            logging.error("Error tagging words. The TreeTagger lemmatizer detected a different number"
                          " of words compared to what was given.."
                          "\nOriginal:%s\nFrom TreeTagger:%s" % (str([word.word for word in words]), str(tagged)))
            return words
        for i in range(len(tagged)):
            words[i].pos = tagged[i][1]
        return words

    def tag_word(self, word, language='en'):
        tagged = self._get_tagger_instance(language).tag_text(word.word)
        tagged = list(map(lambda x: x.split("\t"), tagged))
        word.pos = tagged[0][1]
        return word

