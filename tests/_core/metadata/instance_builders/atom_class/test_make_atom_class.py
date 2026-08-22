"""
Tests for `_core/metadata/instance_builders/atom_class/make_atom_class.py`.
"""
import pytest
from simplibs.object._core.metadata.instance_builders.atom_class.make_atom_class import (
    make_atom_class,
)


def _instantiate_atom(atom_class):
    instance = object.__new__(atom_class)
    atom_class.__init__(instance)
    return instance


class TestMakeAtomClassMutable:

    def test_creates_functional_mutable_atom(self, IntConst):
        atom_class = make_atom_class(IntConst.meta, mutable=True)
        instance = _instantiate_atom(atom_class)

        assert instance.value == IntConst.meta.default
        instance.value = 99
        assert instance.value == 99

    def test_mutable_atom_has_root_value_setter(self, IntConst):
        atom_class = make_atom_class(IntConst.meta, mutable=True)
        assert "_root_value_setter" in atom_class.__dict__

    def test_mutable_atom_class_name_reflects_mutability(self, IntConst):
        atom_class = make_atom_class(IntConst.meta, mutable=True)
        assert atom_class.__name__ == "IntConstAtomMutableBase"


class TestMakeAtomClassImmutable:

    def test_creates_functional_immutable_atom(self, IntConst):
        atom_class = make_atom_class(IntConst.meta, mutable=False)
        instance = _instantiate_atom(atom_class)
        assert instance.value == IntConst.meta.default

    def test_immutable_atom_has_no_setter_attribute_and_read_only_value(self, IntConst):
        atom_class = make_atom_class(IntConst.meta, mutable=False)
        assert "_root_value_setter" not in atom_class.__dict__

        instance = _instantiate_atom(atom_class)
        with pytest.raises(AttributeError):
            instance.value = 5

    def test_immutable_atom_class_name_reflects_mutability(self, IntConst):
        atom_class = make_atom_class(IntConst.meta, mutable=False)
        assert atom_class.__name__ == "IntConstAtomImmutableBase"


class TestMakeAtomClassCleanup:

    def test_declarative_attributes_are_removed(self, IntConst):
        atom_class = make_atom_class(IntConst.meta, mutable=True)
        for name in ("_type", "_default", "_validate", "bool_or_raise_validate_error"):
            assert name not in atom_class.__dict__

    def test_inherited_declarative_attributes_from_owner_class_still_removed(
        self, PositiveIntConst
    ):
        atom_class = make_atom_class(PositiveIntConst.meta, mutable=True)
        assert "_validate" not in atom_class.__dict__


class TestMakeAtomClassSlots:

    def test_atom_class_defines_slots(self, IntConst):
        atom_class = make_atom_class(IntConst.meta, mutable=True)
        assert "__slots__" in atom_class.__dict__
        assert atom_class.__dict__["__slots__"] == ("_value", "_owner", "_locked")