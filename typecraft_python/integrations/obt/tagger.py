import logging
import os
import tempfile
from subprocess import check_output

import nltk

from typecraft_python.core.models import Word, Morpheme, Phrase
from typecraft_python.core.interfaces import TypecraftTagger

# Try to load OBT by the use of the OBT_PATH
# environment variable. Also verify that the
# file tag-bm.sh file exists.
FNULL = open(os.devnull, 'w')
obt_available = False
obt_path = os.environ.get('OBT_PATH')
if obt_path is None:
    logging.error("Error loading OBT, environment variable `OBT_PATH` not set.")
else:
    tag_bm_path = os.path.join(obt_path, 'tag-bm.sh')
    if not os.path.exists(tag_bm_path):
        logging.error("Error loading OBT, the script %s does not exist" % (tag_bm_path,))
    else:
        obt_available = True


class ObtTagger(TypecraftTagger):
    def __init__(self):
        pass

    @staticmethod
    def _store_string_temporarily(raw_string):
        fd, path = tempfile.mkstemp()

        with os.fdopen(fd, "w") as _file:
            _file.write(raw_string.encode("utf-8").strip())

        return path

    @staticmethod
    def _call_obt(tempfile):
        return check_output([os.path.join(obt_path, 'tag-bm.sh'), tempfile], stderr=FNULL).decode("utf-8")

    @staticmethod
    def _word_is_sentence_breaker(tags):
        return '<<<' in tags

    @staticmethod
    def _parse_output_to_phrases(output, original_input, language):
        """
        Parses the output of the OBT to a number of phrases.
        Su

        :param output:
        :return:
        """
        # Import here the avoid circular dependency
        from typecraft_python.util import batch
        phrases = []
        output_lines = output.split("\n")
        batched = batch(output_lines, 3)
        current_phrase = Phrase()
        batched = filter(lambda x: len(x) == 3, batched)

        for original, _, tags in batched:
            # The original is wrapped in <word></word> tags
            original = original[6:-7]
            split_tags = tags.split()
            # The lemma is wrapped in double quotes
            lemma = split_tags[0][1:-1]
            # Punctuations have weird lemmas
            lemma = lemma if not lemma.startswith("$") else original
            pos = split_tags[1]
            word = Word(word=original, pos=pos)
            morpheme = Morpheme(morpheme=original, baseform=lemma)
            word.add_morpheme(morpheme)
            current_phrase.add_word(word)

            if ObtTagger._word_is_sentence_breaker(tags):
                phrases.append(current_phrase)
                current_phrase = Phrase()
                current_phrase.phrase = current_phrase.detokenize()

        # At this stage we have the words contents, but the phrases are not given
        # detokenized versions. We first try to match sentence tokenized phrase from
        # nltk with the phrases. If the amount is uneven we use the `detokenize` method.
        sent_tokenized = nltk.sent_tokenize(original_input)
        if len(sent_tokenized) == len(phrases):
            for i, phrase in enumerate(sent_tokenized):
                phrases[i].phrase = phrase
        else:
            logging.error("Output from OBT does not have as many sentences the tokenized sentences from nltk."
                          "\nFalling back to using `detokenize`."
                          "\n\tOBT:%d"
                          "\n\tNltk:%d" % (len(sent_tokenized), len(phrases)))
            for phrase in phrases:
                phrase.phrase = phrase.detokenize()

        return phrases

    @staticmethod
    def _parse_output_to_phrase(output):
        pass

    def is_parser(self):
        return True

    def has_automatic_sentence_tokenization_support(self, language='en'):
        return True

    def has_automatic_word_tokenization_support(self, language='en'):
        return True

    def tag_raw(self, raw_text, language='nob'):
        if not obt_available:
            raise EnvironmentError("Attempted to parse using OBT when OBT is not available.")
        if not language.startswith('no'):
            logging.error("A non-norwegian language supplied to the Oslo-Bergen tagger.")
        temp_file_path = ObtTagger._store_string_temporarily(raw_text)
        output = self._call_obt(temp_file_path)
        return self._parse_output_to_phrases(output, raw_text, language)

    def tag_raw_phrases(self, phrases, language='nob'):
        if not obt_available:
            raise EnvironmentError("Attempted to parse using OBT when OBT is not available.")
        if not language.startswith('no'):
            logging.error("A non-norwegian language supplied to ")
        pass

    def tag_raw_words(self, word_list, language='nob'):
        if not obt_available:
            raise EnvironmentError("Attempted to parse using OBT when OBT is not available.")
        if not language.startswith('no'):
            logging.error("A non-norwegian language supplied to ")
        pass

    def tag_text(self, text, language='nob'):
        if not obt_available:
            raise EnvironmentError("Attempted to parse using OBT when OBT is not available.")
        if not language.startswith('no'):
            logging.error("A non-norwegian language supplied to ")
        pass

    def tag_phrases(self, phrases, language='nob'):
        if not obt_available:
            raise EnvironmentError("Attempted to parse using OBT when OBT is not available.")
        if not language.startswith('no'):
            logging.error("A non-norwegian language supplied to ")
        pass

    def tag_phrase(self, phrase, language='nob'):
        if not obt_available:
            raise EnvironmentError("Attempted to parse using OBT when OBT is not available.")
        if not language.startswith('no'):
            logging.error("A non-norwegian language supplied to ")
        pass

    def tag_words(self, words, language='nob'):
        if not obt_available:
            raise EnvironmentError("Attempted to parse using OBT when OBT is not available.")
        if not language.startswith('no'):
            logging.error("A non-norwegian language supplied to ")
        pass

    def tag_word(self, word, language='nob'):
        if not obt_available:
            raise EnvironmentError("Attempted to parse using OBT when OBT is not available.")
        if not language.startswith('no'):
            logging.error("A non-norwegian language supplied to ")
        pass

