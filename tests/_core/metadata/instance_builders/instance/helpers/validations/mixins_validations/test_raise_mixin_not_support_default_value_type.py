from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.sentinels import UNSET
from simplibs.object._core.metadata.instance_builders.instance.helpers.validations.mixins_validations.raise_mixin_not_support_default_value_type import (
    raise_mixin_not_support_default_value_type,
)


def test_raise_mixin_not_support_default_value_type(subtests, mixin_test_classes) -> None:
    """Tests that raise_mixin_not_support_default_value_type raises SimpleInitializationError."""

    MyTestMixin, MyTestObject = mixin_test_classes

    # Nastavíme _only_types na mřížku pro testování
    MyTestMixin._only_types = (str,)
    default_value = MyTestObject.meta.default

    try:
        assert_exception_function(
            subtests,
            raise_mixin_not_support_default_value_type,
            invalid_params=(MyTestObject, MyTestMixin),
            exception_type=SimpleInitializationError,
            error_name="INVALID MIXIN USAGE",
            label="mixin_default_type_not_supported",
            value=default_value,
            expected="Default value of type",
            problem="Mixin 'MyTestMixin' declares _only_types",
            context="create_instance(cls=MyTestObject, mixin=MyTestMixin)",
            how_to_fix=(
                "Use this mixin only with classes whose default value matches the required types.",
                "Example:",
                "    class MyClass(SimpleObject):",
                "        _default = 10\n",
                "Or adjust the mixin to accept the desired type:",
                "    _only_types = (int, str)",
            ),
            exception=TypeError,
            verbose=False,
        )

    finally:
        MyTestMixin._only_types = UNSET