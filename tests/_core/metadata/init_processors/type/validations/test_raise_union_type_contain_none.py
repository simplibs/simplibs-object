from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.type.validations.raise_union_type_contain_none import (
    raise_union_type_contain_none,
)


def test_raise_union_type_contain_none(subtests, sample_object_classes) -> None:
    """Tests that raise_union_type_contain_none raises SimpleDefinitionError."""

    MyTestConstant, MyTestObject = sample_object_classes

    assert_exception_function(
        subtests,
        raise_union_type_contain_none,
        invalid_params=(MyTestObject,),
        exception_type=SimpleDefinitionError,
        error_name="INVALID TYPE DEFINITION",
        label="_type",
        expected="A UnionType without NoneType or literal None.",
        problem="The UnionType definition for class 'MyTestObject' contains NoneType.",
        context="Metadata validation for: MyTestObject._type",
        how_to_fix=(
            "Remove NoneType or literal None from the union expression.",
            "Use only real, concrete types in the union.",
            "Acceptable definitions:",
            "class MyTestObject(SimpleObject):",
            "    _type = int",
            "    _type = int | str",
            "    _type = (int, str)",
            "    ...",
        ),
        exception=TypeError,
        verbose=False,
    )