class ValueStepperMixin(SimpleMixin):
    __slots__ = ("_value_step", "_limit_up", "_limit_down")

    def init_mixins(self):
        super().init_mixins()

        # Ověření typu — atom nebo decomposeable kompozice s numeric typem
        value_type = self.meta.value_type
        is_numeric = value_type in (int, float)
        is_valid_composite = (
            not self.meta.is_constant and
            self.meta.is_decomposeable and
            is_numeric
        )

        if not is_numeric and not is_valid_composite:
            raise TypeError(
                f"ValueStepperMixin requires numeric value_type (int or float), "
                f"got {value_type}. For composites, is_decomposeable must be True."
            )

        default = getattr(self, "_default_state", None)
        default_value = default._value if default else self.value

        object.__setattr__(self, "_value_step", default_value)
        object.__setattr__(self, "_limit_up", None)
        object.__setattr__(self, "_limit_down", None)

    # -----------------------------
    # Step konfigurace
    # -----------------------------
    @property
    def value_step(self):
        return self._value_step

    @value_step.setter
    def value_step(self, step):
        if not isinstance(step, (int, float)):
            raise TypeError("value_step must be numeric")
        object.__setattr__(self, "_value_step", step)

    # -----------------------------
    # Limity
    # -----------------------------
    def set_up_limit(self, limit, action=None):
        object.__setattr__(self, "_limit_up", (limit, action))

    def set_down_limit(self, limit, action=None):
        object.__setattr__(self, "_limit_down", (limit, action))

    # -----------------------------
    # Stepování
    # -----------------------------
    def value_up(self):
        new_value = self._apply_limits(self.value + self._value_step)
        self.value = new_value

    def value_down(self):
        new_value = self._apply_limits(self.value - self._value_step)
        self.value = new_value

    # -----------------------------
    # Limity
    # -----------------------------
    def _apply_limits(self, new_value):
        if self._limit_up and new_value > self._limit_up[0]:
            limit, action = self._limit_up
            if action:
                action(self)
            return limit  # ← správně vrací limit

        if self._limit_down and new_value < self._limit_down[0]:
            limit, action = self._limit_down
            if action:
                action(self)
            return limit  # ← správně vrací limit

        return new_value

