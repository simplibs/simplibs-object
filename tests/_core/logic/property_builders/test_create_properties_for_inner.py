"""
Tests for `_core/logic/property_builders/create_properties_for_inner.py`.

Verifies dictionary assembly of value and instance properties for child nodes.
"""
from simplibs.object._core.logic.property_builders.create_properties_for_inner import (
    create_properties_for_inner,
)


class TestCreatePropertiesForInnerKeys:

    def test_returns_value_and_instance_property_keys(self, PairObject) -> None:
        """Verifies exact property dictionary keys: `<name>` and `<name>_instance`."""
        inner_meta = PairObject.meta.inners[0].meta
        result = create_properties_for_inner(inner_meta, path=("_first",))

        assert set(result.keys()) == {"first", "first_instance"}

    def test_value_property_is_property_instance(self, PairObject) -> None:
        """Verifies primary value property descriptor instance type."""
        inner_meta = PairObject.meta.inners[0].meta
        result = create_properties_for_inner(inner_meta, path=("_first",))
        assert isinstance(result["first"], property)

    def test_instance_property_is_property_instance(self, PairObject) -> None:
        """Verifies instance property descriptor instance type."""
        inner_meta = PairObject.meta.inners[0].meta
        result = create_properties_for_inner(inner_meta, path=("_first",))
        assert isinstance(result["first_instance"], property)


class TestCreatePropertiesForInnerMutability:

    def test_mutable_true_produces_property_with_setter(self, PairObject) -> None:
        """Verifies mutable=True attaches setter to value property descriptor."""
        inner_meta = PairObject.meta.inners[0].meta
        result = create_properties_for_inner(inner_meta, path=("_first",), mutable=True)
        assert result["first"].fset is not None

    def test_mutable_false_produces_getter_only_property(self, PairObject) -> None:
        """Verifies mutable=False yields getter-only value property descriptor."""
        inner_meta = PairObject.meta.inners[0].meta
        result = create_properties_for_inner(inner_meta, path=("_first",), mutable=False)
        assert result["first"].fset is None

    def test_instance_property_is_always_read_only_regardless_of_mutable(self, PairObject) -> None:
        """Verifies instance property descriptor remains read-only regardless of mutability mode."""
        inner_meta = PairObject.meta.inners[0].meta
        result = create_properties_for_inner(inner_meta, path=("_first",), mutable=True)
        assert result["first_instance"].fset is None