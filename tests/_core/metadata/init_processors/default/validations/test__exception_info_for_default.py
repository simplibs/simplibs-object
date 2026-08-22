import pytest
from unittest.mock import Mock

from simplibs.object._core.metadata.init_processors.default.validations._exception_info_for_default import (
    _exception_info_for_default,
)


def test_exception_info_for_default_with_simple_object() -> None:
    """Test standard diagnostic tuple generation for SimpleObject descendants."""

    dummy_class = Mock(__name__="MyObject", __mro__=("MyObject", "SimpleObject", "object"))

    result = _exception_info_for_default(dummy_class)

    assert result == (
        "MyObject",
        "SimpleObject",
        "INVALID DEFAULT DEFINITION",
        "Metadata validation for: MyObject._default",
    )


def test_exception_info_for_default_with_simple_constant() -> None:
    """Test diagnostic tuple generation for SimpleConstant descendants."""

    dummy_class = Mock(__name__="MyConstant", __mro__=("MyConstant", "SimpleConstant", "object"))

    result = _exception_info_for_default(dummy_class)

    assert result == (
        "MyConstant",
        "SimpleConstant",
        "INVALID DEFAULT DEFINITION",
        "Metadata validation for: MyConstant._default",
    )