import copy as _copy
# Outers
from .....immutable.state._utils.immutable_methods.helpers.common import create_new_instance


def immutable_deepcopy(self, memo):
    snapshot = tuple(
        _copy.deepcopy(v, memo)
        for v in self._build_snapshot()
    )
    return create_new_instance(self, snapshot)