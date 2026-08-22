"""
Tests for `tools/automate_creators/bulk/specific_bulks/create_simple_object_bulk_from_table.py`.
"""
import pytest
from simplibs.object.tools.automate_creators.bulk.specific_bulks.create_simple_object_bulk_from_table import (
    create_simple_object_bulk_from_table,
)


class TestCreateSimpleObjectBulkFromTableHappyPath:

    def test_creates_classes_from_full_rows(self):
        table = [
            ["Age", 18],
            ["Score", 0],
        ]
        result = create_simple_object_bulk_from_table(table)

        assert len(result) == 2
        assert result[0].meta.default == 18
        assert result[1].meta.default == 0

    def test_empty_table_returns_empty_result(self):
        result = create_simple_object_bulk_from_table([])
        assert result == []


class TestCreateSimpleObjectBulkFromTableShortRows:

    def test_incomplete_row_uses_none_defaults_for_missing_columns(self):
        table = [["Age", 18]]
        result = create_simple_object_bulk_from_table(table)
        assert result[0].meta.default == 18


class TestCreateSimpleObjectBulkFromTableValidation:

    def test_non_list_non_tuple_input_raises_type_error(self):
        with pytest.raises(TypeError):
            create_simple_object_bulk_from_table("not-a-table")

    def test_non_list_row_raises_type_error(self):
        with pytest.raises(TypeError):
            create_simple_object_bulk_from_table(["not-a-row"])