from typing import Any
import pytest
from simplibs.exception.testing import maybe_subtest


def assert_immutable_behavior(
    subtests: Any,
    test_class: Any,
    *,
    new_value: Any,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """
    Verifies correct immutable behavior:

    - instance created with mutable=False must NOT allow value updates
    - setter must raise an exception
    - original instance must remain unchanged
    """

    subintro = "test_immutable_behavior::"

    # 1) Create immutable instance
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}create_immutable_instance",
        verbose=verbose,
    ):
        try:
            instance = test_class(mutable=False)
        except Exception as exc:
            pytest.fail(f"Failed to create immutable instance: {exc}")

        assert instance is not None

    # 2) Capture original identity and value
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}capture_original_state",
        verbose=verbose,
    ):
        original_id = id(instance)
        original_value = instance.value

    # 3) Attempt to apply new value (must fail)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}setter_must_fail",
        verbose=verbose,
    ):
        # noinspection PyBroadException
        try:
            instance.value = new_value
        except Exception:
            pass  # expected
        else:
            pytest.fail(
                "Immutable instance allowed value update, "
                "but immutable instances must reject setter calls."
            )

    # 4) Identity MUST remain unchanged
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}identity_preserved",
        verbose=verbose,
    ):
        if id(instance) != original_id:
            pytest.fail(
                "Immutable instance changed identity after failed value update."
            )

    # 5) Value MUST remain unchanged
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}value_preserved",
        verbose=verbose,
    ):
        if instance.value != original_value:
            pytest.fail(
                "Immutable instance changed its value after failed setter call."
            )
