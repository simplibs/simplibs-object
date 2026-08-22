"""
Tests for `_core/metadata/init_processors/methods/verifiers/_exceptions_helpers/expected_structure_for_classmethod.py`.
"""
from unittest.mock import Mock
from simplibs.object._core.metadata.init_processors.methods.verifiers._exceptions_helpers.expected_structure_for_classmethod import (
    expected_structure_for_classmethod,
)


class SimpleObject:
    """Mock parent class for MRO testing."""
    pass


class DummyClass(SimpleObject):
    pass


def test_expected_structure_for_classmethod_with_kwargs() -> None:
    """Tests code blueprint generation with positional and keyword parameters."""
    mock_func = Mock(__name__="my_method")
    mock_bound_method = Mock()
    mock_bound_method.__self__ = DummyClass
    mock_bound_method.__func__ = mock_func

    structure = expected_structure_for_classmethod(
        bound_method=mock_bound_method,
        expected_params=("param_a", "param_b", "kw_c"),
        expected_args_params_count=2,
    )

    assert structure == (
        "Expected structure:",
        "class DummyClass(SimpleObject):",
        "    ...",
        "    @classmethod",
        "    def my_method(param_a, param_b, *, kw_c):",
        "        ...",
    )


def test_expected_structure_for_classmethod_args_only() -> None:
    """Tests code blueprint generation with positional parameters only."""
    mock_func = Mock(__name__="my_method")
    mock_bound_method = Mock()
    mock_bound_method.__self__ = Mock(__name__="PlainClass", __mro__=(object,))
    mock_bound_method.__func__ = mock_func

    structure = expected_structure_for_classmethod(
        bound_method=mock_bound_method,
        expected_params=("param_a",),
        expected_args_params_count=1,
    )

    assert structure[1] == "class PlainClass(SimpleConstant):"
    assert structure[4] == "    def my_method(param_a):"


def test_expected_structure_for_classmethod_defensive_fallback() -> None:
    """Tests code blueprint generation when bound_method is an invalid object."""
    invalid_bound_method = "invalid_method_string"

    structure = expected_structure_for_classmethod(
        bound_method=invalid_bound_method,
        expected_params=("param_a",),
        expected_args_params_count=1,
    )

    assert structure == (
        "Expected structure:",
        "class <UnknownClass>(<UnknownClass>):",
        "    ...",
        "    @classmethod",
        "    def invalid_method_string(param_a):",
        "        ...",
    )