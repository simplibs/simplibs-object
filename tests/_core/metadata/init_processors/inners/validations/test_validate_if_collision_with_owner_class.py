import pytest
from unittest.mock import Mock

from simplibs.exception.testing import assert_exception_function
from simplibs.object._core.metadata.init_processors.inners.validations.validate_if_collision_with_owner_class import (
    validate_if_collision_with_owner_class,
)
from simplibs.object.exceptions import SimpleDefinitionError


def test_validate_if_collision_with_owner_class_pass() -> None:
    """Test that distinct names do not trigger an error."""

    dummy_owner = Mock(__name__="OwnerClass")
    dummy_inner = Mock(__name__="InnerClass")

    validate_if_collision_with_owner_class("inner_class", "owner_class", dummy_inner, dummy_owner)


def test_validate_if_collision_with_owner_class_raises_error(subtests) -> None:
    """Test raising SimpleDefinitionError when inner name collides with owner name."""

    dummy_owner = Mock(__name__="OwnerClass")

    inner_culprit = Mock(__name__="OwnerClass")
    inner_culprit.meta.name_snake = "owner_class"
    inner_culprit._inners = ()

    assert_exception_function(
        subtests,
        validate_if_collision_with_owner_class,

        invalid_params=("owner_class", "owner_class", inner_culprit, dummy_owner),
        exception_type=SimpleDefinitionError,

        error_name="INVALID INNERS DEFINITION",
        label="owner_class_name_collision",
        expected="Unique name_snake across entire composition tree",
        value="owner_class",
        problem="Nested component uses the same identifier as its root owner class.",
        context="OwnerClass._inners validation",
        how_to_fix=(
            "Conflicting identifier: 'owner_class'.",
            "Path to offending component: OwnerClass -> OwnerClass.",
            "Rename class 'OwnerClass' or rename root class 'OwnerClass'.",
            "Every class in the composition hierarchy must have a unique name_snake.",
            "Acceptable definition:",
            "class OwnerClass(SimpleObject):",
            "    _inners = (FirstElement, SecondElement)",
        ),
        exception=NameError,

        verbose=False,
    )