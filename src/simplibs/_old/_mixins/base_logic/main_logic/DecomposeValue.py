from typing import Any, Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from ...._metadata.SimpleObjectMetadata import SimpleObjectMetadata

from simplibs.exception import SimpleException


class DecomposeValue:

    meta: 'SimpleObjectMetadata'
    _decompose: Any

    @classmethod
    def decompose_value(cls, value: Any) -> Dict[str, Any]:
        """
        Decomposes an existing value into a dictionary of internal parameters.
        """

        def raise_decompose_error(problem: str, expected: str, fix: tuple[str, ...], val: Any = None):
            raise SimpleException(
                error_name="DECOMPOSITION ERROR",
                value_label=f"{cls.__name__}._decompose output",
                value=val if val is not None else value,
                expected=expected,
                problem=problem,
                how_to_fix=fix,
                context=f"Runtime decomposition of {cls.__name__} instance",
                exception=ValueError
            )


        # 0. Check if decomposition is supported
        if cls.meta.decompose is None:
            raise_decompose_error(
                problem=f"The class '{cls.__name__}' does not support decomposition.",
                expected="A defined '_decompose' method",
                fix=(
                    "Implement '@classmethod _decompose(cls, value)'.",
                    "This method must return a tuple or list of values for inner components."
                ),
                val=cls.__name__
            )


        # 0. Zkontrolovat zda je hodnota správného typu
        if not isinstance(value, cls.meta.value_type):
            raise ...


        # 1. Call decomposition
        decomposed_values = cls._decompose(value)

        # 2. Handle None (intentional skip)
        if decomposed_values is None:
            return {}

        # 3. OUTPUT TYPE CHECK
        if not isinstance(decomposed_values, (tuple, list)):
            raise_decompose_error(
                problem=f"The '_decompose' method must return values in a tuple or list.",
                expected="A tuple or a list",
                fix=(
                    "Adjust the return value of the '_decompose' method to a tuple.",
                    "Example: return (value1, value2)"
                ),
                val=type(decomposed_values).__name__
            )

        # 4. ELEMENT COUNT CHECK
        expected_count = len(cls.meta.param_names)
        if len(decomposed_values) != expected_count:
            raise_decompose_error(
                problem=f"The '_decompose' method returned {len(decomposed_values)} values, but {expected_count} are defined in '_inners'.",
                expected=f"Exactly {expected_count} values",
                fix=(
                    f"Ensure '_decompose' returns values for these parameters: {', '.join(cls.meta.param_names)}",
                    "The order of values in the tuple must match the order in '_inners'."
                ),
                val={"returned": len(decomposed_values), "expected": expected_count}
            )

        # 5. MAPPING
        return dict(zip(cls.meta.param_names, decomposed_values))
