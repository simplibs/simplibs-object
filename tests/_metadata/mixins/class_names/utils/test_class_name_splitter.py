import pytest
from simplibs.object.utils.class_name_splitter import class_name_splitter

@pytest.mark.parametrize("input_name, expected", [
    ("SimpleObject", ("simple", "object")),
    ("HTTPClient", ("HTTP", "client")),
    ("JSONParser2", ("JSON", "parser", "2")),
    ("My_Custom_Class", ("my", "custom", "class")),
    ("IPv6Address", ("ipv", "6", "address")),
    ("simpleCase", ("simple", "case")),
    ("Already_Lower", ("already", "lower")),
])
def test_class_name_splitter_logic(input_name, expected):
    """Ověřuje správnou dekompozici různých stylů zápisu."""
    assert class_name_splitter(input_name, validate=False) == expected

def test_class_name_splitter_validation_trigger():
    """Ověřuje, že splitter volá validaci, pokud je zapnutá."""
    with pytest.raises(Exception): # validate_class_name vyhodí chybu
        class_name_splitter("Třída", validate=True)