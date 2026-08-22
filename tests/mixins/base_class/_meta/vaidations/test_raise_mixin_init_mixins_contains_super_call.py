from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.base_class._meta.validations.raise_mixin_init_mixins_contains_super_call import (
    raise_mixin_init_mixins_contains_super_call,
)


def dummy_init_mixins_with_super(self) -> None:
    super().init_mixins()


def test_raise_mixin_init_mixins_contains_super_call(subtests) -> None:
    """Tests that raise_mixin_init_mixins_contains_super_call raises SimpleRuntimeError."""

    class MyInvalidMixin:
        init_mixins = dummy_init_mixins_with_super

    assert_exception_function(
        subtests,
        raise_mixin_init_mixins_contains_super_call,
        invalid_params=(MyInvalidMixin,),
        exception_type=SimpleRuntimeError,
        error_name="MIXIN DEFINITION ERROR",
        label="Forbidden super() call in init_mixins",
        value=dummy_init_mixins_with_super,
        expected="The method init_mixins must NOT call super().init_mixins().",
        problem=(
            "Mixin 'MyInvalidMixin' overrides 'init_mixins' and calls super().",
            "Mixins are synthesized directly into target classes without MRO inheritance.",
            "Calling super() inside synthesized mixin hooks causes runtime TypeErrors.",
        ),
        context="Mixin definition check: MyInvalidMixin",
        how_to_fix=(
            "Remove all super() calls from init_mixins().",
            "The instance compilation engine automatically orchestrates and calls all mixin hooks.",
            "Example:",
            "    def init_mixins(self):",
            "        self._my_slot = 'default_value'",
        ),
        exception=TypeError,
        verbose=False,
    )