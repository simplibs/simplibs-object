"""
Tests for `_core/metadata/init_processors/methods/verifiers/_exceptions_helpers/exception_info_for_classmethod.py`.
"""
from unittest.mock import Mock
from simplibs.object._core.metadata.init_processors.methods.verifiers._exceptions_helpers.exception_info_for_classmethod import (
    exception_info_for_classmethod,
)


def test_exception_info_for_classmethod_happy_path() -> None:
    """Tests extraction of class name, method name, and context tuple."""
    mock_self = Mock(__name__="DummyClass")
    mock_func = Mock(__name__="dummy_method")

    mock_bound_method = Mock()
    mock_bound_method.__self__ = mock_self
    mock_bound_method.__func__ = mock_func

    class_name, method_name, context = exception_info_for_classmethod(mock_bound_method)

    assert class_name == "DummyClass"
    assert method_name == "dummy_method"
    assert context == "Metadata validation for: DummyClass.dummy_method"


def test_exception_info_for_classmethod_defensive_fallback() -> None:
    """Tests safe fallback when bound_method lacks __self__ or __func__ (e.g., plain string or bad object)."""
    invalid_bound_method = "not_a_bound_classmethod"

    class_name, method_name, context = exception_info_for_classmethod(invalid_bound_method)

    assert class_name == "<UnknownClass>"
    assert method_name == "not_a_bound_classmethod"
    assert context == "Metadata validation for: <UnknownClass>.not_a_bound_classmethod"