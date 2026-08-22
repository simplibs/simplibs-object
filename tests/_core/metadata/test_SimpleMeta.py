"""
Tests for `_core/metadata/SimpleMeta.py`.
"""
import pytest
from simplibs.object import SimpleBase, SimpleConstant, SimpleObject
from simplibs.object.exceptions import SimpleDefinitionError
from simplibs.sentinels import UNSET


class TestSimpleMetaNewSkipsBaseClasses:

    def test_base_classes_do_not_get_metadata_attached(self):
        assert SimpleBase.__metadata__ is UNSET
        assert SimpleConstant.__metadata__ is UNSET
        assert SimpleObject.__metadata__ is UNSET


class TestSimpleMetaNewAttachesCorrectMetadataType:

    def test_class_without_inners_gets_constant_metadata(self, IntConst):
        from simplibs.object._core.metadata.SimpleConstantMetadata import (
            SimpleConstantMetadata,
        )
        assert isinstance(IntConst.__metadata__, SimpleConstantMetadata)

    def test_class_with_inners_gets_object_metadata(self, NonDecomposablePairObject):
        from simplibs.object._core.metadata.SimpleObjectMetadata import (
            SimpleObjectMetadata,
        )
        assert isinstance(NonDecomposablePairObject.__metadata__, SimpleObjectMetadata)


class TestSimpleMetaWriteOnceClassAttributes:

    def test_reassigning_declarative_attribute_raises(self, IntConst):
        with pytest.raises(SimpleDefinitionError):
            IntConst._type = str

    def test_reassigning_default_raises(self, IntConst):
        with pytest.raises(SimpleDefinitionError):
            IntConst._default = 999


class TestSimpleMetaCall:

    def test_call_creates_instance(self, IntConst):
        instance = IntConst()
        assert instance.value == IntConst.meta.default

    def test_call_only_accepts_keyword_arguments(self, IntConst):
        with pytest.raises(TypeError):
            IntConst(True)  # positional arguments are not permitted

    def test_call_forwards_mutable_flag(self, IntConst):
        immutable_instance = IntConst(mutable=False)
        with pytest.raises(AttributeError):
            immutable_instance.value = 1


class TestSimpleMetaRepr:

    def test_base_class_repr_shows_system_base(self):
        assert "System Base" in repr(SimpleConstant)

    def test_user_class_repr_shows_blueprint_info(self, IntConst):
        result = repr(IntConst)
        assert "IntConst" in result
        assert "blueprint=" in result
        assert "type=Constant" in result

    def test_composite_class_repr_shows_object_type(self, NonDecomposablePairObject):
        result = repr(NonDecomposablePairObject)
        assert "type=Object" in result


class TestSimpleMetaStr:

    def test_str_returns_class_name(self, IntConst):
        assert str(IntConst) == "IntConst"


class TestSimpleMetaMetaProperty:

    def test_meta_property_returns_dunder_metadata(self, IntConst):
        assert IntConst.meta is IntConst.__metadata__