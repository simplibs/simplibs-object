import pytest
from unittest.mock import Mock

from simplibs.exception.testing import assert_exception_function
from simplibs.object._core.metadata.init_processors.inners.validations.validate_collision_within_inners import (
    validate_collision_within_inners,
)
from simplibs.object.exceptions import SimpleDefinitionError


def test_validate_collision_within_inners_pass_no_collision() -> None:
    """Test that empty collision name or owner match is ignored."""

    dummy_owner = Mock(__name__="ParentClass")

    # Empty string collision_name
    validate_collision_within_inners("", "parent_class", (), Mock(), dummy_owner)
    # Collision with owner's snake name is handled elsewhere
    validate_collision_within_inners("parent_class", "parent_class", (), Mock(), dummy_owner)


def test_validate_collision_within_inners_raises_error(subtests) -> None:
    """Test raising SimpleDefinitionError on sibling name collisions."""

    dummy_owner = Mock(__name__="ParentClass")

    # First inner registering the collision name
    first_inner = Mock(__name__="InnerA")
    first_inner.meta.name_snake = "conflict_name"
    first_inner.meta.node_names_set = {"conflict_name"}
    first_inner._inners = ()

    # Second inner causing collision
    second_inner = Mock(__name__="InnerB")
    second_inner.meta.name_snake = "conflict_name"
    second_inner.meta.node_names_set = {"conflict_name"}
    second_inner._inners = ()

    raw_inners = (first_inner,)

    assert_exception_function(
        subtests,
        validate_collision_within_inners,

        invalid_params=("conflict_name", "parent_class", raw_inners, second_inner, dummy_owner),
        exception_type=SimpleDefinitionError,

        error_name="INVALID INNERS DEFINITION",
        label="inner_name_collision",
        expected="Unique name_snake across all inner components",
        value="conflict_name",
        problem="Two inner components share the same identifier.",
        context="ParentClass._inners validation",
        how_to_fix=(
            "Conflicting identifier: 'conflict_name'.",
            "Existing definition: ParentClass -> InnerA.",
            "Duplicate declaration: ParentClass -> InnerB.",
            "Rename one of the conflicting components inside 'ParentClass'.",
            "Ensure you did not accidentally register the same class twice.",
            "name_snake must be globally unique within the composition tree.",
            "Acceptable definition:",
            "class ParentClass(SimpleObject):",
            "    _inners = (FirstElement, SecondElement)",
        ),
        exception=NameError,

        verbose=False,
    )