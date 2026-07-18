from typing import Any, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......protocols.mixins.core_mixins import InfrastructureProtocol
    from ......protocols.alias_typings import ChangesTuple



def split_changes(
    self: "InfrastructureProtocol",
    changes: "ChangesTuple"
) -> tuple["ChangesTuple", "ChangesTuple"]:
    """
    Rozdělí vstupní změny na:
        - constants: [(name, value), ...]
        - composite: [(name, value), ...]

    Zároveň provádí validaci struktury.
    """

    constants = []
    composite = []

    for inner_tuple in changes:

        # Validace struktury
        if (not isinstance(inner_tuple, tuple)
            or len(inner_tuple) != 2
            or not isinstance(inner_tuple[0], str)):
            raise ...

        name = inner_tuple[0]

        # Konstanta
        if name in self._constant_names_tuple:
            constants.append(inner_tuple)

        # Kompozice
        elif name in self.meta.node_names_set:
            composite.append(inner_tuple)

        # Neznámý název
        else:
            raise ...

    return tuple(constants), tuple(composite)
