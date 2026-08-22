"""
Tests for `_core/logic/property_builders/create_instance_property.py`.

Verifies read-only `<name>_instance` property access and attributes.
"""
import pytest
from simplibs.object._core.logic.property_builders.create_instance_property import (
    create_instance_property,
)


class TestCreateInstancePropertyReadOnly:

    def test_getter_returns_inner_instance(self, PairObject) -> None:
        """Verifies property getter extracts the inner object instance."""
        pair = PairObject()
        prop = create_instance_property(PairObject.meta.inners[0].meta, ("_first",))

        class Holder:
            pass

        Holder._first = pair._first
        holder = Holder()
        assert prop.fget(holder) is pair._first

    def test_property_has_no_setter(self, PairObject) -> None:
        """Verifies instance property is strictly read-only (fset is None)."""
        prop = create_instance_property(PairObject.meta.inners[0].meta, ("_first",))
        assert prop.fset is None

    def test_property_docstring_mentions_inner_name(self, PairObject) -> None:
        """Verifies generated docstring references the inner variable name."""
        inner_meta = PairObject.meta.inners[0].meta
        prop = create_instance_property(inner_meta, ("_first",))
        assert inner_meta.name_snake in prop.__doc__


class TestCreateInstancePropertyViaRealComposite:

    def test_instance_property_accessible_on_real_composite(self, PairObject) -> None:
        """Verifies generated property slots link to nested inner instances."""
        pair = PairObject()
        assert pair.first_instance is pair._first
        assert pair.second_instance is pair._second

    def test_instance_property_cannot_be_assigned(self, PairObject) -> None:
        """Verifies attempting to mutate instance property raises AttributeError."""
        pair = PairObject()
        with pytest.raises(AttributeError):
            pair.first_instance = None