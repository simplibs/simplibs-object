from typing import Union, Any
from simplibs.object._core.metadata.init_processors.methods.verifiers.annotations_and_defaults.validations._convert_annotation_to_type_set import (
    _convert_annotation_to_type_set,
)


def test_convert_annotation_single_type() -> None:
    """Tests conversion of a single type."""
    assert _convert_annotation_to_type_set(int) == {int}


def test_convert_annotation_union_types() -> None:
    """Tests conversion of Union and PEP 604 union types."""
    assert _convert_annotation_to_type_set(Union[int, str]) == {int, str}
    assert _convert_annotation_to_type_set(int | str) == {int, str}


def test_convert_annotation_fallback() -> None:
    """Tests fallback to {Any} for complex or non-type annotations."""
    assert _convert_annotation_to_type_set(None) == {Any}
    assert _convert_annotation_to_type_set("string_annotation") == {Any}