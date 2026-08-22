"""
Tests for `_core/metadata/init_processors/names/create_names.py`.
"""
from simplibs.object import SimpleConstant


class TestCreateNamesSingleWord:

    def test_simple_class_name_forms(self):
        class Age(SimpleConstant):
            _type = int
            _default = 0

        assert Age.meta.name_tuple == ("Age",)
        assert Age.meta.name_snake == "age"
        assert Age.meta.name_private == "_age"


class TestCreateNamesMultiWord:

    def test_multi_word_class_name_forms(self):
        class FirstName(SimpleConstant):
            _type = str
            _default = ""

        assert FirstName.meta.name_tuple == ("First", "Name")
        assert FirstName.meta.name_snake == "first_name"
        assert FirstName.meta.name_private == "_first_name"


class TestCreateNamesAcronymLowercasedInSnake:

    def test_snake_and_private_are_always_fully_lowercase(self):
        class HTTPCode(SimpleConstant):
            _type = int
            _default = 200

        assert HTTPCode.meta.name_tuple == ("HTTP", "Code")
        assert HTTPCode.meta.name_snake == "http_code"
        assert HTTPCode.meta.name_private == "_http_code"