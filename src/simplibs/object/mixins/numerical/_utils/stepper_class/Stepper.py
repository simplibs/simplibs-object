from simplibs.sentinels import UNSET
# Outers
from ......protocols import SimpleInstanceType
# Inners
from .validations import (
    validate_instance,
    process_value,
    process_up_limit_value,
    process_down_limit_value,
    process_limit_action,
)
from .methods import do_step_up, do_step_down, do_set_value


# noinspection PyProtectedMember
class Stepper:

    __slots__ = (
        "_instance",
        "_step",
        "_up_limit",
        "_down_limit",
        "_up_limit_action",
        "_down_limit_action",
        "_value_type"
    )

    def __init__(self, instance: SimpleInstanceType):
        validate_instance(instance)
        self._instance = instance
        self._value_type = type(instance.value)
        self._step = self._value_type(1)
        self._up_limit = UNSET
        self._down_limit = UNSET
        self._up_limit_action = UNSET
        self._down_limit_action = UNSET

    # --------------------------------
    # Property - getters
    # --------------------------------
    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._step = process_value(self, value)

    @property
    def up_limit(self):
        return self._up_limit

    @property
    def down_limit(self):
        return self._down_limit

    @property
    def up_limit_action(self):
        return self._up_limit_action

    @property
    def down_limit_action(self):
        return self._down_limit_action

    # --------------------------------
    # Property - setters
    # --------------------------------
    @up_limit.setter
    def up_limit(self, value):
        self._up_limit = process_up_limit_value(self, value)

    @down_limit.setter
    def down_limit(self, value):
        self._down_limit = process_down_limit_value(self, value)

    @up_limit_action.setter
    def up_limit_action(self, value):
        self._up_limit_action = process_limit_action(self, value)

    @down_limit_action.setter
    def down_limit_action(self, value):
        self._down_limit_action = process_limit_action(self, value)

    # --------------------------------
    # Methods
    # --------------------------------
    def step_up(self, value=UNSET, *, validate=True, raise_exception=False):
        """Posune hodnotu nahoru"""
        return do_step_up(self, value, validate=validate, raise_exception=raise_exception)

    def step_down(self, value=UNSET, *, validate=True, raise_exception=False):
        """Posune hodnotu dolu"""
        return do_step_down(self, value, validate=validate, raise_exception=raise_exception)

    def set_value(self, value, *, validate=True, raise_exception=False):
        """Zapíše hodnotu - kontroluje limity"""
        return do_set_value(self, value, validate=validate, raise_exception=raise_exception)

    # --------------------------------
    # Dunders
    # --------------------------------

    def __repr__(self):
        return f"<Stepper value={self._instance.value!r} step={self._step}>"
