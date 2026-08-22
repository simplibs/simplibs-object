"""
Tests for `_core/logic/property_builders/value_helpers/create_value_setter.py`.

Verifies:
    1. Locked instance rejection.
    2. Non-decomposable composite rejection.
    3. Root vs. inner target resolution.
    4. Propagation of `_root_value_setter(recalculate_up=True)`.
    5. Conditional invocation of `_recalculate_inners()` for composite types.
    6. Expected parameter annotations.
"""
from types import SimpleNamespace
from typing import Any, Tuple
import pytest
from simplibs.object._core.logic.property_builders.value_helpers.create_value_setter import (
    create_value_setter,
)
from simplibs.object.exceptions import SimpleRuntimeError


def _make_fake_instance(
    locked: bool = False, class_name: str = "FakeInstance"
) -> Tuple[SimpleNamespace, dict[str, Any]]:
    """Helper creating a minimal test-double simulating SimpleInstanceLike."""
    calls: dict[str, Any] = {"root_value_setter": None, "recalculate_inners": False}

    def _root_value_setter(value: Any, recalculate_up: bool = True) -> None:
        calls["root_value_setter"] = (value, recalculate_up)

    def _recalculate_inners() -> None:
        calls["recalculate_inners"] = True

    instance = SimpleNamespace(
        _locked=locked,
        _root_value_setter=_root_value_setter,
        _recalculate_inners=_recalculate_inners,
        __class__=type(class_name, (), {}),
    )
    return instance, calls


class TestCreateValueSetterLockedInstance:

    def test_raises_when_instance_is_locked(self) -> None:
        """Verifies setting value on a locked instance raises SimpleRuntimeError."""
        meta = SimpleNamespace(value_type=int, is_decomposeable=True)
        setter = create_value_setter(meta, is_constant=True, path=None)
        instance, _ = _make_fake_instance(locked=True)

        with pytest.raises(SimpleRuntimeError):
            setter(instance, 5)


class TestCreateValueSetterNotDecomposeable:

    def test_composite_setter_raises_when_not_decomposeable(
        self, NonDecomposablePairObject
    ) -> None:
        """Verifies non-decomposable composite setter raises SimpleRuntimeError."""
        meta = NonDecomposablePairObject.meta

        setter = create_value_setter(meta, is_constant=False, path=None)
        instance, _ = _make_fake_instance(locked=False)

        with pytest.raises(SimpleRuntimeError):
            setter(instance, 5)

    def test_constant_setter_ignores_decomposeable_flag(self) -> None:
        """Verifies constant setter proceeds regardless of is_decomposeable flag."""
        meta = SimpleNamespace(value_type=int, is_decomposeable=False)
        setter = create_value_setter(meta, is_constant=True, path=None)
        instance, calls = _make_fake_instance(locked=False)

        setter(instance, 5)
        assert calls["root_value_setter"] == (5, True)


class TestCreateValueSetterRootVsInner:

    def test_root_setter_targets_self(self) -> None:
        """Verifies path=None invokes root setter on the passed instance directly."""
        meta = SimpleNamespace(value_type=int, is_decomposeable=True)
        setter = create_value_setter(meta, is_constant=True, path=None)
        instance, calls = _make_fake_instance(locked=False)

        setter(instance, 10)
        assert calls["root_value_setter"] == (10, True)

    def test_inner_setter_targets_resolved_instance(self) -> None:
        """Verifies path resolves the nested instance and invokes its root setter."""
        meta = SimpleNamespace(value_type=int, is_decomposeable=True)
        setter = create_value_setter(meta, is_constant=True, path=("_inner",))

        inner_instance, inner_calls = _make_fake_instance(locked=False)
        owner = SimpleNamespace(_locked=False, _inner=inner_instance)

        setter(owner, 3)
        assert inner_calls["root_value_setter"] == (3, True)


class TestCreateValueSetterRecalculateInners:

    def test_composite_setter_calls_recalculate_inners(self) -> None:
        """Verifies composite setter invokes _recalculate_inners()."""
        meta = SimpleNamespace(value_type=int, is_decomposeable=True)
        setter = create_value_setter(meta, is_constant=False, path=None)
        instance, calls = _make_fake_instance(locked=False)

        setter(instance, 5)
        assert calls["recalculate_inners"] is True

    def test_constant_setter_does_not_call_recalculate_inners(self) -> None:
        """Verifies constant setter does not trigger inner recalculation."""
        meta = SimpleNamespace(value_type=int, is_decomposeable=True)
        setter = create_value_setter(meta, is_constant=True, path=None)
        instance, calls = _make_fake_instance(locked=False)

        setter(instance, 5)
        assert calls["recalculate_inners"] is False


class TestCreateValueSetterAnnotations:

    def test_setter_has_expected_annotations(self) -> None:
        """Verifies setter signature annotations for input value and return type."""
        meta = SimpleNamespace(value_type=int, is_decomposeable=True)
        setter = create_value_setter(meta, is_constant=True, path=None)
        assert setter.__annotations__ == {"value": int, "return": None}