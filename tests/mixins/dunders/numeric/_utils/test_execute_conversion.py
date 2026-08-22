"""
Tests for `execute_conversion(self, func, *args)`.
"""
from types import SimpleNamespace
import pytest
from simplibs.object.mixins.dunders.numeric import Conversion
from simplibs.object.mixins.dunders.numeric._utils import execute_conversion


class TestExecuteConversion:

    def test_int_conversion(self, IntLeaf):
        instance = IntLeaf(mixins=(Conversion,), as_atom=True)
        result = execute_conversion(instance, int)
        assert result == instance.value
        assert isinstance(result, int)

    def test_float_conversion(self, IntLeaf):
        instance = IntLeaf(mixins=(Conversion,), as_atom=True)
        result = execute_conversion(instance, float)
        assert result == float(instance.value)

    def test_conversion_with_extra_args(self, IntLeaf):
        instance = IntLeaf(mixins=(Conversion,), as_atom=True)
        result = execute_conversion(instance, round, 2)
        assert result == round(instance.value, 2)

    def test_failed_conversion_wrapped_in_type_error(self):
        mock_instance = SimpleNamespace(
            value="not_numeric",
            meta=SimpleNamespace(class_name="DummyClass"),
        )
        with pytest.raises(TypeError) as exc_info:
            execute_conversion(mock_instance, int)

        assert "Cannot execute int() on DummyClass" in str(exc_info.value)

    def test_error_message_contains_class_name_and_func_name(self):
        mock_instance = SimpleNamespace(
            value=complex(1, 2),
            meta=SimpleNamespace(class_name="ComplexLeaf"),
        )
        with pytest.raises(TypeError) as exc_info:
            execute_conversion(mock_instance, int)

        error_msg = str(exc_info.value)
        assert "int" in error_msg
        assert "ComplexLeaf" in error_msg
        assert "value=(1+2j)" in error_msg