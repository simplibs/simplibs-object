# Outers
from .....immutable.state._utils.immutable_methods.helpers.common import create_new_instance


def immutable_copy(self):
    snapshot = self._build_snapshot()
    return create_new_instance(self, snapshot)