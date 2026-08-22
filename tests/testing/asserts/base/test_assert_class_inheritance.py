"""
Tests for `testing/asserts/base/assert_class_inheritance.py`.
"""
import pytest
from simplibs.object.testing.asserts.base.assert_class_inheritance import (
    assert_class_inheritance,
)


class TestAssertClassInheritanceConstant:

    def test_passes_for_valid_constant_class(self, IntConst, subtests):
        assert_class_inheritance(subtests, IntConst)


class TestAssertClassInheritanceObject:

    def test_passes_for_valid_object_class(self, NonDecomposablePairObject, subtests):
        assert_class_inheritance(subtests, NonDecomposablePairObject)


class TestAssertClassInheritanceMismatch:

    def test_fails_for_object_class_registered_as_constant_check(self, subtests):
        class NotSimpleAtAll:
            pass

        with pytest.raises(AssertionError):
            assert_class_inheritance(subtests, NotSimpleAtAll, verbose=False)