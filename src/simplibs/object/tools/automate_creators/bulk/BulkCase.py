from dataclasses import dataclass
from typing import Any, Callable, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Inners
from ..create_simple_object import create_simple_object
from .._validations import (
    validate_class_name_is_str,
    validate_constant_has_default,
    validate_constant_has_not_logic,
    validate_constant_has_not_decompose,
    validate_composite_has_inners,
    validate_composite_has_logic,
    validate_composite_has_not_default,
)
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassType, SimpleMixinLike


@dataclass
class BulkCase:
    """Data container representing a single definition blueprint for bulk object generation.

    Validates initial specification boundaries during initialization and serves as a
    factory runner forwarding stored configuration parameters to ``create_simple_object``.
    """

    class_name: str
    default: Any | UnsetType = UNSET
    inners: tuple["SimpleClassType", ...] | UnsetType = UNSET
    value_type: type | UnsetType = UNSET
    validate: Callable | UnsetType = UNSET
    logic: Callable | UnsetType = UNSET
    decompose: Callable | UnsetType = UNSET
    return_instance: bool = False
    mixins: tuple["SimpleMixinLike", ...] = ()
    as_atom: bool = False
    mutable: bool = True

    def __post_init__(self) -> None:
        """Validates parameter constraints upon dataclass initialization."""

        # 1. Validate class_name strictly as non-empty string
        validate_class_name_is_str(self.class_name)

        # 2. Leaf constant definition checks
        if self.inners is UNSET:
            validate_constant_has_default(self.class_name, self.default)
            validate_constant_has_not_logic(self.class_name, self.logic)
            validate_constant_has_not_decompose(self.class_name, self.decompose)

        # 3. Composite object definition checks
        else:
            validate_composite_has_inners(self.class_name, self.inners)
            validate_composite_has_logic(self.class_name, self.logic)
            validate_composite_has_not_default(self.class_name, self.default)

    def create_simple_object(self) -> Any:
        """Executes object creation using the encapsulated parameters.

        Returns:
            Dynamically created Simple class blueprint, or initialized instance if return_instance=True.
        """
        return create_simple_object(
            class_name=self.class_name,
            default=self.default,
            inners=self.inners,
            value_type=self.value_type,
            validate=self.validate,
            logic=self.logic,
            decompose=self.decompose,
            return_instance=self.return_instance,
            mixins=self.mixins,
            as_atom=self.as_atom,
            mutable=self.mutable,
        )


_DESIGN_NOTES = """
# BulkCase (Bulk Definition Specification Container)

## Purpose
Acts as an explicit structural container (data object) representing a target `SimpleConstant` 
or `SimpleObject` definition for bulk dynamic generation workflows.

## Post-Initialization Validation Rules
1. **Class Name:** Enforces non-empty string via `validate_class_name_is_str`.
2. **Leaf Node (`inners` is UNSET):**
   - Must provide concrete non-None default (`validate_constant_has_default`).
   - Must NOT supply `logic` (`validate_constant_has_not_logic`).
   - Must NOT supply `decompose` (`validate_constant_has_not_decompose`).
3. **Composite Node (`inners` is supplied):**
   - Must supply non-empty `inners` tuple (`validate_composite_has_inners`).
   - Must supply calculation `logic` (`validate_composite_has_logic`).
   - Must NOT supply `default` (`validate_composite_has_not_default`).

## Execution
- `create_simple_object()` acts as a runner forwarding stored configuration arguments 
  directly to the orchestrator facade.
"""