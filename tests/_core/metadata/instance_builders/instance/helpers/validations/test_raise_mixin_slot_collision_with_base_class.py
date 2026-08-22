from unittest.mock import Mock
from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.helpers.validations.raise_mixin_slot_collision_with_base_class import (
    raise_mixin_slot_collision_with_base_class,
)


def test_raise_mixin_slot_collision_with_base_class(subtests) -> None:
    """Tests that raise_mixin_slot_collision_with_base_class raises SimpleInitializationError."""

    dummy_cls = Mock()
    dummy_cls.__name__ = "BaseClass"

    dummy_mixin = Mock()
    dummy_mixin.__name__ = "MyMixin"

    assert_exception_function(
        subtests,
        raise_mixin_slot_collision_with_base_class,
        invalid_params=(dummy_cls, dummy_mixin, "shadowed_slot"),
        exception_type=SimpleInitializationError,
        error_name="MIXIN BASE SLOT COLLISION",
        label="mixin_base_slot_collision",
        expected="Mixin slots distinct from base class __slots__ layout",
        value="shadowed_slot",
        problem=(
            "Mixin 'MyMixin' defines slot 'shadowed_slot', "
            "which shadows an existing slot from base class 'BaseClass' "
            "when building class_dict."
        ),
        context="create_instance(cls=BaseClass, mixin=MyMixin)",
        how_to_fix=(
            "Rename or remove slot 'shadowed_slot' in mixin 'MyMixin'.",
            "Example:",
            "    class MyMixin(SimpleMixin):",
            "        __slots__ = ('_mymixin_shadowed_slot',)",
            "Base class 'BaseClass' already owns this attribute slot layout.",
        ),
        exception=TypeError,
        verbose=False,
    )