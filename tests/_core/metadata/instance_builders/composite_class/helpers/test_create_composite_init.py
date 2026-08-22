"""
Tests for `_core/metadata/instance_builders/composite_class/helpers/create_composite_init.py`.
"""
import pytest
from simplibs.object._core.metadata.instance_builders.composite_class.helpers.create_composite_init import (
    create_composite_init,
)


class TestCreateCompositeInit:

    @pytest.mark.parametrize("is_mutable", [True, False])
    def test_initializes_atom_base_and_all_inners(
        self, NonDecomposablePairObject, is_mutable: bool
    ):
        meta = NonDecomposablePairObject.meta
        init = create_composite_init(meta, "FakeComposite", mutable=is_mutable)

        atom_base = (
            meta.atom_class_mutable if is_mutable else meta.atom_class_immutable
        )

        class FakeComposite(atom_base):
            __slots__ = tuple(inner.meta.name_private for inner in meta.inners)

        FakeComposite.__init__ = init

        # Direct instantiation bypassing SimpleMeta.__call__
        instance = object.__new__(FakeComposite)
        FakeComposite.__init__(instance)

        assert instance._value == meta.default
        for inner in meta.inners:
            inner_instance = getattr(instance, inner.meta.name_private)
            assert inner_instance.value == inner.meta.default
            assert inner_instance._owner is instance

    def test_reflection_alignment(self, NonDecomposablePairObject):
        meta = NonDecomposablePairObject.meta
        init = create_composite_init(meta, "FakeComposite", mutable=True)
        assert init.__name__ == "__init__"
        assert init.__qualname__ == "FakeComposite.__init__"
        assert init.__annotations__ == {"return": None}