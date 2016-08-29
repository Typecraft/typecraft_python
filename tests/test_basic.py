import typecraft_python


class TestBasic(object):
    @classmethod
    def setup_class(cls):
        pass

    def test_variables_exist(self):
        assert typecraft_python.__author__ is not None
        assert typecraft_python.__email__ is not None
        assert typecraft_python.__version__ is not None
