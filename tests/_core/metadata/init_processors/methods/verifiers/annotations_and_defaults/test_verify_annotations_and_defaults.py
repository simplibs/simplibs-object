"""
Tests for `_core/metadata/init_processors/methods/verifiers/annotations_and_defaults/verify_annotations_and_defaults.py`.

Tested via concrete class definitions with differing annotations and defaults on
`_logic` (positional defaults) and `_validate` (keyword-only default `return_bool`).
This verification triggers only when the user explicitly provides annotations/defaults;
otherwise, it is skipped in favor of the auto-injected defaults.
"""
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions import SimpleDefinitionError


def _int_const(name, default=0):
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


class TestVerifyAnnotationsMismatch:

    def test_wrong_param_annotation_raises(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class BadAnnotation(SimpleObject):
                _type = int
                _inners = (First,)

                @classmethod
                def _logic(cls, first: str) -> int:
                    return first

    def test_wrong_return_annotation_raises(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class BadReturnAnnotation(SimpleObject):
                _type = int
                _inners = (First,)

                @classmethod
                def _logic(cls, first: int) -> str:
                    return first

    def test_matching_annotations_are_accepted(self):
        First = _int_const("First")

        class GoodAnnotation(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first: int) -> int:
                return first

        assert GoodAnnotation.calculate_value(5) == 5


class TestVerifyPositionalDefaultsMismatch:

    def test_wrong_positional_default_raises(self):
        First = _int_const("First", default=0)

        with pytest.raises(SimpleDefinitionError):
            class BadDefault(SimpleObject):
                _type = int
                _inners = (First,)

                @classmethod
                def _logic(cls, first=999):
                    return first

    def test_matching_positional_default_is_accepted(self):
        First = _int_const("First", default=7)

        class GoodDefault(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first=7):
                return first

        assert GoodDefault.calculate_value() == 7


class TestVerifyKeywordOnlyDefaultsMismatch:

    def test_wrong_kwonly_default_on_validate_raises(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class BadValidateDefault(SimpleObject):
                _type = int
                _inners = (First,)

                @classmethod
                def _logic(cls, first):
                    return first

                @classmethod
                def _validate(cls, value, *, return_bool=True):
                    return True

    def test_matching_kwonly_default_on_validate_is_accepted(self):
        First = _int_const("First")

        class GoodValidateDefault(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

            @classmethod
            def _validate(cls, value, *, return_bool=False):
                return True

        assert GoodValidateDefault.calculate_value(3) == 3