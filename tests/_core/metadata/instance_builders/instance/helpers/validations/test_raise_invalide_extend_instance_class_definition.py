from unittest.mock import Mock
from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.helpers.validations.raise_invalide_extend_instance_class_definition import (
    raise_invalide_extend_instance_class_definition,
)


def test_raise_invalide_extend_instance_class_definition(subtests) -> None:
    """Tests that raise_invalide_extend_instance_class_definition raises SimpleInitializationError."""

    dummy_cls = Mock()
    dummy_cls.__name__ = "MyClass"

    # Mixin mock simulating a class with raw __dict__ containing un-decorated method
    class DummyMixin:
        def __extend_instance_class__(self):
            pass

    assert_exception_function(
        subtests,
        raise_invalide_extend_instance_class_definition,
        invalid_params=(dummy_cls, DummyMixin),
        exception_type=SimpleInitializationError,
        error_name="INVALID EXTEND INSTANCE CLASS DEFINITION",
        label="mixin_invalid_extend_instance_class_definition",
        expected="@classmethod or @staticmethod decorator on __extend_instance_class__",
        value="function",
        problem=(
            "Mixin 'DummyMixin' defines '__extend_instance_class__' as an "
            "un-decorated method or invalid descriptor (function) "
            "when compiling instance class for 'MyClass'."
        ),
        context="create_instance(cls=MyClass, mixin=DummyMixin)",
        how_to_fix=(
            "Decorate '__extend_instance_class__' on the mixin with @classmethod or @staticmethod.",
            "Example:",
            "    class MyMixin(SimpleMixin):",
            "        @classmethod",
            "        def __extend_instance_class__(cls, instance_cls):",
            "            # In-place class modification logic",
            "            ...",
        ),
        exception=TypeError,
        verbose=False,
    )