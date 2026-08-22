"""
Tests for `_core/metadata/init_processors/default/process_default_for_constant.py`[cite: 78].

Errors under `_core/metadata/` are validated via `SimpleDefinitionError`[cite: 78].
"""
import pytest
from simplibs.object import SimpleConstant
from simplibs.object.exceptions import SimpleDefinitionError


class TestProcessDefaultForConstantHappyPath:

    def test_valid_default_is_returned(self) -> None:
        class Age(SimpleConstant):
            _type = int
            _default = 18

        assert Age.meta.default == 18

    def test_falsy_but_valid_default_is_accepted(self) -> None:
        """0 is a valid integer default and must not be confused with unprovided defaults."""
        class Counter(SimpleConstant):
            _type = int
            _default = 0

        assert Counter.meta.default == 0

    def test_empty_string_default_is_accepted(self) -> None:
        class Label(SimpleConstant):
            _type = str
            _default = ""

        assert Label.meta.default == ""


class TestProcessDefaultForConstantMissing:

    def test_missing_default_raises_definition_error(self) -> None:
        with pytest.raises(SimpleDefinitionError):
            class NoDefault(SimpleConstant):
                _type = int


class TestProcessDefaultForConstantTypeMismatch:

    def test_default_not_matching_type_raises_definition_error(self) -> None:
        with pytest.raises(SimpleDefinitionError):
            class WrongDefault(SimpleConstant):
                _type = int
                _default = "not-an-int"

    def test_default_matching_union_type_is_accepted(self) -> None:
        class MaybeIntOrStr(SimpleConstant):
            _type = int | str
            _default = "hello"

        assert MaybeIntOrStr.meta.default == "hello"