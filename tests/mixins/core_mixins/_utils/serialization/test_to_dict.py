"""
Tests for `to_dict(self, *, constant_only=False)`.
"""
from simplibs.object.mixins._common_logic.constants import OWNER_CLASS, VALUE
from simplibs.object.mixins.core_mixins import Infrastructure
from simplibs.object.mixins.core_mixins._utils.serialization import to_dict


class TestToDict:

    def test_contains_owner_class(self, Outer):
        instance = Outer(mixins=(Infrastructure,))
        result = to_dict(instance)
        assert OWNER_CLASS in result
        assert result[OWNER_CLASS] == instance.meta.class_name

    def test_leaf_values_present(self, Outer):
        instance = Outer(mixins=(Infrastructure,))
        result = to_dict(instance)
        assert result["pair"]["first"] == 1
        assert result["pair"]["second"] == 2
        assert result["third"] == 3

    def test_composite_value_present_under_value_key(self, Outer):
        instance = Outer(mixins=(Infrastructure,))
        result = to_dict(instance)
        assert VALUE in result["pair"]
        assert result["pair"][VALUE] == 3  # 1 + 2

    def test_root_value_present(self, Outer):
        instance = Outer(mixins=(Infrastructure,))
        result = to_dict(instance)
        assert VALUE in result
        assert result[VALUE] == 6  # pair(3) + third(3)

    def test_constant_only_excludes_composite_values(self, Outer):
        instance = Outer(mixins=(Infrastructure,))
        result = to_dict(instance, constant_only=True)
        assert VALUE not in result["pair"]
        assert VALUE not in result
        # Constants must remain present
        assert result["pair"]["first"] == 1
        assert result["third"] == 3

    def test_atom_serialization(self, IntLeaf):
        instance = IntLeaf(mixins=(Infrastructure,), as_atom=True)
        result = to_dict(instance)
        assert result[OWNER_CLASS] == instance.meta.class_name
        assert result[instance.meta.name_snake] == 7