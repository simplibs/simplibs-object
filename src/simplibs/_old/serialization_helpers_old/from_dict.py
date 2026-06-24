UNSET = None
VALUE = "_value"
OWNER_CLASS = "_owner_class"

# noinspection PyProtectedMember
def from_dict(self, user_dict: dict):

    # =========================================================
    # 1. VALIDACE OWNER CLASS
    # =========================================================
    # 1. Validace zda je dict pro správnou třídu
    owner_class = user_dict.get(OWNER_CLASS, UNSET)
    if self.meta.owner_class != owner_class:
        raise ValueError("Owner class mismatch")

    # =========================================================
    # 2. FIRST PASS (collect values only)
    # =========================================================
    # 2. Vytvoření porměných
    values = []
    last_composite_key = UNSET
    last_composite_dict = {}

    # 3. Cyklus dle pořadí node tuple
    for instance, path in self._nodes_tuple:

        # -----------------------------------------------------
        # root value
        # -----------------------------------------------------
        # 3.1 Vyřízení kořenových položek
        if len(path) == 1:
            value = user_dict.get(path[0], UNSET)
            if value is UNSET:
                raise KeyError(f"Missing key: {path[0]}")
            values.append(value)
            continue

        # 3.2 Načtení posledního a předposledního klíče
        parent_key = path[-2]
        last_key = path[-1]

        # -----------------------------------------------------
        # FAST PATH (cached composite)
        # -----------------------------------------------------
        # 3.3 Zápis do stejného kompozitního slovníku
        if last_composite_key == parent_key:
            value = last_composite_dict.get(last_key, UNSET)
            if value is UNSET:
                raise KeyError(f"Missing key: {path}")
            values.append(value)

        # -----------------------------------------------------
        # SLOW PATH (full traversal)
        # -----------------------------------------------------
        # 3.4 Vytvoření nového pole
        else:

            # vyhledání předposlední hodnoty
            current_dict = user_dict
            for key in path[:-1]:
                current_dict = current_dict.get(key, UNSET)
                if current_dict is UNSET:
                    raise KeyError(f"Missing key: {key}")
                if not isinstance(current_dict, dict):
                    raise KeyError(f"Invalid structure at {key}")

            value = current_dict.get(last_key, UNSET)
            if value is UNSET:
                raise KeyError(f"Missing key: {path}")
            values.append(value)

            # 2.6 Kontrola zda se jedná o kompozici
            if last_key == VALUE:
                last_composite_key = parent_key
                last_composite_dict = current_dict

    # =========================================================
    # 3. SECOND PASS (apply values)
    # =========================================================
    # 4. Druhý cyklus na zápis hodnot
    for (instance, _), value in zip(self._nodes_tuple, values):
        instance.validate(value)
        instance._value = value