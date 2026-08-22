"""
Tests for `_core/logic/property_builders/create_value_property.py`.

Verifies getter/setter building and contextual docstrings across constant/composite models.
"""
from types import SimpleNamespace
from simplibs.object._core.logic.property_builders.create_value_property import (
    create_value_property,
)


class TestCreateValuePropertyImmutable:

    def test_immutable_returns_getter_only(self) -> None:
        """Verifies mutable=False produces property descriptor without setter."""
        meta = SimpleNamespace(value_type=int, value_type_name="int", is_decomposeable=True)
        prop = create_value_property(meta, is_constant=True, mutable=False)
        assert prop.fget is not None
        assert prop.fset is None


class TestCreateValuePropertyMutable:

    def test_mutable_constant_returns_getter_and_setter(self) -> None:
        """Verifies mutable constant produces complete getter/setter property."""
        meta = SimpleNamespace(value_type=int, value_type_name="int", is_decomposeable=True)
        prop = create_value_property(meta, is_constant=True, mutable=True)
        assert prop.fget is not None
        assert prop.fset is not None

    def test_mutable_composite_returns_getter_and_setter(self) -> None:
        """Verifies mutable composite produces complete getter/setter property."""
        meta = SimpleNamespace(value_type=int, value_type_name="int", is_decomposeable=True)
        prop = create_value_property(meta, is_constant=False, mutable=True)
        assert prop.fget is not None
        assert prop.fset is not None


class TestCreateValuePropertyDocstring:

    def test_constant_docstring_mentions_normalization(self) -> None:
        """Verifies constant property docstring details value normalization."""
        meta = SimpleNamespace(value_type=int, value_type_name="int", is_decomposeable=True)
        prop = create_value_property(meta, is_constant=True, mutable=True)
        assert "normaliz" in prop.__doc__.lower()

    def test_composite_docstring_mentions_decomposition(self) -> None:
        """Verifies composite property docstring details value decomposition."""
        meta = SimpleNamespace(value_type=int, value_type_name="int", is_decomposeable=True)
        prop = create_value_property(meta, is_constant=False, mutable=True)
        assert "dekompon" in prop.__doc__.lower()

    def test_value_type_name_appears_in_docstring(self) -> None:
        """Verifies metadata value_type_name is injected into property docstring."""
        meta = SimpleNamespace(value_type=int, value_type_name="int", is_decomposeable=True)
        prop = create_value_property(meta, is_constant=True, mutable=True)
        assert "int" in prop.__doc__


class TestCreateValuePropertyRealIntegration:

    def test_property_works_on_real_atom_instance(self, IntConst) -> None:
        """Sanity check verifying read and write behavior on a live atomic instance."""
        instance = IntConst()
        assert instance.value == IntConst.meta.default
        instance.value = 99
        assert instance.value == 99