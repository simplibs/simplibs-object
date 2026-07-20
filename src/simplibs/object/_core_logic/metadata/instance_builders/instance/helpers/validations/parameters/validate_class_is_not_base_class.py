from typing import Any, TYPE_CHECKING
# Outers
from ........exceptions import SimpleInstanceError
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_class_is_not_base_class(
    cls: "SimpleClassLike"
) -> None:
    """
    Validuje, že uživatel nepředal základní třídu Simple systému.
    """

    # Podmínka, která vede k vyvolání výjimky:
    # if cls.__name__ in BASE_CLASS_NAMES:

    if cls.__name__ in BASE_CLASS_NAMES:

        raise SimpleInstanceError(
            error_name="INVALID CLASS",
            label="Base class used instead of declarative class",
            expected="Deklarativní třídu odvozenou od SimpleBase, nikoli základní třídu.",
            value=cls,
            problem=(
                f"Třída '{cls.__name__}' je základní třídou Simple systému "
                "a nelze ji použít pro vytvoření runtime instance."
            ),
            context=f"create_instance(cls={cls.__name__})",
            how_to_fix=(
                "Použijte deklarativní třídu, kterou jste definoval pomocí Simple systému.",
                "Například:",
                "    class MyNumber(SimpleObject):",
                "        _type = int",
                "",
                "Základní třídy (SimpleObject, SimpleAtom, SimpleComposite, …) "
                "slouží pouze jako frameworkové stavební bloky."
            ),
            exception=TypeError
        )
