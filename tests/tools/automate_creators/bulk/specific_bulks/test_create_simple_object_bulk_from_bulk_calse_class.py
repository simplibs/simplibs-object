"""
Tests for `tools/automate_creators/bulk/specific_bulks/create_simple_object_bulk_from_bulk_case_class.py`.
"""
import pytest
from simplibs.object.tools.automate_creators.bulk.BulkCase import BulkCase
from simplibs.object.tools.automate_creators.bulk.specific_bulks.create_simple_object_bulk_from_bulk_case_class import (
    create_simple_object_bulk_from_bulk_case_class,
)


class TestCreateSimpleObjectBulkFromBulkCaseClassHappyPath:

    def test_creates_list_of_classes_from_bulk_cases(self):
        cases = [
            BulkCase(class_name="Age", default=18),
            BulkCase(class_name="Score", default=0),
        ]
        result = create_simple_object_bulk_from_bulk_case_class(cases)

        assert len(result) == 2
        assert result[0].meta.default == 18
        assert result[1].meta.default == 0

    def test_empty_iterable_returns_empty_list(self):
        result = create_simple_object_bulk_from_bulk_case_class([])
        assert result == []

    def test_respects_return_instance_flag_per_case(self):
        cases = [BulkCase(class_name="Age", default=18, return_instance=True)]
        result = create_simple_object_bulk_from_bulk_case_class(cases)
        assert result[0].value == 18


class TestCreateSimpleObjectBulkFromBulkCaseClassValidation:

    def test_non_bulk_case_item_raises(self):
        with pytest.raises(Exception):
            create_simple_object_bulk_from_bulk_case_class([{"class_name": "Age"}])

    def test_mixed_valid_and_invalid_items_raises_on_invalid(self):
        cases = [BulkCase(class_name="Age", default=18), "not-a-bulk-case"]
        with pytest.raises(Exception):
            create_simple_object_bulk_from_bulk_case_class(cases)