from typing import Protocol, runtime_checkable, TYPE_CHECKING
if TYPE_CHECKING:
    from ..alias_typings import MixinsTuple


@runtime_checkable
class SimpleInstanceBaseProtocol(
    Protocol
):
    """
    Root protocol for all runtime instances in the Simple system.

    It can be based on ConstantInstanceProtocol when constructed as a constant,
    or on CompositeInstanceProtocol when constructed as a composite object.
    (The larger element is referenced here to cover all variants.)

    Encompasses common technical dunders injected by the `create_instance` factory
    and guarantees the presence of the core instance interface.
    """

    # --- TECHNICAL ATTRIBUTES (Injected by the create_instance factory) ---
    __is_constant__: bool
    __is_mutable__: bool
    __mixins__: "MixinsTuple"