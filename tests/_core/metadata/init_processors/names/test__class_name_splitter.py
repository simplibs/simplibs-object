"""
Tests for `_core/metadata/init_processors/names/_class_name_splitter.py`.

Definition errors are tested as `SimpleDefinitionError` because this module
is located under `_core/metadata/`.
"""
import pytest
from simplibs.object._core.metadata.init_processors.names._class_name_splitter import (
    _class_name_splitter,
)
from simplibs.object.exceptions import SimpleDefinitionError


class TestClassNameSplitterBasic:

    def test_single_word(self):
        assert _class_name_splitter("Age") == ("Age",)

    def test_two_words(self):
        assert _class_name_splitter("FirstName") == ("First", "Name")

    def test_three_words(self):
        assert _class_name_splitter("MyPersonAge") == (
            "My",
            "Person",
            "Age",
        )


class TestClassNameSplitterAcronyms:

    def test_acronym_is_kept_uppercase_as_one_block(self):
        result = _class_name_splitter("HTTPRequest")
        assert result == ("HTTP", "Request")

    def test_acronym_followed_by_lowercase_splits_last_upper_correctly(self):
        result = _class_name_splitter("IOStream")
        assert result == ("IO", "Stream")


class TestClassNameSplitterDigits:

    def test_digits_start_new_block(self):
        result = _class_name_splitter("Version2Alpha")
        assert result == ("Version", "2", "Alpha")

    def test_leading_digit_forms_own_block(self):
        result = _class_name_splitter("A1B2")
        assert result == ("A", "1", "B", "2")


class TestClassNameSplitterValidation:

    def test_non_identifier_raises_definition_error(self):
        with pytest.raises(SimpleDefinitionError):
            _class_name_splitter("123Invalid")

    def test_non_ascii_raises_definition_error(self):
        with pytest.raises(SimpleDefinitionError):
            _class_name_splitter("Věk")

    def test_underscore_raises_definition_error(self):
        with pytest.raises(SimpleDefinitionError):
            _class_name_splitter("My_Class")