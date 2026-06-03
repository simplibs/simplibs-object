import pytest
from unittest.mock import MagicMock
from simplibs.object.core._metadata.mixins.class_names.CreateNames import CreateNames


class MockMetadata(CreateNames):
    """Pomocná třída pro otestování mixinu."""

    def __init__(self, owner_name: str):
        self.owner_class = MagicMock()
        self.owner_class.__name__ = owner_name
        self.name_readable = None
        self.name_title = None
        self.name_snake = None
        self.name_private = None


def test_create_names_integration():
    """Ověřuje kompletní transformaci jména třídy na všechny varianty."""
    meta = MockMetadata("HTTPClient")
    meta.create_names()

    assert meta.name_readable == "HTTP client"
    assert meta.name_title == "HTTP client"
    assert meta.name_snake == "http_client"
    assert meta.name_private == "_http_client"


def test_create_names_standard_case():
    meta = MockMetadata("MySimpleObject")
    meta.create_names()

    assert meta.name_readable == "my simple object"
    assert meta.name_title == "My simple object"
    assert meta.name_snake == "my_simple_object"
    assert meta.name_private == "_my_simple_object"