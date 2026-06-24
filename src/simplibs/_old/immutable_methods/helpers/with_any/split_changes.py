from typing import Any


def split_changes(self, changes: tuple[tuple[str, Any], ...]):
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
        if name in self._constant_names:
            constants.append(inner_tuple)

        # Kompozice
        elif name in self.meta.node_names_set:
            composite.append(inner_tuple)

        # Neznámý název
        else:
            raise ...

    return constants, composite
