from tc_xml_python.models import Text, Phrase, Word, Morpheme

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
