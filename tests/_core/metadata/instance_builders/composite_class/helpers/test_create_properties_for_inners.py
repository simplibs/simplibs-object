"""
Tests for `_core/metadata/instance_builders/composite_class/helpers/create_properties_for_inners.py`.
"""
from simplibs.object._core.metadata.instance_builders.composite_class.helpers.create_properties_for_inners import (
    create_properties_for_inners,
)


class TestCreatePropertiesForInnersKeys:

    def test_returns_value_and_instance_keys_for_every_inner(
        self, NonDecomposablePairObject
    ):
        result = create_properties_for_inners(
            NonDecomposablePairObject.meta, mutable=True
        )
        assert set(result.keys()) == {
            "first",
            "first_instance",
            "second",
            "second_instance",
        }


class TestCreatePropertiesForInnersMutability:

    def test_mutable_true_gives_settable_value_properties(
        self, NonDecomposablePairObject
    ):
        result = create_properties_for_inners(
            NonDecomposablePairObject.meta, mutable=True
        )
        assert result["first"].fset is not None
        assert result["second"].fset is not None

    def test_mutable_false_gives_read_only_value_properties(
        self, NonDecomposablePairObject
    ):
        result = create_properties_for_inners(
            NonDecomposablePairObject.meta, mutable=False
        )
        assert result["first"].fset is None
        assert result["second"].fset is None