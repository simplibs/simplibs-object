import pytest
from typing import Any
from unittest.mock import Mock
from simplibs.randomize import RegistryBase
from simplibs.exception.testing import (
    assert_function_valid_input,
    assert_exception_function,
)
from simplibs.object.tools.randomize._validations.validate_registry_is_randomize_registry_base import (
    validate_registry_is_randomize_registry_base,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "valid_registry",
    [
        None,
        Mock(spec=RegistryBase),
    ],
)
def test_valid_registry(subtests, valid_registry: Any) -> None:
    """Test happy path for valid registry objects (None or RegistryBase instances)."""
    assert_function_valid_input(
        subtests,
        validate_registry_is_randomize_registry_base,
        valid_params=(valid_registry,),
        verbose=False,
    )


@pytest.mark.parametrize(
    "invalid_registry",
    [
        "invalid_registry",
        123,
        [1, 2, 3],
        {"key": "value"},
    ],
)
def test_invalid_registry(subtests, invalid_registry: Any) -> None:
    """Test that invalid registry objects raise SimpleRuntimeError."""
    received_type = type(invalid_registry).__name__

    assert_exception_function(
        subtests,
        validate_registry_is_randomize_registry_base,
        invalid_params=(invalid_registry,),
        exception_type=SimpleRuntimeError,
        error_name="INVALID RANDOMIZE REGISTRY ERROR",
        label="registry",
        expected="None or an instance inheriting from RegistryBase (e.g. LocalRegistry).",
        value=received_type,
        problem=(
            "Provided registry parameter is not a valid simplibs-randomize registry instance.",
            "Custom randomizer lookup requires a compatible RegistryBase container.",
        ),
        context=(
            f"Received registry argument: {invalid_registry!r}",
            f"Received type: '{received_type}'",
        ),
        how_to_fix=(
            "Pass None to use default global RANDOMIZERS registry.",
            "Pass a valid LocalRegistry instance created via simplibs.randomize.",
        ),
        exception=TypeError,
        verbose=False,
    )