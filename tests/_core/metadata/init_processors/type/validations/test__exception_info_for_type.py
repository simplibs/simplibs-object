from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object._core.metadata.init_processors.type.validations._exception_info_for_type import (
    _exception_info_for_type,
)


def test_exception_info_for_type_object(sample_object_classes) -> None:
    """Tests diagnostic data extraction for a SimpleObject subclass."""

    MyTestConstant, MyTestObject = sample_object_classes

    class_name, class_parent, error_name, context, acceptable_definitions = (
        _exception_info_for_type(MyTestObject)
    )

    assert class_name == "MyTestObject"
    assert class_parent == "SimpleObject"
    assert error_name == "INVALID TYPE DEFINITION"
    assert context == "Metadata validation for: MyTestObject._type"
    assert acceptable_definitions == (
        "Acceptable definitions:",
        "class MyTestObject(SimpleObject):",
        "    _type = int",
        "    _type = int | str",
        "    _type = (int, str)",
        "    ...",
    )


def test_exception_info_for_type_constant() -> None:
    """Tests diagnostic data extraction for a SimpleConstant subclass."""

    class MyTestConstant(SimpleConstant):
        _type = int
        _default = 1

    class_name, class_parent, error_name, context, acceptable_definitions = (
        _exception_info_for_type(MyTestConstant)
    )

    assert class_name == "MyTestConstant"
    assert class_parent == "SimpleConstant"
    assert error_name == "INVALID TYPE DEFINITION"
    assert context == "Metadata validation for: MyTestConstant._type"
    assert acceptable_definitions[1] == "class MyTestConstant(SimpleConstant):"