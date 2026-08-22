"""
Tests for `_core/metadata/SimpleBaseMetadata.py`.
"""
import pytest
from simplibs.object._core.metadata.SimpleBaseMetadata import SimpleBaseMetadata
from simplibs.object.exceptions import SimpleDefinitionError


class TestSimpleBaseMetadataNameDerivation:

    def test_derives_name_fields_from_class_name(self):
        FakeOwner = type("Widget", (), {})
        meta = SimpleBaseMetadata(FakeOwner)

        assert meta.class_name == "Widget"
        assert meta.name_tuple == ("Widget",)
        assert meta.name_snake == "widget"
        assert meta.name_private == "_widget"

    def test_node_names_set_seeded_with_own_name(self):
        FakeOwner = type("Widget", (), {})
        meta = SimpleBaseMetadata(FakeOwner)
        assert meta.node_names_set == {"widget"}

    def test_owner_class_reference_is_stored(self):
        FakeOwner = type("Widget", (), {})
        meta = SimpleBaseMetadata(FakeOwner)
        assert meta.owner_class is FakeOwner


class TestSimpleBaseMetadataProcessUserDataHook:

    def test_process_user_data_is_a_noop_by_default(self):
        FakeOwner = type("Widget", (), {})
        meta = SimpleBaseMetadata(FakeOwner)
        meta._process_user_data()


class TestSimpleBaseMetadataWriteOnce:

    def test_reassigning_existing_attribute_raises(self):
        FakeOwner = type("Widget", (), {})
        meta = SimpleBaseMetadata(FakeOwner)

        with pytest.raises(SimpleDefinitionError):
            meta.class_name = "SomethingElse"

    def test_first_assignment_of_unset_slot_succeeds(self):
        """
        __setattr__ allows assignment only when current value is UNSET.
        """
        from simplibs.object import SimpleConstant

        class Age(SimpleConstant):
            _type = int
            _default = 0

        # First direct assignment to an UNSET slot passes
        Age.meta._atom_class_mutable = "manually-set-once"

        # Second assignment to a non-UNSET slot must fail
        with pytest.raises(SimpleDefinitionError):
            Age.meta._atom_class_mutable = "manually-set-twice"