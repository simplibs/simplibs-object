"""
Tests for `_core/metadata/init_processors/blueprint_path/calculate_blueprint_path.py`[cite: 77].

Verifies:
    1. Direct subclasses of SimpleConstant/SimpleObject have paths matching their class name[cite: 77].
    2. Subclasses in custom Simple inheritance chains include parent names in parentheses[cite: 77].
    3. System base classes (SimpleBase, SimpleConstant, SimpleObject) are excluded[cite: 77].
"""
from simplibs.object import SimpleConstant, SimpleObject


class TestCalculateBlueprintPathDirectSubclass:

    def test_direct_subclass_path_is_just_class_name(self) -> None:
        class Age(SimpleConstant):
            _type = int
            _default = 0

        assert Age.meta.blueprint_path == "Age"


class TestCalculateBlueprintPathInheritanceChain:

    def test_subclass_of_user_defined_class_includes_parent(self) -> None:
        class Age(SimpleConstant):
            _type = int
            _default = 0

        class SpecificAge(Age):
            _default = 18

        assert SpecificAge.meta.blueprint_path == "SpecificAge(Age)"

    def test_multi_level_inheritance_lists_all_user_parents(self) -> None:
        class Age(SimpleConstant):
            _type = int
            _default = 0

        class SpecificAge(Age):
            _default = 18

        class VerySpecificAge(SpecificAge):
            _default = 21

        path = VerySpecificAge.meta.blueprint_path
        assert path.startswith("VerySpecificAge(")
        assert "SpecificAge" in path
        assert "Age" in path


class TestCalculateBlueprintPathExcludesBaseClasses:

    def test_base_class_names_never_appear_in_path(self) -> None:
        class Age(SimpleConstant):
            _type = int
            _default = 0

        for base_name in ("SimpleBase", "SimpleConstant", "SimpleObject"):
            assert base_name not in Age.meta.blueprint_path

    def test_composite_object_direct_subclass_path_is_just_class_name(self) -> None:
        class First(SimpleConstant):
            _type = int
            _default = 0

        class Pair(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

        assert Pair.meta.blueprint_path == "Pair"