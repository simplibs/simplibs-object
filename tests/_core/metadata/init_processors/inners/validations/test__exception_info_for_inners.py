import pytest
from unittest.mock import Mock

from simplibs.object._core.metadata.init_processors.inners.validations._exception_info_for_inners import (
    _exception_info_for_inners,
)


def test_exception_info_for_inners() -> None:
    """Test standard diagnostic tuple generation for _inners validations."""

    dummy_class = Mock(__name__="OrderObject")

    class_name, error_name, context, acceptable = _exception_info_for_inners(dummy_class)

    assert class_name == "OrderObject"
    assert error_name == "INVALID INNERS DEFINITION"
    assert context == "OrderObject._inners validation"
    assert acceptable == (
        "Acceptable definition:",
        "class OrderObject(SimpleObject):",
        "    _inners = (FirstElement, SecondElement)",
    )