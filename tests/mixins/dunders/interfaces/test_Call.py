"""
Tests for `Call` mixin.
"""
import pytest
from simplibs.object.mixins.core_mixins import Infrastructure
from simplibs.object.mixins.dunders.interfaces import Call
from simplibs.object.testing import assert_simple_mixin


class TestCallStructure:

    def test_inherits_from_infrastructure(self):
        assert issubclass(Call, Infrastructure)

    def test_slots_empty(self):
        assert Call.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            Call,
            test_class=Outer,
            method_names=("__call__",),
        )


class TestCallSingleChangeForms:

    def test_call_with_two_positional_args(self, Outer):
        instance = Outer(mixins=(Call,), mutable=False)
        result = instance("third", 42)
        assert result._nodes_dict["third"][0].value == 42

    def test_call_with_single_tuple_arg(self, Outer):
        instance = Outer(mixins=(Call,), mutable=False)
        result = instance(("third", 42))
        assert result._nodes_dict["third"][0].value == 42


class TestCallMultipleChangesForm:

    def test_call_with_tuple_of_tuples(self, Outer):
        instance = Outer(mixins=(Call,), mutable=False)
        result = instance((("first", 10), ("third", 20)))
        assert result._nodes_dict["first"][0].value == 10
        assert result._nodes_dict["third"][0].value == 20

    def test_call_with_multiple_tuple_positional_args(self, Outer):
        instance = Outer(mixins=(Call,), mutable=False)
        result = instance(("first", 10), ("third", 20))
        assert result._nodes_dict["first"][0].value == 10
        assert result._nodes_dict["third"][0].value == 20


class TestCallKwargsForm:

    def test_call_with_kwargs(self, Outer):
        instance = Outer(mixins=(Call,), mutable=False)
        result = instance(third=42)
        assert result._nodes_dict["third"][0].value == 42

    def test_call_kwargs_override_positional(self, Outer):
        instance = Outer(mixins=(Call,), mutable=False)
        result = instance(("first", 999), third=42)
        assert result._nodes_dict["third"][0].value == 42
        assert result._nodes_dict["first"][0].value != 999


class TestCallNoArgs:

    def test_call_with_no_args_returns_equivalent_instance(self, Outer):
        instance = Outer(mixins=(Call,), mutable=False)
        result = instance()
        assert result.value == instance.value