"""
Tests for `tools/automate_creators/_helpers/load_parameters_from_inners.py`.
"""
import pytest
from simplibs.object import SimpleConstant
from simplibs.object.tools.automate_creators._helpers.load_parameters_from_inners import (
    load_parameters_from_inners,
)


def _int_const(name, default=0):
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


class TestLoadParametersFromInnersEmptyInners:

    def test_empty_tuple_returns_empty_dict(self):
        result = load_parameters_from_inners("Widget", ())
        assert result == {}


class TestLoadParametersFromInnersInputValidation:

    def test_non_tuple_inners_raises(self):
        with pytest.raises(Exception):
            load_parameters_from_inners("Widget", [_int_const("First")])

    def test_inner_not_simple_constant_subclass_raises(self):
        class NotSimple:
            pass

        with pytest.raises(Exception):
            load_parameters_from_inners("Widget", (NotSimple,))


class TestLoadParametersFromInnersHappyPath:

    def test_extracts_default_values_keyed_by_name_snake(self):
        First = _int_const("First", default=1)
        Second = _int_const("Second", default=2)

        result = load_parameters_from_inners("Widget", (First, Second))
        assert result == {"first": 1, "second": 2}

    def test_single_inner(self):
        Only = _int_const("Only", default=99)
        result = load_parameters_from_inners("Widget", (Only,))
        assert result == {"only": 99}