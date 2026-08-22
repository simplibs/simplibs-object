"""
Tests for `_core/metadata/instance_builders/atom_class/InstanceBase.py`.
"""
from simplibs.object._core.metadata.instance_builders.atom_class.InstanceBase import (
    InstanceBase,
)


class TestInstanceBaseInitMixins:

    def test_init_mixins_is_noop_by_default(self):
        instance = InstanceBase()
        instance.init_mixins()


class TestInstanceBaseMetaProperty:

    def test_meta_reads_from_class_metadata(self):
        class Fake(InstanceBase):
            __metadata__ = "sentinel-metadata"

        assert Fake().meta == "sentinel-metadata"


class TestInstanceBaseRepr:

    def test_repr_without_value_shows_empty(self):
        class FakeMeta:
            class_name = "Fake"
            blueprint_path = "Fake"

        class Fake(InstanceBase):
            __metadata__ = FakeMeta()

        result = repr(Fake())
        assert "value=EMPTY" in result
        assert "Fake" in result

    def test_repr_with_value_shows_value(self):
        class FakeMeta:
            class_name = "Fake"
            blueprint_path = "Fake"

        class Fake(InstanceBase):
            __metadata__ = FakeMeta()

        instance = Fake()
        instance._value = 42
        assert "value=42" in repr(instance)

    def test_repr_includes_object_id(self):
        class FakeMeta:
            class_name = "Fake"
            blueprint_path = "Fake"

        class Fake(InstanceBase):
            __metadata__ = FakeMeta()

        instance = Fake()
        assert hex(id(instance)) in repr(instance)


class TestInstanceBaseStr:

    def test_str_returns_class_name_from_meta(self):
        class FakeMeta:
            class_name = "Fake"

        class Fake(InstanceBase):
            __metadata__ = FakeMeta()

        assert str(Fake()) == "Fake"