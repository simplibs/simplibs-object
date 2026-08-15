from typing import Any
import pytest
from simplibs.exception.testing import maybe_subtest


def assert_instance_hasattr(
    subtests: Any,
    instance: Any,
    *,
    names: tuple[str, ...],
    kind: str,   # "slot", "attribute", "method", ...
    verbose: bool = True,
    intro: str = "",
) -> None:
    """
    Generic attribute presence validator.

    Validates that all expected names exist on the instance.
    Used for:
        - slot names
        - attribute names
        - method names
        - any other mixin-provided members

    Parameters:
        subtests:
        instance:
        names: tuple of strings to check
        kind: textual label used in error messages ("slot", "attribute", "method")
        verbose:
        intro:
    """

    subintro = f"assert_instance_hasattr[{kind}]::"

    # 1) Validate input type
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_input",
        verbose=verbose,
    ):
        if not isinstance(names, tuple):
            pytest.fail(
                f"Parameter '{kind}_names' must be a tuple of strings, "
                f"got: {names!r}"
            )

        for name in names:
            if not isinstance(name, str):
                pytest.fail(
                    f"{kind.capitalize()} name '{name!r}' is not a string. "
                    f"All {kind} names must be strings."
                )

    # 2) Validate presence on instance
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}check_presence",
        verbose=verbose,
    ):
        for name in names:
            if not hasattr(instance, name):
                pytest.fail(
                    f"Instance of class '{instance.__class__.__name__}' "
                    f"does not contain expected {kind} '{name}'. "
                    f"Available attributes: {dir(instance)}"
                )
