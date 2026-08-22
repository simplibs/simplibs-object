"""
Tests for `ValueFormatting` mixin.
"""
import pytest
from simplibs.object.mixins.dunders.representation import ValueFormatting
from simplibs.object.testing import assert_simple_mixin


class TestValueFormattingStructure:

    def test_no_compatibility_flags(self):
        assert ValueFormatting._constant_only is False
        assert ValueFormatting._composite_only is False

    def test_assert_simple_mixin_shallow(self, subtests, IntLeaf):
        assert_simple_mixin(
            subtests,
            ValueFormatting,
            test_class=IntLeaf,
            method_names=("format", "__format__", "__bytes__", "__bool__"),
        )


class TestValueFormattingFormat:

    def test_format_without_pattern_returns_str(self, IntLeaf):
        instance = IntLeaf(mixins=(ValueFormatting,), as_atom=True)
        assert instance.format() == str(instance.value)

    def test_format_with_pattern(self, IntLeaf):
        instance = IntLeaf(mixins=(ValueFormatting,), as_atom=True)
        result = instance.format("{:03d}")
        assert result == "{:03d}".format(instance.value)

    def test_dunder_format_via_fstring(self, IntLeaf):
        instance = IntLeaf(mixins=(ValueFormatting,), as_atom=True)
        result = f"{instance:03d}"
        assert result == "{:03d}".format(instance.value)

    def test_dunder_format_without_spec(self, IntLeaf):
        instance = IntLeaf(mixins=(ValueFormatting,), as_atom=True)
        assert format(instance) == str(instance.value)

    def test_works_on_composite(self, Outer):
        instance = Outer(mixins=(ValueFormatting,))
        assert instance.format() == str(instance.value)


class TestValueFormattingBytes:

    def test_bytes_from_str_value(self):
        from simplibs.object import SimpleConstant

        class StrLeaf(SimpleConstant):
            _type = str
            _default = "hello"

        instance = StrLeaf(mixins=(ValueFormatting,), as_atom=True)
        assert bytes(instance) == "hello".encode("utf-8")

    def test_bytes_from_bytes_value_returned_directly(self):
        from simplibs.object import SimpleConstant

        class BytesLeaf(SimpleConstant):
            _type = bytes
            _default = b"raw"

        instance = BytesLeaf(mixins=(ValueFormatting,), as_atom=True)
        assert bytes(instance) == b"raw"

    def test_bytes_raises_for_unsupported_type(self, IntLeaf):
        instance = IntLeaf(mixins=(ValueFormatting,), as_atom=True)
        with pytest.raises(TypeError):
            bytes(instance)


class TestValueFormattingBool:

    def test_bool_matches_value_truthiness_nonzero(self, IntLeaf):
        instance = IntLeaf(mixins=(ValueFormatting,), as_atom=True)
        assert bool(instance) is True

    def test_bool_matches_value_truthiness_zero(self):
        from simplibs.object import SimpleConstant

        class ZeroLeaf(SimpleConstant):
            _type = int
            _default = 0

        instance = ZeroLeaf(mixins=(ValueFormatting,), as_atom=True)
        assert bool(instance) is False