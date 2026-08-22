"""
Tests for `_core/metadata/instance_builders/instance/helpers/_verify_mixin_compatibility.py`.
"""
from unittest.mock import MagicMock
import pytest
from simplibs.sentinels import UNSET
from simplibs.object.mixins.base_class import SimpleMixin
from simplibs.object.exceptions import SimpleInitializationError
from simplibs.object._core.metadata.instance_builders.instance.helpers._verify_mixin_compatibility import (
    _verify_mixin_compatibility,
)


def _make_dummy_class(name="DummyObject", default_val=0):
    dummy = type(name, (), {})
    dummy.meta = MagicMock()
    dummy.meta.default = default_val
    return dummy


class TestVerifyMixinCompatibilityIdentity:

    def test_non_class_mixin_raises_error(self):
        cls = _make_dummy_class()
        with pytest.raises(SimpleInitializationError):
            _verify_mixin_compatibility(cls, "not_a_class", is_atom=True, mutable=True)

    def test_non_simple_mixin_subclass_raises_error(self):
        class RegularClass:
            pass

        cls = _make_dummy_class()
        with pytest.raises(SimpleInitializationError):
            _verify_mixin_compatibility(cls, RegularClass, is_atom=True, mutable=True)

    def test_valid_simple_mixin_subclass_passes(self):
        class ValidMixin(SimpleMixin):
            __slots__ = ()

        cls = _make_dummy_class()
        _verify_mixin_compatibility(cls, ValidMixin, is_atom=True, mutable=True)


class TestVerifyMixinCompatibilityTopologyMatrix:

    def test_constant_only_passes_for_atom(self):
        class ConstantOnlyMixin(SimpleMixin):
            __slots__ = ()
            _constant_only = True

        cls = _make_dummy_class()
        _verify_mixin_compatibility(cls, ConstantOnlyMixin, is_atom=True, mutable=True)

    def test_constant_only_raises_for_composite(self):
        class ConstantOnlyMixin(SimpleMixin):
            __slots__ = ()
            _constant_only = True

        cls = _make_dummy_class()
        with pytest.raises(SimpleInitializationError):
            _verify_mixin_compatibility(cls, ConstantOnlyMixin, is_atom=False, mutable=True)

    def test_composite_only_passes_for_composite(self):
        class CompositeOnlyMixin(SimpleMixin):
            __slots__ = ()
            _composite_only = True

        cls = _make_dummy_class()
        _verify_mixin_compatibility(cls, CompositeOnlyMixin, is_atom=False, mutable=True)

    def test_composite_only_raises_for_atom(self):
        class CompositeOnlyMixin(SimpleMixin):
            __slots__ = ()
            _composite_only = True

        cls = _make_dummy_class()
        with pytest.raises(SimpleInitializationError):
            _verify_mixin_compatibility(cls, CompositeOnlyMixin, is_atom=True, mutable=True)


class TestVerifyMixinCompatibilityMutabilityMatrix:

    def test_mutable_only_passes_when_mutable(self):
        class MutableOnlyMixin(SimpleMixin):
            __slots__ = ()
            _mutable_only = True

        cls = _make_dummy_class()
        _verify_mixin_compatibility(cls, MutableOnlyMixin, is_atom=True, mutable=True)

    def test_mutable_only_raises_when_immutable(self):
        class MutableOnlyMixin(SimpleMixin):
            __slots__ = ()
            _mutable_only = True

        cls = _make_dummy_class()
        with pytest.raises(SimpleInitializationError):
            _verify_mixin_compatibility(cls, MutableOnlyMixin, is_atom=True, mutable=False)

    def test_immutable_only_passes_when_immutable(self):
        class ImmutableOnlyMixin(SimpleMixin):
            __slots__ = ()
            _immutable_only = True

        cls = _make_dummy_class()
        _verify_mixin_compatibility(cls, ImmutableOnlyMixin, is_atom=True, mutable=False)

    def test_immutable_only_raises_when_mutable(self):
        class ImmutableOnlyMixin(SimpleMixin):
            __slots__ = ()
            _immutable_only = True

        cls = _make_dummy_class()
        with pytest.raises(SimpleInitializationError):
            _verify_mixin_compatibility(cls, ImmutableOnlyMixin, is_atom=True, mutable=True)


class TestVerifyMixinCompatibilityOnlyTypes:

    def test_unset_only_types_passes_any_default_value_type(self):
        class AnyTypeMixin(SimpleMixin):
            __slots__ = ()
            _only_types = UNSET

        cls = _make_dummy_class(default_val="string_value")
        _verify_mixin_compatibility(cls, AnyTypeMixin, is_atom=True, mutable=True)

    def test_matching_only_types_passes(self):
        class IntOnlyMixin(SimpleMixin):
            __slots__ = ()
            _only_types = (int, float)

        cls = _make_dummy_class(default_val=42)
        _verify_mixin_compatibility(cls, IntOnlyMixin, is_atom=True, mutable=True)

    def test_mismatched_only_types_raises_error(self):
        class IntOnlyMixin(SimpleMixin):
            __slots__ = ()
            _only_types = int

        cls = _make_dummy_class(default_val="not_an_int")
        with pytest.raises(SimpleInitializationError):
            _verify_mixin_compatibility(cls, IntOnlyMixin, is_atom=True, mutable=True)