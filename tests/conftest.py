"""
Shared fixtures for the `simplibs-object` test suite.

Philosophy:
    Functions in `_core/logic/*` are pure functions operating on `cls`
    (blueprint classes) via the `SimpleConstantProtocol` /
    `SimpleObjectProtocol`. The most natural and resilient way to provide
    a valid `cls` is to use real subclasses of `SimpleConstant` /
    `SimpleObject` processed through `SimpleMeta`.

    These fixture classes serve as building blocks for logic layer tests.
"""
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.mixins.base_class import SimpleMixin


# ----------------------------------------------------------------------
# 1) Atomic (Constant) Blueprints
# ----------------------------------------------------------------------

@pytest.fixture
def IntConst():
    """Simple integer constant without custom validation."""

    class IntConst(SimpleConstant):
        _type = int
        _default = 0

    return IntConst


@pytest.fixture
def StrConst():
    """Simple string constant without custom validation."""

    class StrConst(SimpleConstant):
        _type = str
        _default = ""

    return StrConst


@pytest.fixture
def PositiveIntConst():
    """Integer constant with custom validation via `_validate`.

    Used to distinguish between type validation failures (`validate_type`)
    and value validation failures (`_validate`).
    """

    class PositiveIntConst(SimpleConstant):
        _type = int
        _default = 1

        @classmethod
        def _validate(cls, value, *, return_bool=False):
            if value > 0:
                return True
            return cls.bool_or_raise_validate_error(
                value,
                problem="Value must be a positive integer.",
                return_bool=return_bool,
            )

    return PositiveIntConst


# ----------------------------------------------------------------------
# 2) Composite Blueprints
# ----------------------------------------------------------------------

@pytest.fixture
def PairObject(IntConst):
    """Composite object with two integer inners, summing their values.

    Implements `_decompose` for reactivity tests (`_recalculate_self` /
    `_recalculate_inners`) and `decompose_value` tests.
    """

    class First(IntConst):
        _default = 0

    class Second(IntConst):
        _default = 0

    class PairObject(SimpleObject):
        _type = int
        _inners = (First, Second)

        @classmethod
        def _logic(cls, first, second):
            return first + second

        @classmethod
        def _decompose(cls, value):
            # Deterministic decomposition: first inner takes the value, second stays default
            return value, 0

    return PairObject


@pytest.fixture
def NonDecomposablePairObject(IntConst):
    """Composite object without `_decompose` for `is_decomposeable is False` tests."""

    class First(IntConst):
        _default = 0

    class Second(IntConst):
        _default = 0

    class NonDecomposablePairObject(SimpleObject):
        _type = int
        _inners = (First, Second)

        @classmethod
        def _logic(cls, first, second):
            return first + second

    return NonDecomposablePairObject


# ----------------------------------------------------------------------
# 3) Validation Test Objects
# ----------------------------------------------------------------------

@pytest.fixture(scope="session")
def sample_object_classes():
    """Provides reusable test classes for SimpleConstant and SimpleObject."""

    class MyTestConstant(SimpleConstant):
        _type = int
        _default = 1

    class MyTestObject(SimpleObject):
        _type = dict
        _inners = (MyTestConstant,)

        @classmethod
        def _logic(cls, my_test_constant: int) -> dict:
            return {"my_test_constant": my_test_constant}

        @classmethod
        def _decompose(cls, value: dict) -> tuple:
            return (value.get("my_test_constant", 1),)

    return MyTestConstant, MyTestObject


# ----------------------------------------------------------------------
# 4) Mixin & Initialization Logic Test Objects
# ----------------------------------------------------------------------

@pytest.fixture(scope="session")
def mixin_test_classes():
    """Provides reusable SimpleMixin and SimpleObject test classes."""

    class MyTestMixin(SimpleMixin):
        __slots__ = ("mixin_slot",)

    class MyTestObject(SimpleObject):
        _type = dict

        class MyTestConstant(SimpleConstant):
            _type = int
            _default = 10

        _inners = (MyTestConstant,)

        @classmethod
        def _logic(cls, my_test_constant):
            return {"my_test_constant": my_test_constant}

        @classmethod
        def _decompose(cls, value: dict) -> tuple:
            return (value.get("value", 1),)

    return MyTestMixin, MyTestObject