"""
Tests for `_core/metadata/SimpleObjectMetadata.py`.
"""
from simplibs.sentinels import UNSET


class TestSimpleObjectMetadataBasicFields:

    def test_is_constant_is_false(self, NonDecomposablePairObject):
        assert NonDecomposablePairObject.meta.is_constant is False

    def test_inners_tuple_is_stored(self, NonDecomposablePairObject):
        assert len(NonDecomposablePairObject.meta.inners) == 2

    def test_inners_map_keys_by_name_snake(self, NonDecomposablePairObject):
        inners_map = NonDecomposablePairObject.meta.inners_map
        assert set(inners_map.keys()) == {"first", "second"}

    def test_inners_params_name_matches_logic_signature(self, NonDecomposablePairObject):
        assert NonDecomposablePairObject.meta.inners_params_name == ("first", "second")

    def test_default_is_computed_via_logic_dry_run(self, NonDecomposablePairObject):
        assert NonDecomposablePairObject.meta.default == 0


class TestSimpleObjectMetadataDecomposeability:

    def test_missing_decompose_is_not_decomposeable(self, NonDecomposablePairObject):
        assert NonDecomposablePairObject.meta.is_decomposeable is False

    def test_decompose_attribute_is_unset_when_not_overridden(self, NonDecomposablePairObject):
        assert NonDecomposablePairObject.meta.decompose is UNSET


class TestSimpleObjectMetadataCompositeClassLazyCache:

    def test_composite_class_mutable_creates_and_caches_class(
        self, NonDecomposablePairObject
    ):
        first_access = NonDecomposablePairObject.meta.composite_class_mutable
        second_access = NonDecomposablePairObject.meta.composite_class_mutable

        assert first_access is not UNSET
        assert isinstance(first_access, type)
        assert first_access is second_access

    def test_composite_class_immutable_creates_and_caches_class(
        self, NonDecomposablePairObject
    ):
        first_access = NonDecomposablePairObject.meta.composite_class_immutable
        second_access = NonDecomposablePairObject.meta.composite_class_immutable

        assert first_access is not UNSET
        assert isinstance(first_access, type)
        assert first_access is second_access