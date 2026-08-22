"""
Tests for `_core/metadata/init_processors/type/process_type.py`.

Covers all branches of `_type` resolution:
    1. Plain type (`int`)
    2. UnionType (`int | str`)
    3. UnionType containing None -> error (must use a tuple with None instead)
    4. Tuple of types (`(int, str)`) -> merged into UnionType
    5. Tuple containing None or nested tuples -> error
    6. Missing or empty `_type` -> error
    7. Invalid `_type` value (fallback) -> error
"""
import pytest
from simplibs.object import SimpleConstant
from simplibs.object.exceptions import SimpleDefinitionError


class TestProcessTypePlainType:

    def test_plain_type_is_used_directly(self):
        class Age(SimpleConstant):
            _type = int
            _default = 0

        assert Age.meta.value_type is int
        assert Age.meta.value_type_name == "int"


class TestProcessTypeUnionType:

    def test_union_type_is_accepted(self):
        class Flexible(SimpleConstant):
            _type = int | str
            _default = 0

        assert Flexible.meta.value_type == (int | str)

    def test_union_type_name_is_stringified(self):
        class Flexible(SimpleConstant):
            _type = int | str
            _default = 0

        assert Flexible.meta.value_type_name == str(int | str)

    def test_union_type_containing_none_raises(self):
        with pytest.raises(SimpleDefinitionError):
            class Nullable(SimpleConstant):
                _type = int | None
                _default = 0


class TestProcessTypeTuple:

    def test_tuple_of_types_is_merged_into_union(self):
        class Flexible(SimpleConstant):
            _type = (int, str)
            _default = 0

        assert Flexible.meta.value_type == (int | str)

    def test_tuple_with_none_raises(self):
        with pytest.raises(SimpleDefinitionError):
            class Bad(SimpleConstant):
                _type = (int, None)
                _default = 0

    def test_nested_tuple_raises(self):
        with pytest.raises(SimpleDefinitionError):
            class Bad(SimpleConstant):
                _type = (int, (str, float))
                _default = 0


class TestProcessTypeMissing:

    def test_missing_type_raises(self):
        with pytest.raises(SimpleDefinitionError):
            class NoType(SimpleConstant):
                _default = 0

    def test_falsy_type_raises(self):
        with pytest.raises(SimpleDefinitionError):
            class EmptyType(SimpleConstant):
                _type = ()
                _default = 0


class TestProcessTypeInvalidFallback:

    def test_non_type_value_raises(self):
        with pytest.raises(SimpleDefinitionError):
            class Invalid(SimpleConstant):
                _type = "int"
                _default = 0