"""
Tests for `_core/metadata/instance_builders/composite_class/helpers/create_recalculate_inners.py`.
"""
from types import SimpleNamespace
from simplibs.object._core.metadata.instance_builders.composite_class.helpers.create_recalculate_inners import (
    create_recalculate_inners,
)


def _make_fake_composite(decomposed_values, inner_is_constant_map):
    inner_metas = []
    inner_calls = {}

    class Fake:
        pass

    fake = Fake()
    fake._value = "composite-value"
    fake.decompose_value = lambda value: decomposed_values

    for name, is_constant in inner_is_constant_map.items():
        private = f"_{name}"
        calls = {"root_value_setter": None, "recalculate_inners": False}
        inner_calls[name] = calls

        def _root_value_setter(value, recalculate_up=True, _calls=calls):
            _calls["root_value_setter"] = (value, recalculate_up)

        def _recalculate_inners(_calls=calls):
            _calls["recalculate_inners"] = True

        inner_instance = SimpleNamespace(
            _root_value_setter=_root_value_setter,
            _recalculate_inners=_recalculate_inners,
        )
        setattr(fake, private, inner_instance)
        inner_metas.append(
            SimpleNamespace(
                meta=SimpleNamespace(
                    name_snake=name, name_private=private, is_constant=is_constant
                )
            )
        )

    meta = SimpleNamespace(inners=tuple(inner_metas))
    return fake, meta, inner_calls


class TestCreateRecalculateInnersPushesValuesDown:

    def test_writes_decomposed_value_into_each_inner_without_bubbling_up(self):
        fake, meta, calls = _make_fake_composite(
            (2, 3), {"first": True, "second": True}
        )
        recalc = create_recalculate_inners(meta, "FakeComposite")

        recalc(fake)

        assert calls["first"]["root_value_setter"] == (2, False)
        assert calls["second"]["root_value_setter"] == (3, False)


class TestCreateRecalculateInnersCascade:

    def test_constant_inner_does_not_cascade(self):
        fake, meta, calls = _make_fake_composite(
            (2, 3), {"first": True, "second": True}
        )
        recalc = create_recalculate_inners(meta, "FakeComposite")

        recalc(fake)

        assert calls["first"]["recalculate_inners"] is False
        assert calls["second"]["recalculate_inners"] is False

    def test_composite_inner_cascades_recalculate_inners(self):
        fake, meta, calls = _make_fake_composite(
            (2, 3), {"first": False, "second": True}
        )
        recalc = create_recalculate_inners(meta, "FakeComposite")

        recalc(fake)

        assert calls["first"]["recalculate_inners"] is True
        assert calls["second"]["recalculate_inners"] is False


class TestCreateRecalculateInnersReflection:

    def test_reflection_alignment(self):
        _, meta, _ = _make_fake_composite((1,), {"first": True})
        recalc = create_recalculate_inners(meta, "FakeComposite")
        assert recalc.__name__ == "_recalculate_inners"
        assert recalc.__qualname__ == "FakeComposite._recalculate_inners"