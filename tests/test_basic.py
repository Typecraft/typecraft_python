import tc_xml_python


class TestBasic(object):
    @classmethod
    def setup_class(cls):
        pass

    def test_variables_exist(self):
        assert tc_xml_python.__author__ is not None
        assert tc_xml_python.__email__ is not None
        assert tc_xml_python.__version__ is not None
