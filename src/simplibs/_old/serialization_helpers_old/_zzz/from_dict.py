def from_dict(self, data: dict, validate: bool = True, rebuild: bool = True):
    """
    Obnoví stav objektu z dictu podle serialization nodes.
    """

    nodes = self._nodes_tuple

    # 1. případná validace
    if validate:
        self._validate_dict(data)

    # 2. lineární aplikace dat na instance
    for instance, path in nodes:

        # 2.1 získání hodnoty z dictu podle cesty
        current = data

        for key in path:
            current = current[key]

        # 2.2 rozlišení kompozice vs leaf
        if isinstance(current, dict):
            value = current["_value"]
        else:
            value = current

        if validate:
            instance.validate(value)

        # 2.3 přímý zápis bez triggerů
        object.__setattr__(instance, "_value", value)

    # 3. případná finalizace / přepočet
    if rebuild:
        self.recalculate()

    return self

def from_dict2(self, data, validate=True):
    nodes = self._serialization_nodes

    if validate:
        self._validate_dict(data)

    for (instance, path) in nodes:
        value = self._extract_value(data, path)
        object.__setattr__(instance, "_value", value)

    self._finalize_import()

    # for instance, path in nodes:
    #     value = walk(user_dict, path)
    #     instance.validate(value)