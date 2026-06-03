import keyword
from textwrap import dedent


def make_property(
    *,
    attr_name: str,
    param_name: str,
    value_type: type,
    core_class: type,
) -> property:

    # Validace názvu
    if not param_name.isidentifier():
        raise ValueError(param_name)

    if keyword.iskeyword(param_name):
        raise ValueError(param_name)

    # Typy pro anotace
    value_type_name = value_type.__name__
    core_class_name = core_class.__name__

    # ==========================================================
    # GETTER
    # ==========================================================

    getter_source = dedent(f'''
    def getter(
        self
    ) -> {core_class_name}:
        """
        Getter pro '{param_name}'.
        """

        return self.{attr_name}
    ''')

    getter_namespace = {
        core_class_name: core_class,
    }

    exec(getter_source, getter_namespace)

    getter = getter_namespace["getter"]

    # ==========================================================
    # SETTER
    # ==========================================================

    setter_source = dedent(f'''
    def setter(
        self,
        new_value: {value_type_name} | None
    ) -> None:
        """
        Setter pro '{param_name}'.
        """

        self.{attr_name}.value = new_value

        self._on_update()
    ''')

    setter_namespace = {
        value_type_name: value_type,
    }

    exec(setter_source, setter_namespace)

    setter = setter_namespace["setter"]

    # ==========================================================
    # PROPERTY
    # ==========================================================

    return property(
        getter,
        setter,
    )