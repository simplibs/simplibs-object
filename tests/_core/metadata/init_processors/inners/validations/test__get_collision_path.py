import pytest
from unittest.mock import Mock

from simplibs.object._core.metadata.init_processors.inners.validations._get_collision_path import (
    _get_collision_path,
)


def test_get_collision_path_direct_match() -> None:
    """Test path computation when the current class itself matches collision_name."""

    dummy_class = Mock(__name__="Address")
    dummy_class.meta.name_snake = "address"

    path = _get_collision_path(dummy_class, "address")
    assert path == "Address"


def test_get_collision_path_nested_match() -> None:
    """Test recursive path computation through nested inner components."""

    # Leaf inner (musíme definovat node_names_set i pro koncový uzlík)
    leaf_inner = Mock(__name__="ZipCode")
    leaf_inner.meta.name_snake = "zip_code"
    leaf_inner.meta.node_names_set = {"zip_code"}
    leaf_inner._inners = ()

    # Middle inner containing leaf
    middle_inner = Mock(__name__="Delivery")
    middle_inner.meta.name_snake = "delivery"
    middle_inner.meta.node_names_set = {"delivery", "zip_code"}
    middle_inner._inners = (leaf_inner,)

    # Root class
    root_class = Mock(__name__="Order")
    root_class.meta.name_snake = "order"
    root_class._inners = (middle_inner,)

    path = _get_collision_path(root_class, "zip_code")
    assert path == "Order/Delivery/ZipCode"


def test_get_collision_path_no_match() -> None:
    """Test returning None when no matching collision_name is found."""
    dummy_class = Mock(__name__="Order")
    dummy_class.meta.name_snake = "order"
    dummy_class._inners = ()

    path = _get_collision_path(dummy_class, "unknown_identifier")
    assert path is None