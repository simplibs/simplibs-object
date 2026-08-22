"""
Tests for `_core/metadata/init_processors/methods/verifiers/calculation/decompose_method/verify_decompose_outcome.py`.
"""
import pytest
from simplibs.object._core.metadata.init_processors.methods.verifiers.calculation.decompose_method.verify_decompose_outcome import (
    verify_decompose_outcome,
)
from simplibs.object.exceptions import SimpleDefinitionError


class TestVerifyDecomposeOutcomeHappyPath:

    def test_correct_length_and_types_does_not_raise(self, NonDecomposablePairObject):
        owner_class = NonDecomposablePairObject
        bound_method = owner_class.meta.logic

        verify_decompose_outcome((5, 0), owner_class, bound_method)

    def test_values_equal_to_inner_defaults_are_accepted_regardless_of_type(
        self, NonDecomposablePairObject
    ):
        owner_class = NonDecomposablePairObject
        bound_method = owner_class.meta.logic
        defaults = tuple(inner.meta.default for inner in owner_class.meta.inners)

        verify_decompose_outcome(defaults, owner_class, bound_method)


class TestVerifyDecomposeOutcomeWrongLength:

    def test_too_few_items_raises(self, NonDecomposablePairObject):
        owner_class = NonDecomposablePairObject
        bound_method = owner_class.meta.logic

        with pytest.raises(SimpleDefinitionError):
            verify_decompose_outcome((5,), owner_class, bound_method)

    def test_too_many_items_raises(self, NonDecomposablePairObject):
        owner_class = NonDecomposablePairObject
        bound_method = owner_class.meta.logic

        with pytest.raises(SimpleDefinitionError):
            verify_decompose_outcome((5, 0, 1), owner_class, bound_method)


class TestVerifyDecomposeOutcomeWrongItemType:

    def test_wrong_type_item_not_matching_default_raises(self, NonDecomposablePairObject):
        owner_class = NonDecomposablePairObject
        bound_method = owner_class.meta.logic

        with pytest.raises(SimpleDefinitionError):
            verify_decompose_outcome(("not-an-int", 0), owner_class, bound_method)

    def test_invalid_bound_method_format_fails_safely_with_exception(self, NonDecomposablePairObject):
        owner_class = NonDecomposablePairObject
        invalid_bound_method = "not_a_method"

        with pytest.raises(SimpleDefinitionError) as exc_info:
            verify_decompose_outcome((5,), owner_class, invalid_bound_method)

        assert "<UnknownClass>" in str(exc_info.value)