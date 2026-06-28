

def _create_stepper_property(path: tuple[str, ...]):
    def getter(self):
        obj = self
        for attr in path:
            obj = getattr(obj, attr)
        return obj.stepper
    return property(getter)