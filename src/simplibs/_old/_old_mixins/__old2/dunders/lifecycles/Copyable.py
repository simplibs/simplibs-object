# Outers
from ...common.core_logic import NodesDicts, Snapshot
# Inners
from ._utils.coppy_deepcopy import (
    mutable_copy,
    mutable_deepcopy,
    immutable_copy,
    immutable_deepcopy
)


class Copyable(NodesDicts, Snapshot):
    """
    Společný mixin pro mutable a immutbale verzy.

    Mutable lifecycle:
    - mělká kopie přes create_instance(validate=False)
    - hluboká kopie přes create_instance(validate=False)

    Immutable lifecycle:
    - mělká kopie přes snapshot
    - hluboká kopie přes deepcopy snapshotu
    """

    __slots__ = ()

    # ---------------------------------------------------------
    # 1) Mělká kopie (immutable)
    # ---------------------------------------------------------
    def __copy__(self):
        return (
            mutable_copy(self)
            if self.__is_mutable__
            else immutable_copy(self)
        )

    # ---------------------------------------------------------
    # 2) Hluboká kopie (immutable)
    # ---------------------------------------------------------
    def __deepcopy__(self, memo):
        return (
            mutable_deepcopy(self, memo)
            if self.__is_mutable__
            else immutable_deepcopy(self, memo)
        )
