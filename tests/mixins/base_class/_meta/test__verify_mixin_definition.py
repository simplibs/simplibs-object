"""
Tests for `_verify_mixin_definition` validation pipeline.
"""
from types import SimpleNamespace
import pytest
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.object.mixins.base_class._meta._verify_mixin_definition import (
    _verify_mixin_definition,
)
from simplibs.sentinels import UNSET


class TestVerifyMixinDefinition:

    def test_valid_mixin_passes_validation(self):
        class ValidMixin:
            __name__ = "ValidMixin"
            __slots__ = ("a", "b")
            _constant_only = True
            _only_types = int

            def init_mixins(self):
                self.a = 1

        # Must not raise any error
        _verify_mixin_definition(ValidMixin)

    def test_missing_slots_raises(self):
        class NoSlotsMixin:
            __name__ = "NoSlotsMixin"

        with pytest.raises(SimpleRuntimeError) as exc_info:
            _verify_mixin_definition(NoSlotsMixin)
        assert exc_info.value.label == "__slots__"

    def test_invalid_slots_type_raises(self):
        class ListSlotsMixin:
            __name__ = "ListSlotsMixin"
            __slots__ = ["item"]

        with pytest.raises(SimpleRuntimeError) as exc_info:
            _verify_mixin_definition(ListSlotsMixin)
        assert exc_info.value.label == "__slots__"

    def test_slots_containing_non_string_raises(self):
        dummy_cls = SimpleNamespace(
            __name__="BadSlotItemsMixin",
            __dict__={"__slots__": ("valid", 123)},
        )
        with pytest.raises(SimpleRuntimeError) as exc_info:
            _verify_mixin_definition(dummy_cls)
        assert exc_info.value.label == "__slots__"

    def test_slots_containing_forbidden_name_raises(self):
        class ForbiddenSlotMixin:
            __name__ = "ForbiddenSlotMixin"
            __slots__ = ("_value", "ok_slot")

        with pytest.raises(SimpleRuntimeError) as exc_info:
            _verify_mixin_definition(ForbiddenSlotMixin)
        assert exc_info.value.label == "Forbidden slot names in __slots__"

    def test_dict_containing_forbidden_attributes_raises(self):
        class ForbiddenAttrMixin:
            __name__ = "ForbiddenAttrMixin"
            __slots__ = ()
            value = 100

        with pytest.raises(SimpleRuntimeError) as exc_info:
            _verify_mixin_definition(ForbiddenAttrMixin)
        assert exc_info.value.label == "Forbidden class attributes"

    def test_restriction_flag_not_boolean_raises(self):
        class BadFlagMixin:
            __name__ = "BadFlagMixin"
            __slots__ = ()
            _constant_only = "true"

        with pytest.raises(SimpleRuntimeError) as exc_info:
            _verify_mixin_definition(BadFlagMixin)
        assert exc_info.value.label == "Invalid mixin flag types"

    def test_only_types_invalid_structure_raises(self):
        class BadOnlyTypesMixin:
            __name__ = "BadOnlyTypesMixin"
            __slots__ = ()
            _only_types = ["int", "str"]

        with pytest.raises(SimpleRuntimeError) as exc_info:
            _verify_mixin_definition(BadOnlyTypesMixin)
        assert exc_info.value.label == "_only_types"

    def test_init_mixins_containing_super_call_raises(self):
        class SuperCallingMixin:
            __name__ = "SuperCallingMixin"
            __slots__ = ()

            def init_mixins(self):
                super().init_mixins()

        with pytest.raises(SimpleRuntimeError) as exc_info:
            _verify_mixin_definition(SuperCallingMixin)
        assert exc_info.value.label == "Forbidden super() call in init_mixins"