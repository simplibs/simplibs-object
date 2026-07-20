from typing import TYPE_CHECKING
# Outers
from .....constants import BASE_CLASS_NAMES
# Inners
from .validations.parameters import (
    validate_param_is_bool,
    validate_class_is_not_base_class
)
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike


def validate_class_and_parameters(
    cls: "SimpleClassLike",
    as_atom: bool,
    mutable: bool,
) -> None:
    """
    Validuje základní parametry pro vytvoření instance.

    - Ověří, že cílová třída není jednou ze základních (BASE_CLASS_NAMES).
    - Ověří, že parametr `as_atom` je typu bool.
    - Ověří, že parametr `mutable` je typu bool.
    - Při chybě vyvolá odpovídající validační výjimku.
    """

    if (cls.__name__ in BASE_CLASS_NAMES or
        not isinstance(as_atom, bool)):
        validate_class_is_not_base_class(cls)
        validate_param_is_bool(as_atom)
        validate_param_is_bool(mutable)