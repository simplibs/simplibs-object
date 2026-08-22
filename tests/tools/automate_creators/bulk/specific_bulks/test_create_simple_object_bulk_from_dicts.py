"""
Tests for `tools/automate_creators/bulk/specific_bulks/create_simple_object_bulk_from_dicts.py`.
"""
import pytest
from simplibs.object.tools.automate_creators.bulk.specific_bulks.create_simple_object_bulk_from_dicts import (
    create_simple_object_bulk_from_dicts,
)


class TestCreateSimpleObjectBulkFromDictsHappyPath:

    def test_creates_classes_from_list_of_dicts(self):
        dicts = [
            {"class_name": "Age", "default": 18},
            {"class_name": "Score", "default": 0},
        ]
        result = create_simple_object_bulk_from_dicts(dicts)

        assert len(result) == 2
        assert result[0].meta.default == 18
        assert result[1].meta.default == 0

    def test_empty_list_returns_empty_result(self):
        result = create_simple_object_bulk_from_dicts([])
        assert result == []

    def test_accepts_tuple_input_too(self):
        result = create_simple_object_bulk_from_dicts(
            ({"class_name": "Age", "default": 18},)
        )
        assert len(result) == 1


class TestCreateSimpleObjectBulkFromDictsValidation:

    def test_non_list_non_tuple_input_raises_type_error(self):
        with pytest.raises(TypeError):
            create_simple_object_bulk_from_dicts("not-a-list")

    def test_dict_missing_class_name_raises(self):
        with pytest.raises(Exception):
            create_simple_object_bulk_from_dicts([{"default": 18}])

    def test_dict_with_unknown_key_raises_type_error(self):
        with pytest.raises(TypeError):
            create_simple_object_bulk_from_dicts(
                [{"class_name": "Age", "default": 18, "totally_unknown_key": 1}]
            )