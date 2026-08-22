"""
Tests for `tools/automate_creators/bulk/specific_bulks/create_simple_object_bulk_from_csv.py`.
"""
import pytest
from simplibs.object.tools.automate_creators.bulk.specific_bulks.create_simple_object_bulk_from_csv import (
    create_simple_object_bulk_from_csv,
)

CSV_HEADER = "class_name,default,value_type,validate,logic,decompose,return_instance,as_atom,mutable"


class TestCreateSimpleObjectBulkFromCsvHappyPath:

    def test_creates_classes_from_csv_rows(self):
        csv_string = f"{CSV_HEADER}\nAge,18,int,,,,,,\nScore,0,int,,,,,,\n"
        result = create_simple_object_bulk_from_csv(csv_string)

        assert len(result) == 2
        assert result[0].meta.default == 18
        assert result[1].meta.default == 0

    def test_header_only_returns_empty_result(self):
        result = create_simple_object_bulk_from_csv(CSV_HEADER)
        assert result == []


class TestCreateSimpleObjectBulkFromCsvTypeConversion:

    def test_default_is_converted_to_int_when_possible(self):
        csv_string = f"{CSV_HEADER}\nAge,18,,,,,,,\n"
        result = create_simple_object_bulk_from_csv(csv_string)
        assert isinstance(result[0].meta.default, int)

    def test_default_falls_back_to_string_when_not_numeric(self):
        csv_string = f"{CSV_HEADER}\nLabel,hello,str,,,,,,\n"
        result = create_simple_object_bulk_from_csv(csv_string)
        assert result[0].meta.default == "hello"

    def test_return_instance_true_flag_is_parsed(self):
        csv_string = f"{CSV_HEADER}\nAge,18,,,,,true,,\n"
        result = create_simple_object_bulk_from_csv(csv_string)
        assert result[0].value == 18


class TestCreateSimpleObjectBulkFromCsvValidation:

    def test_non_string_input_raises_type_error(self):
        with pytest.raises(TypeError):
            create_simple_object_bulk_from_csv(["not", "a", "string"])

    def test_callable_columns_are_unsupported_in_csv(self):
        csv_string = f"{CSV_HEADER}\nPair,,,,some_callable_reference,,,,\n"
        with pytest.raises(ValueError):
            create_simple_object_bulk_from_csv(csv_string)