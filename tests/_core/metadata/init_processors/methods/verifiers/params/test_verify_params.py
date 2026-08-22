"""
Tests for `_core/metadata/init_processors/methods/verifiers/params/verify_params.py`.
"""
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions import SimpleDefinitionError


def _int_const(name, default=0):
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


class TestVerifyParamsHappyPath:

    def test_correct_param_names_and_count_pass(self):
        First = _int_const("First")
        Second = _int_const("Second")

        class Pair(SimpleObject):
            _type = int
            _inners = (First, Second)

            @classmethod
            def _logic(cls, first, second):
                return first + second

        assert Pair.calculate_value(1, 2) == 3


class TestVerifyParamsWrongNames:

    def test_wrong_param_name_raises(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class Single(SimpleObject):
                _type = int
                _inners = (First,)

                @classmethod
                def _logic(cls, wrong_name):
                    return wrong_name


class TestVerifyParamsWrongCount:

    def test_extra_positional_param_raises(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class Single(SimpleObject):
                _type = int
                _inners = (First,)

                @classmethod
                def _logic(cls, first, extra):
                    return first

    def test_missing_positional_param_raises(self):
        First = _int_const("First")
        Second = _int_const("Second")

        with pytest.raises(SimpleDefinitionError):
            class Pair(SimpleObject):
                _type = int
                _inners = (First, Second)

                @classmethod
                def _logic(cls, first):
                    return first


class TestVerifyParamsPlaceholdersForbidden:

    def test_varargs_raises(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class Single(SimpleObject):
                _type = int
                _inners = (First,)

                @classmethod
                def _logic(cls, *args):
                    return args[0]

    def test_varkwargs_raises(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class Single(SimpleObject):
                _type = int
                _inners = (First,)

                @classmethod
                def _logic(cls, first, **kwargs):
                    return first