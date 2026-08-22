"""
Tests for `tools/automate_creators/bulk/specific_bulks/create_simple_object_bulk_from_yaml.py`.
"""
import pytest

pytest.importorskip("yaml")

from simplibs.object.tools.automate_creators.bulk.specific_bulks.create_simple_object_bulk_from_yaml import (
    create_simple_object_bulk_from_yaml,
)


class TestCreateSimpleObjectBulkFromYamlHappyPath:

    def test_creates_classes_from_yaml_list(self):
        yaml_string = "- class_name: Age\n  default: 18\n"
        result = create_simple_object_bulk_from_yaml(yaml_string)

        assert len(result) == 1
        assert result[0].meta.default == 18

    def test_multiple_entries(self):
        yaml_string = "- class_name: Age\n  default: 18\n- class_name: Score\n  default: 0\n"
        result = create_simple_object_bulk_from_yaml(yaml_string)
        assert len(result) == 2


class TestCreateSimpleObjectBulkFromYamlValidation:

    def test_non_string_input_raises_type_error(self):
        with pytest.raises(TypeError):
            create_simple_object_bulk_from_yaml(["not", "a", "string"])

    def test_invalid_yaml_syntax_raises_value_error(self):
        with pytest.raises(ValueError):
            create_simple_object_bulk_from_yaml(":\tthis: is: not: valid:")

    def test_yaml_mapping_instead_of_list_raises_value_error(self):
        yaml_string = "class_name: Age\ndefault: 18\n"
        with pytest.raises(ValueError):
            create_simple_object_bulk_from_yaml(yaml_string)