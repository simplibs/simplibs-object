"""
Shared fixtures for `_common_logic/immutability/*` tests.

Tree structure used across tests:

    Outer (composite, _type=int, logic=sum)
    ├── pair (composite, _type=int, logic=first+second)
    │   ├── first (IntConst, default=1)
    │   └── second (IntConst, default=2)
    └── third (IntConst, default=3)
"""
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.mixins.core_mixins import Infrastructure


@pytest.fixture
def tree_classes():
    """Returns (Outer, Pair, First, Second, Third) blueprint classes."""

    class First(SimpleConstant):
        _type = int
        _default = 1

    class Second(SimpleConstant):
        _type = int
        _default = 2

    class Third(SimpleConstant):
        _type = int
        _default = 3

    class Pair(SimpleObject):
        _type = int
        _inners = (First, Second)

        @classmethod
        def _logic(cls, first, second):
            return first + second

        @classmethod
        def _decompose(cls, value):
            # Deterministic: full value to first, second = 0
            return value, 0

    class Outer(SimpleObject):
        _type = int
        _inners = (Pair, Third)

        @classmethod
        def _logic(cls, pair, third):
            return pair + third

        @classmethod
        def _decompose(cls, value):
            # Deterministic: full value to pair, third = 0
            return value, 0

    return Outer, Pair, First, Second, Third


@pytest.fixture
def immutable_outer_instance(tree_classes):
    """Immutable instance configured with Infrastructure mixin (for with_* functions)."""
    Outer, *_ = tree_classes
    return Outer(mixins=(Infrastructure,), mutable=False)


@pytest.fixture
def mutable_outer_instance(tree_classes):
    """Mutable instance configured with Infrastructure mixin."""
    Outer, *_ = tree_classes
    return Outer(mixins=(Infrastructure,), mutable=True)