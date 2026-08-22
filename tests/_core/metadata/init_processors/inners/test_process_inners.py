"""
Tests for `_core/metadata/init_processors/inners/process_inners.py`[cite: 79].

Verifies:
    1. Valid inner tuples[cite: 79].
    2. Empty or non-tuple `_inners` structures[cite: 79].
    3. Invalid inner types (non-class, non-Simple subclasses, direct base usage)[cite: 79].
    4. Name collisions between inners[cite: 79].
    5. Name collisions between an inner and the composite owner class[cite: 79].

Note on missing `_inners`:
    `SimpleMeta.__new__` routes classes without `_inners` to `SimpleConstantMetadata`,
    so `process_inners` is only invoked when `_inners` is present[cite: 79].
"""
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions import SimpleDefinitionError


def _int_const(name: str, default: int = 0) -> type:
    """Helper factory function to create a named integer SimpleConstant."""
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


class TestProcessInnersHappyPath:

    def test_valid_inners_are_accepted(self) -> None:
        First = _int_const("First")
        Second = _int_const("Second")

        class Pair(SimpleObject):
            _type = int
            _inners = (First, Second)

            @classmethod
            def _logic(cls, first, second):
                return first + second

        assert Pair.meta.inners == (First, Second)

    def test_node_names_set_includes_inner_names(self) -> None:
        First = _int_const("First")

        class Single(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

        assert "first" in Single.meta.node_names_set
        assert "single" in Single.meta.node_names_set


class TestProcessInnersInvalidStructure:

    def test_empty_tuple_inners_raises(self) -> None:
        with pytest.raises(SimpleDefinitionError):
            class EmptyInners(SimpleObject):
                _type = int
                _inners = ()

                @classmethod
                def _logic(cls):
                    return 0

    def test_non_tuple_inners_raises(self) -> None:
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class ListInners(SimpleObject):
                _type = int
                _inners = [First]

                @classmethod
                def _logic(cls, first):
                    return first


class TestProcessInnersInvalidInnerType:

    def test_non_class_inner_raises(self) -> None:
        with pytest.raises(SimpleDefinitionError):
            class BadInner(SimpleObject):
                _type = int
                _inners = (42,)

                @classmethod
                def _logic(cls, first):
                    return first

    def test_non_simple_class_inner_raises(self) -> None:
        class NotSimple:
            pass

        with pytest.raises(SimpleDefinitionError):
            class BadInner(SimpleObject):
                _type = int
                _inners = (NotSimple,)

                @classmethod
                def _logic(cls, first):
                    return first

    def test_using_simple_constant_directly_raises(self) -> None:
        with pytest.raises(SimpleDefinitionError):
            class BadInner(SimpleObject):
                _type = int
                _inners = (SimpleConstant,)

                @classmethod
                def _logic(cls, first):
                    return first

    def test_using_simple_object_directly_raises(self) -> None:
        with pytest.raises(SimpleDefinitionError):
            class BadInner(SimpleObject):
                _type = int
                _inners = (SimpleObject,)

                @classmethod
                def _logic(cls, first):
                    return first


class TestProcessInnersNameCollisions:

    def test_collision_between_two_inners_raises(self) -> None:
        FirstA = _int_const("Duplicate")
        FirstB = _int_const("Duplicate")

        with pytest.raises(SimpleDefinitionError):
            class Pair(SimpleObject):
                _type = int
                _inners = (FirstA, FirstB)

                @classmethod
                def _logic(cls, duplicate):
                    return duplicate

    def test_inner_name_colliding_with_owner_class_name_raises(self) -> None:
        Owner = _int_const("Owner")

        def _logic(cls, owner):
            return owner

        with pytest.raises(SimpleDefinitionError):
            type(
                "Owner",
                (SimpleObject,),
                {
                    "_type": int,
                    "_inners": (Owner,),
                    "_logic": classmethod(_logic),
                },
            )