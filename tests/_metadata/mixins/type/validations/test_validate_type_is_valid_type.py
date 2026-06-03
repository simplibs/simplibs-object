import pytest
from simplibs.object.utils import SimpleObjectMetadataError
from simplibs.object.core._metadata.mixins.type.validations.validate_type_is_valid_type import validate_type_is_valid_type

class MyClass: pass

def test_validate_type_success():
    """Ověřuje, že základní i složené typy projdou."""
    validate_type_is_valid_type(MyClass, int)
    validate_type_is_valid_type(MyClass, (int, str))
    validate_type_is_valid_type(MyClass, MyClass)

def test_validate_type_fails_on_none():
    with pytest.raises(SimpleObjectMetadataError, match="není definován"):
        validate_type_is_valid_type(MyClass, None)

def test_validate_type_fails_on_instance():
    """_type = 123 místo _type = int."""
    with pytest.raises(SimpleObjectMetadataError, match="není platným typem"):
        validate_type_is_valid_type(MyClass, 123)

def test_validate_type_fails_on_empty_tuple():
    with pytest.raises(SimpleObjectMetadataError, match="není platným typem"):
        validate_type_is_valid_type(MyClass, ())

def test_validate_type_recursive_failure():
    """Tuple obsahuje jeden nevalidní prvek."""
    with pytest.raises(SimpleObjectMetadataError, match="není platným typem"):
        validate_type_is_valid_type(MyClass, (int, "není_typ"))