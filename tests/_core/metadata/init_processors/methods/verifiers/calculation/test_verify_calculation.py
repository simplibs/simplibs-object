"""
Tests for `_core/metadata/init_processors/methods/verifiers/calculation/verify_calculation.py`.
"""
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions import SimpleDefinitionError


def _int_const(name, default=0):
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


class TestVerifyCalculationHappyPath:

    def test_logic_dry_run_succeeds_and_calculates_default(self):
        First = _int_const("First", default=2)
        Second = _int_const("Second", default=3)

        class Pair(SimpleObject):
            _type = int
            _inners = (First, Second)

            @classmethod
            def _logic(cls, first, second):
                return first + second

        assert Pair.meta.default == 5


class TestVerifyCalculationExceptionDuringDryRun:

    def test_logic_raising_exception_becomes_definition_error(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class Exploding(SimpleObject):
                _type = int
                _inners = (First,)

                @classmethod
                def _logic(cls, first):
                    raise RuntimeError("boom during dry-run")


class TestVerifyCalculationWrongReturnType:

    def test_logic_returning_wrong_type_raises(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class WrongReturn(SimpleObject):
                _type = int
                _inners = (First,)

                @classmethod
                def _logic(cls, first):
                    return "not-an-int"


class TestVerifyCalculationDecomposeHappyPath:

    def test_correct_tuple_returning_decompose_succeeds(self):
        First = _int_const("First")
        Second = _int_const("Second")

        class Pair(SimpleObject):
            _type = int
            _inners = (First, Second)

            @classmethod
            def _logic(cls, first, second):
                return first + second

            @classmethod
            def _decompose(cls, value):
                return value, 0

        assert Pair.meta.default == 0

    def test_single_inner_decompose_succeeds(self):
        First = _int_const("First")

        class Single(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

            @classmethod
            def _decompose(cls, value):
                return (value,)

        assert Single.meta.default == 0