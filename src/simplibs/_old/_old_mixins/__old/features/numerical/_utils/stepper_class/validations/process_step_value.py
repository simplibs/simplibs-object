from simplibs.sentinels import UNSET
# Inners
from .process_value import process_value


def process_step_value(self, value=UNSET, *, validate=True):
    return (
        self._step if value is UNSET
        else process_value(self, value, validate=validate)
    )