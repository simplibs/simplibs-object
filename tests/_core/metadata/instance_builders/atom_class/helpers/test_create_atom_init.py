"""
Tests for `_core/metadata/instance_builders/atom_class/helpers/create_atom_init.py`.
"""
from types import SimpleNamespace
from simplibs.object._core.metadata.instance_builders.atom_class.helpers.create_atom_init import (
    create_atom_init,
)
from simplibs.sentinels import UNSET


class FakeAtomInstance:
    """Mock class providing the base methods required by an atomic instance."""
    def init_mixins(self) -> None:
        pass


class TestCreateAtomInit:

    def test_sets_value_to_meta_default(self):
        meta = SimpleNamespace(default=42)
        init = create_atom_init(meta, "FakeAtom")

        instance = FakeAtomInstance()
        init(instance)
        assert instance._value == 42

    def test_sets_owner_to_unset(self):
        meta = SimpleNamespace(default=0)
        init = create_atom_init(meta, "FakeAtom")

        instance = FakeAtomInstance()
        init(instance)
        assert instance._owner is UNSET

    def test_sets_locked_to_false(self):
        meta = SimpleNamespace(default=0)
        init = create_atom_init(meta, "FakeAtom")

        instance = FakeAtomInstance()
        init(instance)
        assert instance._locked is False

    def test_calls_init_mixins(self):
        meta = SimpleNamespace(default=0)
        init = create_atom_init(meta, "FakeAtom")

        calls = []

        class CustomFake(FakeAtomInstance):
            def init_mixins(self):
                calls.append(True)

        instance = CustomFake()
        init(instance)
        assert calls == [True]

    def test_reflection_alignment(self):
        meta = SimpleNamespace(default=0)
        init = create_atom_init(meta, "FakeAtom")

        assert init.__name__ == "__init__"
        assert init.__qualname__ == "FakeAtom.__init__"
        assert init.__annotations__ == {"return": None}