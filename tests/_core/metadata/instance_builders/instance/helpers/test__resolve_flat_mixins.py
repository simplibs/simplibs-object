"""
Tests for `_core/metadata/instance_builders/instance/helpers/_resolve_flat_mixins.py`.
"""
import importlib
import pytest
from simplibs.object.mixins.base_class import SimpleMixin
from simplibs.object import SimpleConstant

_resolve_flat_mixins_module = importlib.import_module(
    "simplibs.object._core.metadata.instance_builders.instance.helpers._resolve_flat_mixins"
)
_resolve_flat_mixins = _resolve_flat_mixins_module._resolve_flat_mixins


def _int_const(name="Widget", default=0):
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


@pytest.fixture
def no_op_validate(monkeypatch):
    """
    Replaces `_verify_mixin_compatibility` with a no-op recorder to isolate
    flattening logic from validation logic.
    """
    calls = []

    def fake_verify_mixin_compatibility(cls, mixin, is_atom, mutable):
        calls.append((cls, mixin, is_atom, mutable))

    monkeypatch.setattr(
        _resolve_flat_mixins_module,
        "_verify_mixin_compatibility",
        fake_verify_mixin_compatibility,
    )
    return calls


class TestResolveFlatMixinsBasicFlattening:

    def test_single_mixin_without_parents_is_returned(self, no_op_validate):
        class MixinA(SimpleMixin):
            __slots__ = ()

        cls = _int_const()
        result = _resolve_flat_mixins(cls, (MixinA,), is_atom=True, mutable=True)
        assert result == (MixinA,)

    def test_multiple_independent_mixins_preserve_order(self, no_op_validate):
        class MixinA(SimpleMixin):
            __slots__ = ()

        class MixinB(SimpleMixin):
            __slots__ = ()

        cls = _int_const()
        result = _resolve_flat_mixins(cls, (MixinA, MixinB), is_atom=True, mutable=True)
        assert result == (MixinA, MixinB)


class TestResolveFlatMixinsMroExpansion:

    def test_parent_mixin_is_included_via_mro(self, no_op_validate):
        class ParentMixin(SimpleMixin):
            __slots__ = ()

        class ChildMixin(ParentMixin):
            __slots__ = ()

        cls = _int_const()
        result = _resolve_flat_mixins(cls, (ChildMixin,), is_atom=True, mutable=True)

        assert ChildMixin in result
        assert ParentMixin in result

    def test_child_appears_before_parent_in_output(self, no_op_validate):
        class ParentMixin(SimpleMixin):
            __slots__ = ()

        class ChildMixin(ParentMixin):
            __slots__ = ()

        cls = _int_const()
        result = _resolve_flat_mixins(cls, (ChildMixin,), is_atom=True, mutable=True)

        assert result.index(ChildMixin) < result.index(ParentMixin)


class TestResolveFlatMixinsFiltersRoots:

    def test_object_and_simple_mixin_are_never_included(self, no_op_validate):
        class MixinA(SimpleMixin):
            __slots__ = ()

        cls = _int_const()
        result = _resolve_flat_mixins(cls, (MixinA,), is_atom=True, mutable=True)

        assert object not in result
        assert SimpleMixin not in result


class TestResolveFlatMixinsDeduplication:

    def test_shared_parent_mixin_appears_only_once(self, no_op_validate):
        class SharedParent(SimpleMixin):
            __slots__ = ()

        class ChildA(SharedParent):
            __slots__ = ()

        class ChildB(SharedParent):
            __slots__ = ()

        cls = _int_const()
        result = _resolve_flat_mixins(cls, (ChildA, ChildB), is_atom=True, mutable=True)

        assert result.count(SharedParent) == 1

    def test_explicitly_duplicated_top_level_mixin_appears_only_once(self, no_op_validate):
        class MixinA(SimpleMixin):
            __slots__ = ()

        cls = _int_const()
        result = _resolve_flat_mixins(cls, (MixinA, MixinA), is_atom=True, mutable=True)

        assert result.count(MixinA) == 1


class TestResolveFlatMixinsValidationIsInvoked:

    def test_verify_mixin_compatibility_called_once_per_unique_node(self, no_op_validate):
        class ParentMixin(SimpleMixin):
            __slots__ = ()

        class ChildMixin(ParentMixin):
            __slots__ = ()

        cls = _int_const()
        _resolve_flat_mixins(cls, (ChildMixin,), is_atom=True, mutable=True)

        validated_mixins = [call[1] for call in no_op_validate]
        assert validated_mixins.count(ChildMixin) == 1
        assert validated_mixins.count(ParentMixin) == 1

    def test_verify_mixin_compatibility_receives_cls_is_atom_and_mutable(self, no_op_validate):
        class MixinA(SimpleMixin):
            __slots__ = ()

        cls = _int_const()
        _resolve_flat_mixins(cls, (MixinA,), is_atom=False, mutable=False)

        assert no_op_validate == [(cls, MixinA, False, False)]

    def test_verify_mixin_compatibility_error_propagates(self, monkeypatch):
        def failing_verify(cls, mixin, is_atom, mutable):
            raise TypeError("Incompatible mixin")

        monkeypatch.setattr(
            _resolve_flat_mixins_module,
            "_verify_mixin_compatibility",
            failing_verify,
        )

        class MixinA(SimpleMixin):
            __slots__ = ()

        cls = _int_const()
        with pytest.raises(TypeError, match="Incompatible mixin"):
            _resolve_flat_mixins(cls, (MixinA,), is_atom=True, mutable=True)


class TestResolveFlatMixinsEmptyInput:

    def test_empty_mixins_tuple_returns_empty_tuple(self, no_op_validate):
        cls = _int_const()
        result = _resolve_flat_mixins(cls, (), is_atom=True, mutable=True)
        assert result == ()
        assert no_op_validate == []