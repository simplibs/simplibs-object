from typing import Any, TYPE_CHECKING
from functools import reduce
from operator import or_
from simplibs.sentinels import EMPTY, UNSET
# Inners
from .SimpleConstantMetadata import SimpleConstantMetadata
from .init_processors.default import raise_default_is_defined_in_composition
from .init_processors.type import process_type
from .init_processors.inners import process_inners
from .init_processors.methods import process_classmethod
from .instance_builders.composite_class import make_composite_class
# Annotations
if TYPE_CHECKING:
    from ..protocols.metadata import SimpleObjectMetadataProtocol
    from ..protocols.instance.core_classes import CompositeInstanceProtocol


class SimpleObjectMetadata(SimpleConstantMetadata):
    """Metadata compiler for composite nodes."""

    __slots__ = (
        "inners",
        "logic",
        "decompose",
        "inners_params_name",
        "inners_map",
        "is_decomposeable",
        "_composite_class_mutable",
        "_composite_class_immutable",
    )

    def _process_user_data(self: "SimpleObjectMetadataProtocol") -> None:
        # 1. Mark as composite
        self.is_constant = False

        # 2. Composition cannot define _default
        if "_default" in self.owner_class.__dict__:
            raise_default_is_defined_in_composition(self.owner_class)

        # 3. Process type
        self.value_type, self.value_type_name = process_type(self.owner_class)

        # 4. Process inners
        inners, node_names_set = process_inners(
            node_names_set=self.node_names_set,
            name_snake=self.name_snake,
            owner_class=self.owner_class,
        )
        self.inners = inners
        self.node_names_set.update(node_names_set)

        # 5. Build lookup maps
        self.inners_map = {inner.meta.name_snake: inner for inner in self.inners}
        self.inners_params_name = tuple(inner.meta.name_snake for inner in self.inners)

        # 6. Prepare annotations/defaults
        inners_default = tuple(inner.meta.default for inner in self.inners)
        inners_annotations = {
            inner.meta.name_snake: inner.meta.value_type
            for inner in self.inners
        }

        # 7. Process _logic
        self.logic, self.default = process_classmethod(
            method_name="_logic",
            expected_params=("cls", *self.inners_params_name),
            expected_args_params_count=1 + len(self.inners_params_name),
            expected_args_defaults=inners_default,
            expected_kwargs_defaults={},
            expected_param_types=inners_annotations,
            expected_return_type=self.value_type,
            owner_class=self.owner_class,
            return_calculated_value=True,
        )

        # 8. Process _decompose
        self.decompose = process_classmethod(
            method_name="_decompose",
            expected_params=("cls", "value"),
            expected_args_params_count=2,
            expected_args_defaults=(self.default,),
            expected_kwargs_defaults={},
            expected_param_types={"value": self.value_type},
            expected_return_type=tuple,
            owner_class=self.owner_class,
        )

        # 9. Determine decomposability
        self.is_decomposeable = (
            self.decompose is not UNSET
            and all(
                inner.meta.is_constant or inner.meta.is_decomposeable
                for inner in self.inners
            )
        )

        # 10. Process _validate
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

        # 11. Reset caches
        self._atom_class_mutable = UNSET
        self._atom_class_immutable = UNSET
        self._composite_class_mutable = UNSET
        self._composite_class_immutable = UNSET

    @property
    def composite_class_mutable(self: "SimpleObjectMetadataProtocol") -> "CompositeInstanceProtocol":
        if self._composite_class_mutable is UNSET:
            # noinspection PyAttributeOutsideInit
            self._composite_class_mutable = make_composite_class(self.owner_class.__metadata__)
        return self._composite_class_mutable

    @property
    def composite_class_immutable(self: "SimpleObjectMetadataProtocol") -> "CompositeInstanceProtocol":
        if self._composite_class_immutable is UNSET:
            # noinspection PyAttributeOutsideInit
            self._composite_class_immutable = make_composite_class(
                self.owner_class.__metadata__,
                mutable=False,
            )
        return self._composite_class_immutable


_DESIGN_NOTES = """
# SimpleObjectMetadata

## Purpose
Compiles metadata for composite nodes.  
Validates structure, processes inners, binds logic/decompose/validate methods, and
provides lazy access to compiled composite classes.

## Behavior
1. Marks the node as composite (`is_constant = False`).
2. Forbids `_default` on composite classes.
3. Processes type information.
4. Processes inners and updates the global name namespace.
5. Builds lookup maps (`inners_map`, `inners_params_name`).
6. Extracts defaults and annotations for method validation.
7. Validates and binds `_logic`.
8. Validates and binds `_decompose`.
9. Determines whether the node supports backward decomposition.
10. Validates and binds `_validate`.
11. Resets lazy caches for atom/composite classes.

## Lazy class synthesis
- `composite_class_mutable` and `composite_class_immutable` call `make_composite_class`
  on first access.
- **Important:** cache uses `EMPTY` for checking but is initialized with `UNSET`.
  This mismatch prevents caching and forces recompilation on every access.

## Notes
- Ensures deterministic structure for composite nodes.
- Guarantees strict signature alignment between inners and `_logic`.
- Provides full reactive capabilities via composite class builder.
"""