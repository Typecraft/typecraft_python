import logging

import nltk
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

    @staticmethod
    def _sentence_tokenize_en_result(result):
        batched_result = []
        current = []
        for token in result:
            current.append(token)
            if token.split("\t")[1] == 'SENT':
                batched_result.append(current)
                current = []
        return batched_result

    @staticmethod
    def _convert_result_with_line_numbers_to_phrases(result):
        lines = []
        current = []
        # First entry is always a line number here
        for entry in result[1:]:
            if '<ttpw:line num=\"' in entry:
                lines.append(current)
                current = []
            else:
                current.append(entry)

        lines.append(current)

        return [TreeTagger._convert_result_to_phrase(line) for line in lines]

    def is_parser(self):
        return False

    def has_automatic_sentence_tokenization_support(self, language='en'):
        return True

    def has_automatic_word_tokenization_support(self, language='en'):
        return True

    def tag_raw(self, raw_text, language='en'):
        phrases = []
        if language == 'en':
            # This is easy, as each end-sentence token is tagged SENT
            tagged = self._get_tagger_instance(language).tag_text(raw_text)
            sentence_tokenized = self._sentence_tokenize_en_result(tagged)
            for sentence in sentence_tokenized:
                phrases.append(self._convert_result_to_phrase(sentence))
        else:
            # Sent tokenize then join by new lines. Now we can get line indicators
            # from the TreeTagger automatically.
            raw_text = "\n".join(nltk.sent_tokenize(raw_text))
            tagged = self._get_tagger_instance(language).tag_text(raw_text, numlines=True)
            phrases = self._convert_result_with_line_numbers_to_phrases(tagged)

        return phrases

    def tag_raw_phrases(self, phrases, language='en'):
        pass

    def tag_raw_words(self, word_list, language='en'):
        tagged = self._get_tagger_instance(language).tag_text(word_list, tagonly=True)
        return self._convert_result_to_phrase(tagged)

    def tag_text(self, text, language='en'):
        assert isinstance(text, Text)
        for phrase in text:
            self.tag_phrase(phrase, language)
        return text

    def tag_phrases(self, phrases, language='en'):
        for phrase in phrases:
            self.tag_phrase(phrase, language)
        return phrases

    def tag_phrase(self, phrase, language='en'):
        self.tag_words(phrase.words)
        return phrase

    def tag_words(self, words, language='en'):
        raw_words = [word.word for word in words]
        tagged = self._get_tagger_instance(language).tag_text(raw_words, tagonly=True)
        tagged = list(map(lambda x: x.split("\t"), tagged))
        if len(tagged) != len(words):
            logging.error("Error tagging with the TreeTagger. Number of tagged words "
                          "does not match number of words passed to the TreeTagger.")
            return words

        for tag_result, word in zip(tagged, words):
            word.pos = tag_result[1]
            if tag_result[2]:
                # If the word has no morphemes, we add one with the
                # lemmatization
                if len(word.morphemes) == 0:
                    word.add_morpheme(Morpheme(
                        morpheme=word.word,
                        baseform=tag_result[2]
                    ))
        return words

    def tag_word(self, word, language='en'):
        tagged = self._get_tagger_instance(language).tag_text(word.word)
        tagged = list(map(lambda x: x.split("\t"), tagged))
        word.pos = tagged[0][1]
        return word

