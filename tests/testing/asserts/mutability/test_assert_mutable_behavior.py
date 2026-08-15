from typing import Any
import pytest
from simplibs.exception.testing import maybe_subtest
# Outers
from ..base.assert_value_change import assert_value_change


def assert_mutable_behavior(
    subtests: Any,
    test_class: Any,
    *,
    new_value: Any,
    verbose: bool = True,
    verbose_value_change: bool = True,
    intro: str = "",
) -> None:
    """
    Verifies correct mutable behavior:

    - instance created with mutable=True must NOT change identity
    - setter must update the internal value in-place
    """

    subintro = "test_mutable_behavior::"

    # 1) Create mutable instance
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}create_mutable_instance",
        verbose=verbose,
    ):
        try:
            instance = test_class(mutable=True)
        except Exception as exc:
            pytest.fail(f"Failed to create mutable instance: {exc}")

        assert instance is not None

    # 2) Capture original identity
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}capture_original_identity",
        verbose=verbose,
    ):
        original_id = id(instance)

    # 3) Apply new value (validation + setter handled inside)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}apply_value",
        verbose=verbose,
    ):
        assert_value_change(
            subtests,
            instance,
            value=new_value,
            verbose=verbose_value_change and verbose,
            intro=intro,
        )

    # 4) Identity MUST remain unchanged
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}identity_preserved",
        verbose=verbose,
    ):
        if id(instance) != original_id:
            pytest.fail(
                "Mutable instance changed identity after value update, "
                "but mutable instances must preserve identity."
            )
