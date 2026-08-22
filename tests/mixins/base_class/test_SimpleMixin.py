"""
Tests for `SimpleMixin` base class.
"""
import pytest
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.object.mixins.base_class import SimpleMixin
from simplibs.sentinels import UNSET


class TestSimpleMixinDefaults:

    def test_default_compatibility_flags(self):
        assert SimpleMixin._constant_only is False
        assert SimpleMixin._composite_only is False
        assert SimpleMixin._mutable_only is False
        assert SimpleMixin._immutable_only is False
        assert SimpleMixin._only_types is UNSET

    def test_default_slots_is_empty_tuple(self):
        assert SimpleMixin.__slots__ == ()

    def test_default_init_mixins_is_callable_noop(self):
        instance = SimpleMixin()
        # Should execute cleanly without raising any errors
        assert instance.init_mixins() is None


class TestSimpleMixinSubclassing:

    def test_valid_subclass_declaration_succeeds(self):
        class CustomMixin(SimpleMixin):
            __slots__ = ("_mx_value",)
            _constant_only = True
            _only_types = (int, float)

            def init_mixins(self):
                self._mx_value = 0

        assert issubclass(CustomMixin, SimpleMixin)
        assert CustomMixin._constant_only is True
        assert CustomMixin._only_types == (int, float)

    def test_subclass_missing_slots_raises_runtime_error(self):
        with pytest.raises(SimpleRuntimeError) as exc_info:
            class InvalidMixin(SimpleMixin):
                pass

        assert exc_info.value.label == "__slots__"

    def test_subclass_with_forbidden_slot_raises(self):
        with pytest.raises(SimpleRuntimeError) as exc_info:
            class InvalidMixin(SimpleMixin):
                __slots__ = ("_owner",)

        assert exc_info.value.label == "Forbidden slot names in __slots__"

    def test_subclass_with_super_in_init_mixins_raises(self):
        with pytest.raises(SimpleRuntimeError) as exc_info:
            class InvalidMixin(SimpleMixin):
                __slots__ = ()

                def init_mixins(self):
                    super().init_mixins()

        assert exc_info.value.label == "Forbidden super() call in init_mixins"

    def test_subclass_with_isolated_init_mixins_succeeds(self):
        class ValidHookMixin(SimpleMixin):
            __slots__ = ("_mx_data",)

            def init_mixins(self):
                self._mx_data = []

        assert issubclass(ValidHookMixin, SimpleMixin)