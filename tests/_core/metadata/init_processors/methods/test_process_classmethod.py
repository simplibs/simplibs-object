"""
Tests for `_core/metadata/init_processors/methods/process_classmethod.py`.
"""
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions import SimpleDefinitionError


def _int_const(name, default=0):
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


class TestProcessClassmethodReturnCalculatedValue:

    def test_logic_returns_bound_method_and_calculated_value(self):
        First = _int_const("First", default=4)

        class Single(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first * 2

        assert callable(Single.meta.logic)
        assert Single.meta.default == 8

    def test_validate_returns_only_bound_method_without_calculated_value(self):
        First = _int_const("First")

        class Single(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

        assert callable(Single.meta.validate)


class TestProcessClassmethodSkipsValidationWhenInherited:

    def test_unmodified_deep_subclass_reuses_same_logic_object(self):
        First = _int_const("First")

        class Single(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

        class SingleVariant(Single):
            pass

        assert SingleVariant.calculate_value(6) == 6


class TestProcessClassmethodValidateDryRun:

    def test_validate_dry_run_uses_default_as_test_value(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class RejectsOwnDefault(SimpleObject):
                _type = int
                _inners = (First,)

                @classmethod
                def _logic(cls, first):
                    return first

                @classmethod
                def _validate(cls, value, *, return_bool=False):
                    return cls.bool_or_raise_validate_error(
                        value, problem="always rejects", return_bool=return_bool
                    )