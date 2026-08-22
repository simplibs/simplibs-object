from unittest.mock import Mock
from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.helpers.validations.raise_mixin_slot_collision import (
    raise_mixin_slot_collision,
)


def test_raise_mixin_slot_collision(subtests) -> None:
    """Tests that raise_mixin_slot_collision raises SimpleInitializationError."""

    dummy_cls = Mock()
    dummy_cls.__name__ = "MyClass"

    dummy_mixin = Mock()
    dummy_mixin.__name__ = "MyMixin"

    assert_exception_function(
        subtests,
        raise_mixin_slot_collision,
        invalid_params=(dummy_cls, dummy_mixin, "colliding_slot"),
        exception_type=SimpleInitializationError,
        error_name="SLOT NAME COLLISION",
        label="mixin_slot_name_collision",
        expected="Unique __slots__ attribute names across all applied mixins",
        value="colliding_slot",
        problem=(
            "Mixin 'MyMixin' defines slot 'colliding_slot', "
            "which collides with an existing slot of the same name from another mixin "
            "when building class_dict for 'MyClass'."
        ),
        context="create_instance(cls=MyClass, mixin=MyMixin)",
        how_to_fix=(
            "Rename slot 'colliding_slot' in mixin 'MyMixin' to prevent attribute collisions.",
            "Example:",
            "    class MyMixin(SimpleMixin):",
            "        __slots__ = ('_mymixin_colliding_slot',)",
        ),
        exception=TypeError,
        verbose=False,
    )