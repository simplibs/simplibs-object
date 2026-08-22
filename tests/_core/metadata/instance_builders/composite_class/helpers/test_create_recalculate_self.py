"""
Tests for `_core/metadata/instance_builders/composite_class/helpers/create_recalculate_self.py`.
"""
from types import SimpleNamespace
from simplibs.object._core.metadata.instance_builders.composite_class.helpers.create_recalculate_self import (
    create_recalculate_self,
)


def _make_fake_inner(name_snake, name_private, value):
    return SimpleNamespace(
        meta=SimpleNamespace(name_snake=name_snake, name_private=name_private),
    ), SimpleNamespace(value=value)


def _make_fake_composite(inner_values: dict, current_value, owner=None, new_value=None):
    inner_metas = []
    calls = {"recalculate_self_on_owner": False}

    class Fake:
        pass

    fake = Fake()
    fake._value = current_value
    fake._owner = owner

    for name, value in inner_values.items():
        private = f"_{name}"
        inner_meta_obj = SimpleNamespace(name_snake=name, name_private=private)
        inner_instance = SimpleNamespace(value=value)
        setattr(fake, private, inner_instance)
        inner_metas.append(SimpleNamespace(meta=inner_meta_obj))

    def calculate_value(**kwargs):
        return new_value if new_value is not None else sum(kwargs.values())

    fake.calculate_value = calculate_value

    if owner is not None:
        def _recalculate_self_on_owner():
            calls["recalculate_self_on_owner"] = True
        owner._recalculate_self = _recalculate_self_on_owner

    meta = SimpleNamespace(inners=tuple(inner_metas))
    return fake, meta, calls


class TestCreateRecalculateSelfBasic:

    def test_recomputes_value_from_current_inner_values(self):
        fake, meta, _ = _make_fake_composite({"first": 2, "second": 3}, current_value=0)
        recalc = create_recalculate_self(meta, "FakeComposite")

        recalc(fake)
        assert fake._value == 5


class TestCreateRecalculateSelfShortCircuit:

    def test_unchanged_value_does_not_bubble_up(self):
        owner = SimpleNamespace()
        fake, meta, calls = _make_fake_composite(
            {"first": 2, "second": 3}, current_value=5, owner=owner
        )
        recalc = create_recalculate_self(meta, "FakeComposite")

        recalc(fake)
        assert calls["recalculate_self_on_owner"] is False

    def test_comparison_exception_is_swallowed_and_treated_as_changed(self):
        class Unorderable:
            def __eq__(self, other):
                raise TypeError("cannot compare")

        fake, meta, _ = _make_fake_composite(
            {"first": 2, "second": 3}, current_value=Unorderable()
        )
        recalc = create_recalculate_self(meta, "FakeComposite")

        recalc(fake)
        assert fake._value == 5


class TestCreateRecalculateSelfBubbling:

    def test_changed_value_bubbles_up_to_owner(self):
        owner = SimpleNamespace()
        fake, meta, calls = _make_fake_composite(
            {"first": 2, "second": 3}, current_value=0, owner=owner
        )
        recalc = create_recalculate_self(meta, "FakeComposite")

        recalc(fake)
        assert calls["recalculate_self_on_owner"] is True

    def test_no_owner_does_not_raise(self):
        fake, meta, _ = _make_fake_composite({"first": 2}, current_value=0, owner=None)
        recalc = create_recalculate_self(meta, "FakeComposite")

        recalc(fake)
        assert fake._value == 2


class TestCreateRecalculateSelfReflection:

    def test_reflection_alignment(self):
        _, meta, _ = _make_fake_composite({"first": 1}, current_value=0)
        recalc = create_recalculate_self(meta, "FakeComposite")
        assert recalc.__name__ == "_recalculate_self"
        assert recalc.__qualname__ == "FakeComposite._recalculate_self"