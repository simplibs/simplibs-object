import copy as _copy
# Outers
from ....._metadata.instance_builders.instance import create_instance



class LifecycleImmutableMixin:
    """
    Immutable lifecycle:
    - mělká kopie přes snapshot
    - hluboká kopie přes deepcopy snapshotu
    """

    __slots__ = ()

    # ---------------------------------------------------------
    # 1) Mělká kopie (immutable)
    # ---------------------------------------------------------
    def __copy__(self):
        snapshot = self._build_snapshot()
        return create_new_instance(self, snapshot)

    # ---------------------------------------------------------
    # 2) Hluboká kopie (immutable)
    # ---------------------------------------------------------
    def __deepcopy__(self, memo):
        snapshot = tuple(
            _copy.deepcopy(v, memo)
            for v in self._build_snapshot()
        )
        return create_new_instance(self, snapshot)
