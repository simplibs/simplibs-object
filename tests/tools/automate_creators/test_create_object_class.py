"""
Tests for `tools/automate_creators/create_object_class.py`.
"""
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.tools.automate_creators.create_object_class import (
    create_object_class,
)
from simplibs.sentinels import UNSET


def _int_const(name, default=0):
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


class TestCreateObjectClassHappyPath:

    def test_creates_working_composite_class(self):
        First = _int_const("First", default=2)
        Second = _int_const("Second", default=3)

        def logic(cls, first, second):
            return first + second

        Pair = create_object_class("Pair", inners=(First, Second), logic=logic)

        assert issubclass(Pair, SimpleObject)
        assert Pair.meta.default == 5
        assert Pair.meta.value_type is int

    def test_explicit_value_type_skips_default_inference(self):
        First = _int_const("First", default=2)

        def logic(cls, first):
            return first

        Single = create_object_class(
            "Single", inners=(First,), logic=logic, value_type=int
        )
        assert Single.meta.value_type is int


class TestCreateObjectClassLogicHandling:

    def test_lambda_logic_without_explicit_value_type_works(self):
        First = _int_const("First", default=2)
        Second = _int_const("Second", default=3)

        cls = create_object_class(
            class_name="LambdaComposite",
            inners=(First, Second),
            logic=lambda first, second: first + second,
        )

        assert cls._type is int

    def test_named_function_logic_without_explicit_value_type_works(self):
        First = _int_const("First", default=2)
        Second = _int_const("Second", default=3)

        def logic(cls, first, second):
            return first + second

        Pair = create_object_class("Pair", inners=(First, Second), logic=logic)
        assert Pair.meta.default == 5


class TestCreateObjectClassValidateAndDecompose:

    def test_lambda_validate_is_attached(self):
        First = _int_const("First", default=2)

        def logic(cls, first):
            return first

        Single = create_object_class(
            "Single",
            inners=(First,),
            logic=logic,
            value_type=int,
            validate=lambda value: value >= 0,
        )
        assert Single.is_valid(5) is True
        assert Single.is_valid(-5) is False

    def test_lambda_decompose_is_attached_and_normalized(self):
        First = _int_const("First", default=2)
        Second = _int_const("Second", default=0)

        def logic(cls, first, second):
            return first + second

        Pair = create_object_class(
            "Pair",
            inners=(First, Second),
            logic=logic,
            value_type=int,
            decompose=lambda value: (value, 0),
        )
        assert Pair.decompose_value(5) == (5, 0)


class TestCreateObjectClassValidation:

    def test_invalid_class_name_raises(self):
        First = _int_const("First")

        with pytest.raises(Exception):
            create_object_class("", inners=(First,), logic=lambda first: first)

    def test_missing_logic_raises(self):
        First = _int_const("First")

        with pytest.raises(Exception):
            create_object_class("Widget", inners=(First,), logic=UNSET)

    def test_missing_inners_raises(self):
        with pytest.raises(Exception):
            create_object_class("Widget", inners=UNSET, logic=lambda first: first)