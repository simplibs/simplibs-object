"""
Tests for `tools/automate_creators/bulk/specific_bulks/create_simple_object_bulk_from_json.py`.
"""
import pytest
from simplibs.object.tools.automate_creators.bulk.specific_bulks.create_simple_object_bulk_from_json import (
    create_simple_object_bulk_from_json,
)


class TestCreateSimpleObjectBulkFromJsonHappyPath:

    def test_creates_classes_from_json_array(self):
        json_string = '[{"class_name": "Age", "default": 18}]'
        result = create_simple_object_bulk_from_json(json_string)

        assert len(result) == 1
        assert result[0].meta.default == 18

    def test_empty_json_array_returns_empty_result(self):
        result = create_simple_object_bulk_from_json("[]")
        assert result == []


class TestCreateSimpleObjectBulkFromJsonValidation:

    def test_non_string_input_raises_type_error(self):
        with pytest.raises(TypeError):
            create_simple_object_bulk_from_json(["not", "a", "string"])

    def test_invalid_json_syntax_raises_value_error(self):
        with pytest.raises(ValueError):
            create_simple_object_bulk_from_json("{not valid json")

    def test_json_object_instead_of_array_raises_value_error(self):
        with pytest.raises(ValueError):
            create_simple_object_bulk_from_json('{"class_name": "Age", "default": 18}')