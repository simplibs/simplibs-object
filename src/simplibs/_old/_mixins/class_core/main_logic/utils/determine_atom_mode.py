from typing import Type, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .....SimpleObject import SimpleObject

from simplibs.exception import SimpleException


def determine_atom_mode(cls: Type['SimpleObject'], as_atom: Optional[bool] = None) -> bool:
    """Decides whether the object should behave as an atom or a composite."""
    has_inners = bool(cls.meta.inners)
    has_decompose = cls.meta.decompose is not None

    # 1. Automatic mode (default)
    if as_atom is None:
        return not has_inners

    # 2. Forced Atom
    if as_atom is True:
        return True

    # 3. Forced Composition (as_atom=False)
    if as_atom is False:
        if not has_inners:
            raise SimpleException(
                error_name="MODE CONFIGURATION ERROR",
                value_label="as_atom",
                value=as_atom,
                expected="A class with defined '_inners'",
                problem=f"Class '{cls.__name__}' has no defined internal components, so it cannot be created as a composition.",
                how_to_fix=(
                    "Remove the 'as_atom=False' parameter to use the default atomic mode.",
                    "Define internal components in the '_inners' attribute of the class."
                ),
                context=f"Mode selection for {cls.__name__}",
                exception=ValueError
            )

        if not has_decompose:
            raise SimpleException(
                error_name="DECOMPOSITION ERROR",
                value_label="as_atom",
                value=as_atom,
                expected="A class with a defined '_decompose' method",
                problem=f"Class '{cls.__name__}' requires a decomposition logic to function in composite mode.",
                how_to_fix=(
                    "Implement the '@classmethod _decompose(cls, value)' method.",
                    "Alternatively, allow the object to function as an atom by removing 'as_atom=False'."
                ),
                context=f"Forced composite mode validation for {cls.__name__}",
                exception=AttributeError
            )
        return False

    # 4. Invalid Type check
    raise SimpleException(
        error_name="TYPE ERROR",
        value_label="as_atom",
        value=type(as_atom).__name__,
        expected="bool or None",
        problem=f"The 'as_atom' parameter received an invalid type: '{type(as_atom).__name__}'.",
        how_to_fix=("Pass only 'True', 'False', or 'None' (default) to the 'as_atom' parameter.",),
        context="Parameter type validation in OBJECT factory",
        exception=TypeError
    )