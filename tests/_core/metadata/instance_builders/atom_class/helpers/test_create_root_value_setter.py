"""
Tests for `_core/metadata/instance_builders/atom_class/helpers/create_root_value_setter.py`.
"""
from types import SimpleNamespace
from simplibs.object._core.metadata.instance_builders.atom_class.helpers.create_root_value_setter import (
    create_root_value_setter,
)
from simplibs.sentinels import UNSET


def _make_fake_self(current_value, owner=UNSET):
    calls = {"recalculate_self": False}

    def _recalculate_self():
        calls["recalculate_self"] = True

    owner_obj = None
    if owner is not UNSET:
        owner_obj = SimpleNamespace(_recalculate_self=_recalculate_self)

    fake = SimpleNamespace(
        _value=current_value,
        _owner=owner_obj if owner_obj is not None else UNSET,
        normalize=lambda value, process_none=True: value,
    )
    return fake, calls


class TestCreateRootValueSetterBasicAssignment:

    def test_assigns_new_normalized_value(self):
        setter = create_root_value_setter("FakeAtom")
        fake, _ = _make_fake_self(current_value=1)

        setter(fake, 5)
        assert fake._value == 5

    def test_uses_normalize_from_self(self):
        setter = create_root_value_setter("FakeAtom")
        fake, _ = _make_fake_self(current_value=1)
        fake.normalize = lambda value, process_none=True: value * 100

        setter(fake, 5)
        assert fake._value == 500


class TestCreateRootValueSetterShortCircuit:

    def test_unchanged_value_does_not_reassign_or_bubble(self):
        setter = create_root_value_setter("FakeAtom")
        fake, calls = _make_fake_self(current_value=5, owner="present")

        setter(fake, 5)
        assert calls["recalculate_self"] is False


class TestCreateRootValueSetterBubbling:

    def test_owner_recalculate_self_called_when_owner_present(self):
        setter = create_root_value_setter("FakeAtom")
        fake, calls = _make_fake_self(current_value=1, owner="present")

        setter(fake, 9)
        assert calls["recalculate_self"] is True

    def test_no_owner_does_not_raise(self):
        setter = create_root_value_setter("FakeAtom")
        fake, _ = _make_fake_self(current_value=1, owner=UNSET)

        setter(fake, 9)
        assert fake._value == 9

    def test_recalculate_up_false_skips_bubbling(self):
        setter = create_root_value_setter("FakeAtom")
        fake, calls = _make_fake_self(current_value=1, owner="present")

        setter(fake, 9, recalculate_up=False)
        assert calls["recalculate_self"] is False


class TestCreateRootValueSetterReflection:

    def test_reflection_alignment(self):
        setter = create_root_value_setter("FakeAtom")
        assert setter.__name__ == "_root_value_setter"
        assert setter.__qualname__ == "FakeAtom._root_value_setter"