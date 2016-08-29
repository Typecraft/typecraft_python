from typecraft_python.models import Text, Phrase, Word, Morpheme


class TestModels(object):
    @classmethod
    def setup_class(cls):
        pass

    def test_models_exist(self):
        assert Text is not None
        assert Phrase is not None
        assert Word is not None
        assert Morpheme is not None

    def test_init_text(self):
        my_text = Text()

        assert my_text is not None
        assert my_text.title is ""
        assert my_text.title_translation is ""
        assert my_text.language is "und"
        assert my_text.plain_text is ""
        assert my_text.rich_text is ""
        assert my_text.delta is not None
        assert my_text.metadata is not None
        assert my_text.phrases is not None

    def test_init_phrase(self):
        my_phrase = Phrase()

        assert my_phrase is not None

        assert my_phrase.phrase is ""
        assert my_phrase.free_translation is ""
        assert my_phrase.free_translation2 is ""
        assert my_phrase.comment is ""
        assert my_phrase.offset is 0
        assert my_phrase.duration is 0
        assert my_phrase.senses is not None
        assert my_phrase.words is not None

    def test_init_word(self):
        pass

    def test_init_morpheme(self):
        pass

    def test_add_phrase_to_text(self):
        pass

    def test_add_word_to_phrase(self):
        pass

    def test_add_morpheme_to_word(self):
        pass

    def test_to_dict(self):
        text = Text()
        phrase = Phrase()
        word = Word()
        morpheme = Morpheme()

        text.add_phrase(phrase)

        text_dict = text.to_dict()
        phrase_dict = phrase.to_dict()
        word_dict = word.to_dict()
        morpheme_dict = morpheme.to_dict()

        assert isinstance(text_dict, dict)
        assert isinstance(phrase_dict, dict)
        assert isinstance(word_dict, dict)
        assert isinstance(morpheme_dict, dict)

    def test_to_str(self):
        text = Text()
        phrase = Phrase()
        word = Word()
        morpheme = Morpheme()

        text.add_phrase(phrase)

        text_str = str(text)
        phrase_str = str(phrase)
        word_str = str(word)
        morpheme_str = str(morpheme)

        assert isinstance(text_str, basestring)
        assert isinstance(phrase_str, basestring)
        assert isinstance(word_str, basestring)
        assert isinstance(morpheme_str, basestring)

    def test_iter_text(self):
        text = Text()

        phrase_1 = Phrase()
        phrase_2 = Phrase()

        phrases = [phrase_1, phrase_2]

        text.add_phrase(phrase_1)
        text.add_phrase(phrase_2)

        for phrase in text:
            assert phrase in phrases

    def test_iter_phrase(self):
        phrase = Phrase()

        word_1 = Word()
        word_2 = Word()

        words = [word_1, word_2]

        phrase.add_word(word_1)
        phrase.add_word(word_2)

        for word in phrase:
            assert word in words

    def test_iter_word(self):
        word = Word()

        morph_1 = Morpheme()
        morph_2 = Morpheme()

        morphs = [morph_1, morph_2]

        word.add_morpheme(morph_1)
        word.add_morpheme(morph_2)

        for morph in word:
            assert morph in morphs

    def test_get_glosses_concatenated(self):
        morpheme = Morpheme()

        morpheme.add_gloss("PURP")
        morpheme.add_gloss("ADJ>ADV")

        assert morpheme.get_glosses_concatenated() == "PURP.ADJ>ADV"
        assert morpheme.get_glosses_concatenated(sort=True) == "ADJ>ADV.PURP"

    def test_to_str(self):
        text = Text()
        text_str = str(text)

        phr = Phrase()
        phr_str = str(phr)

        wrd = Word()
        wrd_str = str(wrd)

        mrph = Morpheme()
        morpheme = str(mrph)

