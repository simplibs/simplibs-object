"""
Tests for `MetaShortcuts` mixin.
"""
from simplibs.object.mixins.others.properties import MetaShortcuts
from simplibs.object.testing import assert_simple_mixin


class TestMetaShortcutsStructure:

    def test_slots_empty(self):
        assert MetaShortcuts.__slots__ == ()

    def test_attribute_names_present(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            MetaShortcuts,
            test_class=Outer,
            attribute_names=(
                "name_snake",
                "value_type",
                "default",
                "is_atom",
                "is_composite",
                "is_decomposeable",
            ),
        )


class TestMetaShortcutsIdentity:

    def test_name_snake_matches_meta(self, Outer):
        instance = Outer(mixins=(MetaShortcuts,))
        assert instance.name_snake == instance.meta.name_snake


class TestMetaShortcutsTypeInfo:

    def test_value_type_matches_meta(self, Outer):
        instance = Outer(mixins=(MetaShortcuts,))
        assert instance.value_type == instance.meta.value_type

    def test_default_matches_meta(self, Outer):
        instance = Outer(mixins=(MetaShortcuts,))
        assert instance.default == instance.meta.default


class TestMetaShortcutsStructureFlags:

    def test_is_atom_true_for_leaf(self, IntLeaf):
        instance = IntLeaf(mixins=(MetaShortcuts,), as_atom=True)
        assert instance.is_atom is True
        assert instance.is_composite is False

    def test_is_atom_false_for_composite(self, Outer):
        instance = Outer(mixins=(MetaShortcuts,))
        assert instance.is_atom is False
        assert instance.is_composite is True

    def test_is_atom_and_is_composite_are_always_opposite(self, Outer, IntLeaf):
        for instance in (
            Outer(mixins=(MetaShortcuts,)),
            IntLeaf(mixins=(MetaShortcuts,), as_atom=True),
        ):
            assert instance.is_atom != instance.is_composite

    def test_is_decomposeable_true_when_decompose_defined(self, Outer):
        instance = Outer(mixins=(MetaShortcuts,))
        assert instance.is_decomposeable is True

    def test_is_decomposeable_false_when_no_decompose(self, tree_classes):
        from simplibs.object import SimpleObject
        Outer, Pair, First, Second, Third = tree_classes

        class NonDecomposableOuter(SimpleObject):
            _type = int
            _inners = (Pair, Third)

            @classmethod
            def _logic(cls, pair, third):
                return pair + third

        instance = NonDecomposableOuter(mixins=(MetaShortcuts,))
        assert instance.is_decomposeable is False

    def test_is_decomposeable_uses_getattr_fallback_for_atoms(self, IntLeaf):
        instance = IntLeaf(mixins=(MetaShortcuts,), as_atom=True)
        assert instance.is_decomposeable is False