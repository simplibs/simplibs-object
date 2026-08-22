"""
Tests for `tools/automate_creators/bulk/BulkCase.py`.
"""
import pytest
from simplibs.object import SimpleConstant
from simplibs.object.tools.automate_creators.bulk.BulkCase import BulkCase


def _int_const(name, default=0):
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


class TestBulkCaseConstantValidation:

    def test_valid_constant_case_is_accepted(self):
        case = BulkCase(class_name="Age", default=18)
        assert case.class_name == "Age"
        assert case.default == 18

    def test_constant_with_logic_raises(self):
        with pytest.raises(Exception):
            BulkCase(class_name="Age", default=18, logic=lambda first: first)

    def test_constant_with_decompose_raises(self):
        with pytest.raises(Exception):
            BulkCase(class_name="Age", default=18, decompose=lambda value: (value,))

    def test_constant_missing_default_raises(self):
        with pytest.raises(Exception):
            BulkCase(class_name="Age")

    def test_invalid_class_name_raises(self):
        with pytest.raises(Exception):
            BulkCase(class_name="", default=18)


class TestBulkCaseCompositeValidation:

    def test_valid_composite_case_is_accepted(self):
        First = _int_const("First")
        case = BulkCase(
            class_name="Pair", inners=(First,), logic=lambda cls, first: first
        )
        assert case.inners == (First,)

    def test_composite_missing_logic_raises(self):
        First = _int_const("First")
        with pytest.raises(Exception):
            BulkCase(class_name="Pair", inners=(First,))

    def test_composite_with_default_raises(self):
        First = _int_const("First")
        with pytest.raises(Exception):
            BulkCase(
                class_name="Pair",
                inners=(First,),
                logic=lambda cls, first: first,
                default=5,
            )


class TestBulkCaseDefaults:

    def test_default_mixins_is_empty_tuple(self):
        case = BulkCase(class_name="Age", default=18)
        assert case.mixins == ()

    def test_default_return_instance_is_false(self):
        case = BulkCase(class_name="Age", default=18)
        assert case.return_instance is False

    def test_default_mutable_is_true(self):
        case = BulkCase(class_name="Age", default=18)
        assert case.mutable is True


class TestBulkCaseCreateSimpleObject:

    def test_create_simple_object_returns_working_constant_class(self):
        case = BulkCase(class_name="Age", default=18)
        Age = case.create_simple_object()
        assert Age.meta.default == 18

    def test_create_simple_object_respects_return_instance(self):
        case = BulkCase(class_name="Age", default=18, return_instance=True)
        instance = case.create_simple_object()
        assert instance.value == 18

    def test_create_simple_object_composite(self):
        First = _int_const("First", default=2)
        case = BulkCase(
            class_name="Pair",
            inners=(First,),
            logic=lambda first: first,
        )
        Pair = case.create_simple_object()

        assert Pair.meta.class_name == "Pair"
        assert Pair.meta.inners == (First,)