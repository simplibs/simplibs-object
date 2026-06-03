import pytest
from simplibs.object.utils import SimpleObjectMetadataError
from simplibs.object.core._metadata.mixins.class_names.validations.validate_class_name import validate_class_name

def test_validate_class_name_success():
    """Ověřuje, že validní názvy projdou bez chyby."""
    validate_class_name("MyClass")
    validate_class_name("HTTPClient")
    validate_class_name("User_Profile_1")

def test_validate_class_name_fails_on_type():
    with pytest.raises(SimpleObjectMetadataError, match="musí být řetězec"):
        validate_class_name(123)

def test_validate_class_name_fails_on_empty():
    with pytest.raises(SimpleObjectMetadataError, match="nesmí být prázdné"):
        validate_class_name("")

def test_validate_class_name_fails_on_invalid_identifier():
    with pytest.raises(SimpleObjectMetadataError, match="není platným identifikátorem"):
        validate_class_name("My-Class")  # Pomlčka není povolena
        validate_class_name("1Class")   # Číslo na začátku

def test_validate_class_name_fails_on_non_ascii():
    with pytest.raises(SimpleObjectMetadataError, match="mimo ASCII"):
        validate_class_name("MojeTřída")

def test_validate_class_name_fails_on_dunder():
    with pytest.raises(SimpleObjectMetadataError, match="rezervované"):
        validate_class_name("__MyClass__")