"""
Tests for `_core/metadata/instance_builders/instance/helpers/get_base_class.py`.
"""
from types import SimpleNamespace
from simplibs.object._core.metadata.instance_builders.instance.helpers.get_base_class import (
    get_base_class,
)


def _make_fake_cls():
    meta = SimpleNamespace(
        atom_class_mutable="ATOM_MUTABLE",
        atom_class_immutable="ATOM_IMMUTABLE",
        composite_class_mutable="COMPOSITE_MUTABLE",
        composite_class_immutable="COMPOSITE_IMMUTABLE",
    )
    return SimpleNamespace(meta=meta)


class TestGetBaseClassAtom:

    def test_atom_mutable(self):
        cls = _make_fake_cls()
        assert get_base_class(cls, is_atom=True, mutable=True) == "ATOM_MUTABLE"

    def test_atom_immutable(self):
        cls = _make_fake_cls()
        assert get_base_class(cls, is_atom=True, mutable=False) == "ATOM_IMMUTABLE"


class TestGetBaseClassComposite:

    def test_composite_mutable(self):
        cls = _make_fake_cls()
        assert get_base_class(cls, is_atom=False, mutable=True) == "COMPOSITE_MUTABLE"

    def test_composite_immutable(self):
        cls = _make_fake_cls()
        assert get_base_class(cls, is_atom=False, mutable=False) == "COMPOSITE_IMMUTABLE"