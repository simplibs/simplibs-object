"""
Tests for `SimpleBase.py`.
"""
from simplibs.object import SimpleBase
from simplibs.object._core.metadata.SimpleMeta import SimpleMeta
from simplibs.sentinels import UNSET


class TestSimpleBaseStructure:

    def test_has_empty_slots(self):
        assert SimpleBase.__slots__ == ()

    def test_metadata_placeholder_is_unset(self):
        assert SimpleBase.__metadata__ is UNSET

    def test_uses_simple_meta_as_metaclass(self):
        assert type(SimpleBase) is SimpleMeta