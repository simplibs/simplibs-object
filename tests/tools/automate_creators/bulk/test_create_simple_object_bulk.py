"""
Tests for `tools/automate_creators/bulk/create_simple_object_bulk.py`.
"""
import pytest
from simplibs.object.tools.automate_creators.bulk.create_simple_object_bulk import (
    create_simple_object_bulk,
)
from simplibs.object.tools.automate_creators.bulk.BulkCase import BulkCase


class TestCreateSimpleObjectBulkFromBulkCaseList:

    def test_list_of_bulk_cases(self):
        cases = [BulkCase(class_name="Age", default=18)]
        result = create_simple_object_bulk(cases)
        assert result[0].meta.default == 18


class TestCreateSimpleObjectBulkFromDictList:

    def test_list_of_dicts(self):
        result = create_simple_object_bulk([{"class_name": "Age", "default": 18}])
        assert result[0].meta.default == 18

    def test_empty_list_routes_to_dicts_and_returns_empty(self):
        result = create_simple_object_bulk([])
        assert result == []


class TestCreateSimpleObjectBulkFromTable:

    def test_2d_list_routes_to_table(self):
        result = create_simple_object_bulk([["Age", 18]])
        assert result[0].meta.default == 18


class TestCreateSimpleObjectBulkFromJsonString:

    def test_json_array_string_is_detected(self):
        result = create_simple_object_bulk('[{"class_name": "Age", "default": 18}]')
        assert result[0].meta.default == 18


class TestCreateSimpleObjectBulkFromCsvString:

    def test_csv_string_with_class_name_header_is_detected(self):
        csv_string = "class_name,default,value_type,validate,logic,decompose,return_instance,as_atom,mutable\nAge,18,int,,,,,,\n"
        result = create_simple_object_bulk(csv_string)
        assert result[0].meta.default == 18


class TestCreateSimpleObjectBulkFromYamlString:

    def test_non_json_non_csv_string_falls_back_to_yaml(self):
        yaml_string = "- class_name: Age\n  default: 18\n"
        result = create_simple_object_bulk(yaml_string)
        assert result[0].meta.default == 18


class TestCreateSimpleObjectBulkUnsupportedInput:

    def test_unrecognized_list_item_type_raises_type_error(self):
        with pytest.raises(TypeError):
            create_simple_object_bulk([42])

    def test_completely_unsupported_input_type_raises_type_error(self):
        with pytest.raises(TypeError):
            create_simple_object_bulk(12345)