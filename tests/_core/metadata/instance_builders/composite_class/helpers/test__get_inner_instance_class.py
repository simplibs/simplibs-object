"""
Tests for `_core/metadata/instance_builders/composite_class/helpers/_get_inner_instance_class.py`.
"""
from types import SimpleNamespace
from simplibs.object._core.metadata.instance_builders.composite_class.helpers._get_inner_instance_class import (
    _get_inner_instance_class,
)


class TestGetInnerInstanceClassConstant:

    def test_mutable_constant_returns_atom_class_mutable(self):
        meta = SimpleNamespace(
            is_constant=True,
            atom_class_mutable="ATOM_MUTABLE",
            atom_class_immutable="ATOM_IMMUTABLE",
            composite_class_mutable="COMPOSITE_MUTABLE",
            composite_class_immutable="COMPOSITE_IMMUTABLE",
        )
        assert _get_inner_instance_class(meta, mutable=True) == "ATOM_MUTABLE"

    def test_immutable_constant_returns_atom_class_immutable(self):
        meta = SimpleNamespace(
            is_constant=True,
            atom_class_mutable="ATOM_MUTABLE",
            atom_class_immutable="ATOM_IMMUTABLE",
            composite_class_mutable="COMPOSITE_MUTABLE",
            composite_class_immutable="COMPOSITE_IMMUTABLE",
        )
        assert _get_inner_instance_class(meta, mutable=False) == "ATOM_IMMUTABLE"


class TestGetInnerInstanceClassComposite:

    def test_mutable_composite_returns_composite_class_mutable(self):
        meta = SimpleNamespace(
            is_constant=False,
            atom_class_mutable="ATOM_MUTABLE",
            atom_class_immutable="ATOM_IMMUTABLE",
            composite_class_mutable="COMPOSITE_MUTABLE",
            composite_class_immutable="COMPOSITE_IMMUTABLE",
        )
        assert _get_inner_instance_class(meta, mutable=True) == "COMPOSITE_MUTABLE"

    def test_immutable_composite_returns_composite_class_immutable(self):
        meta = SimpleNamespace(
            is_constant=False,
            atom_class_mutable="ATOM_MUTABLE",
            atom_class_immutable="ATOM_IMMUTABLE",
            composite_class_mutable="COMPOSITE_MUTABLE",
            composite_class_immutable="COMPOSITE_IMMUTABLE",
        )
        assert _get_inner_instance_class(meta, mutable=False) == "COMPOSITE_IMMUTABLE"