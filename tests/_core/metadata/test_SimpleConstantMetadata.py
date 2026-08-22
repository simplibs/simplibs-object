"""
Tests for `_core/metadata/SimpleConstantMetadata.py`.
"""
from simplibs.object import SimpleConstant


class TestSimpleConstantMetadataBasicFields:

    def test_is_constant_is_true(self, IntConst):
        assert IntConst.meta.is_constant is True

    def test_value_type_and_default_are_set(self, IntConst):
        assert IntConst.meta.value_type is int
        assert IntConst.meta.default == 0

    def test_validate_is_callable(self, IntConst):
        assert callable(IntConst.meta.validate)


class TestSimpleConstantMetadataAtomClassLazyCache:

    def test_atom_class_mutable_starts_as_unset_internally_but_property_builds_it(
        self, IntConst
    ):
        first_access = IntConst.meta.atom_class_mutable
        assert first_access is not None

    def test_atom_class_mutable_is_cached_identity_on_repeated_access(self, IntConst):
        first_access = IntConst.meta.atom_class_mutable
        second_access = IntConst.meta.atom_class_mutable
        assert first_access is second_access

    def test_atom_class_mutable_and_immutable_are_different_classes(self, IntConst):
        assert IntConst.meta.atom_class_mutable is not IntConst.meta.atom_class_immutable

    def test_atom_class_immutable_is_cached_identity(self, IntConst):
        first_access = IntConst.meta.atom_class_immutable
        second_access = IntConst.meta.atom_class_immutable
        assert first_access is second_access


class TestSimpleConstantMetadataCustomValidate:

    def test_custom_validate_is_reflected_in_meta(self, PositiveIntConst):
        assert PositiveIntConst.meta.validate(5) is True