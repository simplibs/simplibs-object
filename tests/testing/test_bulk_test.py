"""
Tests for `testing/bulk_test.py`.
"""
import pytest
from simplibs.object.testing.bulk_test import bulk_test
from simplibs.object.testing.containers.ObjectCase import ObjectCase
from simplibs.object.testing.containers.MixinCase import MixinCase
from simplibs.object.testing.containers.TestMixin import TestMixin


class TestBulkTestObjectCase:

    def test_dispatches_object_case(self, IntConst, subtests):
        bulk_test(subtests, [ObjectCase(test_class=IntConst)])


class TestBulkTestMixinCase:

    def test_dispatches_mixin_case(self, IntConst, subtests):
        bulk_test(subtests, [MixinCase(mixin_class=TestMixin, test_class=IntConst)])


class TestBulkTestRawClass:

    def test_dispatches_raw_simple_constant_class(self, IntConst, subtests):
        bulk_test(subtests, [IntConst])


class TestBulkTestClassMixinsTuple:

    def test_dispatches_class_with_mixins_tuple(self, IntConst, subtests):
        bulk_test(subtests, [(IntConst, (TestMixin,))])


class TestBulkTestMixinClassTuple:

    def test_dispatches_mixin_class_tuple(self, IntConst, subtests):
        bulk_test(subtests, [(TestMixin, IntConst)])


class TestBulkTestMixedBatch:

    def test_processes_multiple_heterogeneous_items(self, IntConst, subtests):
        bulk_test(
            subtests,
            [
                IntConst,
                (IntConst, (TestMixin,)),
                (TestMixin, IntConst),
                ObjectCase(test_class=IntConst),
                MixinCase(mixin_class=TestMixin, test_class=IntConst),
            ],
        )


class TestBulkTestUnsupportedItem:

    def test_unrecognized_item_raises_assertion_error(self, subtests):
        with pytest.raises(AssertionError, match="Unsupported bulk test item"):
            bulk_test(subtests, ["not-a-valid-item"])

    def test_wrong_length_tuple_raises(self, IntConst, subtests):
        with pytest.raises(AssertionError, match="Unsupported bulk test item"):
            bulk_test(subtests, [(IntConst, IntConst, IntConst)])