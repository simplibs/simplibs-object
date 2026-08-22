"""
Tests for `_core/logic/property_builders/value_helpers/create_value_getter.py`.

Low-level unit tests verifying getter construction on lightweight test doubles,
covering root and inner property access paths.
"""
from types import SimpleNamespace
import pytest
from simplibs.object._core.logic.property_builders.value_helpers.create_value_getter import (
    create_value_getter,
)


class TestCreateValueGetterRootPath:

    def test_root_getter_reads_value_attribute(self) -> None:
        """Verifies root getter extracts the `_value` attribute from the instance."""
        meta = SimpleNamespace(value_type=int)
        getter = create_value_getter(meta, path=None)

        fake_instance = SimpleNamespace(_value=42)
        assert getter(fake_instance) == 42

    def test_root_getter_annotation_uses_meta_value_type(self) -> None:
        """Verifies return type annotation matches metadata `value_type`."""
        meta = SimpleNamespace(value_type=str)
        getter = create_value_getter(meta, path=None)
        assert getter.__annotations__ == {"return": str}


class TestCreateValueGetterInnerPath:

    def test_inner_getter_resolves_nested_instance_value(self) -> None:
        """Verifies inner getter traverses one path segment to read nested `.value`."""
        meta = SimpleNamespace(value_type=int)
        getter = create_value_getter(meta, path=("_first",))

        inner_instance = SimpleNamespace(value=7)
        owner_instance = SimpleNamespace(_first=inner_instance)

        assert getter(owner_instance) == 7

    def test_multi_element_path_does_not_chain_attributes_bug_note(self) -> None:
        """
        Documenting current behavior: `attrgetter(*path)` with multiple elements returns a tuple
        instead of chained attribute access, causing AttributeError on `.value`.
        """
        meta = SimpleNamespace(value_type=int)
        getter = create_value_getter(meta, path=("_a", "_b"))

        top = SimpleNamespace(_a=1, _b=2)
        with pytest.raises(AttributeError):
            getter(top)