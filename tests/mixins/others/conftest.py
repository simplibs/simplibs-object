"""
Shared fixtures for `others/properties/*` and `others/state/*` tests.

Recreates a tree structure (Outer -> Pair -> First/Second, + Third).
"""
import pytest
from simplibs.object import SimpleConstant, SimpleObject


@pytest.fixture
def IntLeaf():
    class IntLeaf(SimpleConstant):
        _type = int
        _default = 7

    return IntLeaf


@pytest.fixture
def tree_classes():
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
            return value, 0

    class Outer(SimpleObject):
        _type = int
        _inners = (Pair, Third)

        @classmethod
        def _logic(cls, pair, third):
            return pair + third

        @classmethod
        def _decompose(cls, value):
            return value, 0

    return Outer, Pair, First, Second, Third


@pytest.fixture
def Outer(tree_classes):
    outer, *_ = tree_classes
    return outer