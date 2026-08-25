"""
Tests for `_core/metadata/instance_builders/composite_class/make_composite_class.py`.
"""
import pytest
from simplibs.object._core.metadata.instance_builders.composite_class.make_composite_class import (
    make_composite_class,
)


def _instantiate(cls):
    instance = object.__new__(cls)
    instance.__init__()
    return instance


class TestMakeCompositeClassMutable:

    def test_creates_functional_mutable_composite(self, NonDecomposablePairObject):
        composite_class = make_composite_class(
            NonDecomposablePairObject.meta, mutable=True
        )
        instance = _instantiate(composite_class)

        assert instance.value == NonDecomposablePairObject.meta.default
        assert instance.first == NonDecomposablePairObject.meta.inners[0].meta.default
        assert instance.second == NonDecomposablePairObject.meta.inners[1].meta.default

    def test_mutable_composite_has_reactive_hooks(self, NonDecomposablePairObject):
        composite_class = make_composite_class(
            NonDecomposablePairObject.meta, mutable=True
        )
        assert "_recalculate_self" in composite_class.__dict__
        assert "_recalculate_inners" in composite_class.__dict__

    def test_changing_inner_recalculates_composite_value(
        self, NonDecomposablePairObject
    ):
        composite_class = make_composite_class(
            NonDecomposablePairObject.meta, mutable=True
        )
        instance = _instantiate(composite_class)

        instance.first = 10
        assert (
            instance.value == 10 + NonDecomposablePairObject.meta.inners[1].meta.default
        )


class TestMakeCompositeClassImmutable:

    def test_creates_functional_immutable_composite(self, NonDecomposablePairObject):
        composite_class = make_composite_class(
            NonDecomposablePairObject.meta, mutable=False
        )
        instance = _instantiate(composite_class)
        assert instance.value == NonDecomposablePairObject.meta.default

    def test_immutable_composite_has_no_reactive_hooks(self, NonDecomposablePairObject):
        composite_class = make_composite_class(
            NonDecomposablePairObject.meta, mutable=False
        )
        assert "_recalculate_self" not in composite_class.__dict__
        assert "_recalculate_inners" not in composite_class.__dict__

    def test_immutable_composite_inner_value_is_read_only(
        self, NonDecomposablePairObject
    ):
        composite_class = make_composite_class(
            NonDecomposablePairObject.meta, mutable=False
        )
        instance = _instantiate(composite_class)
        with pytest.raises(AttributeError):
            instance.first = 5


class TestMakeCompositeClassSlots:

    def test_slots_match_inner_private_names(self, NonDecomposablePairObject):
        composite_class = make_composite_class(
            NonDecomposablePairObject.meta, mutable=True
        )
        assert composite_class.__slots__ == tuple(
            inner.meta.name_private for inner in NonDecomposablePairObject.meta.inners
        )


class TestMakeCompositeClassNoLeakedDeclarativeAttrs:

    def test_declarative_attributes_are_removed(self, NonDecomposablePairObject):
        composite_class = make_composite_class(
            NonDecomposablePairObject.meta, mutable=True
        )
        for name in ("inners", "_logic", "_decompose"):
            assert name not in composite_class.__dict__