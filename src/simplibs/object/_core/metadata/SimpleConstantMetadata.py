from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .SimpleBaseMetadata import SimpleBaseMetadata
from .init_processors.type import process_type
from .init_processors.default import process_default_for_constant
from .init_processors.methods import process_classmethod
from .instance_builders.atom_class import make_atom_class
# Annotations
if TYPE_CHECKING:
    from ..protocols.metadata import SimpleConstantMetadataProtocol
    from ..protocols.instance.core_classes import AtomInstanceProtocol


class SimpleConstantMetadata(SimpleBaseMetadata):
    """Metadata compiler for constant (atomic) values."""

    __slots__ = (
        "value_type",
        "default",
        "validate",
        "value_type_name",
        "is_constant",
        "_atom_class_mutable",
        "_atom_class_immutable",
    )

    def _process_user_data(self: "SimpleConstantMetadataProtocol") -> None:
        # 1. Mark as constant
        self.is_constant = True

        # 2. Resolve type
        self.value_type, self.value_type_name = process_type(
            owner_class=self.owner_class
        )

        # 3. Resolve default
        self.default = process_default_for_constant(
            default_type=self.value_type,
            owner_class=self.owner_class,
        )

        # 4. Process _validate method
        self.validate = process_classmethod(
            method_name="_validate",
            expected_params=("cls", "value", "return_bool"),
            expected_args_params_count=2,
            expected_args_defaults=(),
            expected_kwargs_defaults={"return_bool": False},
            expected_param_types={"value": Any, "return_bool": bool},
            expected_return_type=bool | None,
            test_value=(self.default,),
            owner_class=self.owner_class,
        )

        # 5. Lazy cache initialization
        self._atom_class_mutable = UNSET
        self._atom_class_immutable = UNSET

    @property
    def atom_class_mutable(self: "SimpleConstantMetadataProtocol") -> "AtomInstanceProtocol":
        if self._atom_class_mutable is UNSET:
            # noinspection PyAttributeOutsideInit
            self._atom_class_mutable = make_atom_class(self.owner_class.__metadata__)
        return self._atom_class_mutable

    @property
    def atom_class_immutable(self: "SimpleConstantMetadataProtocol") -> "AtomInstanceProtocol":
        if self._atom_class_immutable is UNSET:
            # noinspection PyAttributeOutsideInit
            self._atom_class_immutable = make_atom_class(
                self.owner_class.__metadata__,
                mutable=False,
            )
        return self._atom_class_immutable



_DESIGN_NOTES = """
# SimpleConstantMetadata

## Purpose
Compiles constant metadata into a strict runtime specification:
- type,
- default value,
- validation method,
- atomic instance classes.

## Behavior

### 1. Type resolution
`process_type` extracts and normalizes the `_type` definition.

### 2. Default resolution
`process_default_for_constant` ensures the default matches the resolved type.

### 3. Validation method
`process_classmethod` verifies the `_validate` method signature and performs a
dry-run using the default value.

### 4. Lazy atom class creation
Atomic classes (mutable and immutable) are created only when needed using
`make_atom_class`. This reduces initialization overhead for large metadata graphs.

## Notes
This class is part of the public metadata API and is used by both constants and
composition metadata.
"""