"""
Tests for `SimpleObject.py`.

Public methods are thin wrappers around `_core/logic/object_methods/*`.
These tests verify correct delegation to internal functions.
"""
import pytest
from simplibs.object import SimpleObject
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.sentinels import UNSET


class TestSimpleObjectCalculateValueDelegation:

    def test_calculate_value_delegates_correctly(self, NonDecomposablePairObject):
        assert NonDecomposablePairObject.calculate_value(2, 3) == 5

    def test_calculate_value_propagates_param_errors(self, NonDecomposablePairObject):
        with pytest.raises(SimpleRuntimeError):
            NonDecomposablePairObject.calculate_value(unknown=1)


class TestSimpleObjectDecomposeValueDelegation:

    def test_decompose_value_raises_when_not_decomposeable(self, NonDecomposablePairObject):
        with pytest.raises(SimpleRuntimeError):
            NonDecomposablePairObject.decompose_value(5)


class TestSimpleObjectDefaultHooks:

    def test_default_logic_returns_unset_and_is_never_used_directly(self):
        """`SimpleObject._logic` directly on the base class returns UNSET.
        This sentinel indicates the user has not overridden the method.
        """
        assert SimpleObject._logic() is UNSET

    def test_default_decompose_returns_unset(self):
        assert SimpleObject._decompose(None) is UNSET

    def test_default_validate_returns_true(self):
        assert SimpleObject._validate(None) is True