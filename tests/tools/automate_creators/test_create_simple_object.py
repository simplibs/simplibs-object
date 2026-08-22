"""
Tests for `tools/automate_creators/create_simple_object.py`.

Verifies routing logic based on presence of `inners` and proper forwarding
of parameters like `return_instance`, `mixins`, and `mutable`.
"""
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.tools.automate_creators.create_simple_object import (
    create_simple_object,
)


def _int_const(name, default=0):
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


class TestCreateSimpleObjectConstantRouting:

    def test_no_inners_routes_to_constant_class(self):
        Age = create_simple_object("Age", default=18)
        assert issubclass(Age, SimpleConstant)
        assert not issubclass(Age, SimpleObject)
        assert Age.meta.default == 18

    def test_return_instance_true_returns_instance_not_class(self):
        age_instance = create_simple_object("Age", default=18, return_instance=True)
        assert age_instance.value == 18

    def test_return_instance_false_returns_class(self):
        Age = create_simple_object("Age", default=18, return_instance=False)
        assert isinstance(Age, type)

    def test_mutable_flag_is_forwarded_to_instance(self):
        age_instance = create_simple_object(
            "Age", default=18, return_instance=True, mutable=False
        )
        with pytest.raises(AttributeError):
            age_instance.value = 99


class TestCreateSimpleObjectObjectRouting:

    def test_inners_routes_to_object_class(self):
        First = _int_const("First", default=2)
        Second = _int_const("Second", default=3)

        def logic(cls, first, second):
            return first + second

        Pair = create_simple_object(
            "Pair", inners=(First, Second), logic=logic, value_type=int
        )
        assert issubclass(Pair, SimpleObject)
        assert Pair.meta.default == 5