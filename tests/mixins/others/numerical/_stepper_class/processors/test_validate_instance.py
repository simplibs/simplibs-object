"""
Tests for `validate_instance(instance)` (Stepper processor).
"""
import pytest
from simplibs.object.mixins.others.numerical._stepper_class.processors import (
    validate_instance,
)


class TestValidateInstance:

    def test_valid_numeric_instance_passes(self, IntLeaf):
        instance = IntLeaf(as_atom=True, mutable=True)
        validate_instance(instance)

    def test_non_numeric_instance_raises(self):
        from simplibs.object import SimpleConstant

        class StrLeaf(SimpleConstant):
            _type = str
            _default = "hello"

        instance = StrLeaf(as_atom=True, mutable=True)
        with pytest.raises(Exception):
            validate_instance(instance)

    def test_plain_object_raises(self):
        with pytest.raises(Exception):
            validate_instance(object())