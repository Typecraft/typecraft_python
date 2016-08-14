from tc_xml_python.models import *

class TestModels(object):
    @classmethod
    def setup_class(cls):
        pass

    def test_models_exist(self):
        assert text.Text is not None
        assert phrase.Phrase is not None
        assert word.Word is not None
        assert morpheme.Morpheme is not None


