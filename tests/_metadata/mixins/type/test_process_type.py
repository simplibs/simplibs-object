import pytest
from unittest.mock import MagicMock
from simplibs.object.core._metadata.mixins.type.ProcessType import ProcessType

class MockMetadata(ProcessType):
    def __init__(self, owner_type):
        self.owner_class = MagicMock()
        self.owner_class.__name__ = "TestClass"
        self.owner_class._type = owner_type
        self.value_type = None

def test_process_type_extraction():
    meta = MockMetadata(int)
    meta.process_type()
    assert meta.value_type is int