"""
Tests for `tools/automate_creators/create_constant_class.py`.
"""
import pytest
from simplibs.object import SimpleConstant
from simplibs.object.tools.automate_creators.create_constant_class import (
    create_constant_class,
)
from simplibs.sentinels import UNSET


class TestCreateConstantClassHappyPath:

    def test_creates_working_constant_class(self):
        Age = create_constant_class("Age", default=18)

        assert issubclass(Age, SimpleConstant)
        assert Age.meta.default == 18
        assert Age.meta.value_type is int

    def test_explicit_value_type_overrides_inference(self):
        Flexible = create_constant_class("Flexible", default=1, value_type=int | str)
        assert Flexible.meta.value_type == (int | str)

    def test_class_name_is_applied(self):
        Age = create_constant_class("Age", default=0)
        assert Age.__name__ == "Age"


class TestCreateConstantClassValidate:

    def test_regular_validate_function_is_attached(self):
        def _validate(cls, value, *, return_bool=False):
            if value >= 0:
                return True
            return cls.bool_or_raise_validate_error(
                value, problem="must be non-negative", return_bool=return_bool
            )

        PositiveAge = create_constant_class("PositiveAge", default=0, validate=_validate)
        assert PositiveAge.is_valid(5) is True
        assert PositiveAge.is_valid(-5) is False

    def test_lambda_validate_is_normalized_and_attached(self):
        PositiveAge = create_constant_class(
            "PositiveAge", default=0, validate=lambda value: value >= 0
        )
        assert PositiveAge.is_valid(5) is True
        assert PositiveAge.is_valid(-5) is False

    def test_no_validate_means_default_accept_all(self):
        Age = create_constant_class("Age", default=0)
        assert Age.is_valid(-999) is True


class TestCreateConstantClassValidation:

    def test_invalid_class_name_raises(self):
        with pytest.raises(Exception):
            create_constant_class("", default=0)

    def test_missing_default_raises(self):
        with pytest.raises(Exception):
            create_constant_class("Age", default=UNSET)

    def test_none_default_raises(self):
        with pytest.raises(Exception):
            create_constant_class("Age", default=None)