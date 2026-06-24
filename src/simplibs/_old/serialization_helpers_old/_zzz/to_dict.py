def _to_dict(self, structure_only: bool = False):

    # 1. Definice proměnných
    result = {}
    last_created_key = None

    # 2. Cyklus na položky snapshotu
    for instance, path in self._nodes_tuple:

        # 2.1 Načtení hodnoty z instance
        value = instance._value

        # 2.2 Vyřízení kořenové hodnoty
        if not path:
            result["_value"] = value if not structure_only else instance
            continue

        # 2.3 Vyřízení pro jeden prvek
        if len(path) == 1:
            key = path[0]
            result[key] = value if not structure_only else instance
            last_created_key = key
            continue

        # 2.4 Kontrola zda vytváříme vnitřní slovník
        is_same_key = path[-2] == last_created_key

        # 2.5 Vyřízení pro nově založený vnitřní slovník
        if is_same_key:

            # 2.5.1 Definice proměnných
            parent_key = path[-2]
            new_key = path[-1]

            # 2.5.2 Načtení poslední hodnoty
            current = result
            for key in path[:-2]:
                current = current[key]
            previous_value = current[parent_key]

            # 2.5.3 Přepis hodnoty na dict
            current[parent_key] = {
                "_value": previous_value,
                new_key: value if not structure_only else instance
            }
            last_created_key = new_key

        # 2.6 Vyřízení popožky odkazující na hodnotu
        else:

            # 2.6.2 Načtení poslední položky
            current = result
            for key in path[:-1]:
                current = current.setdefault(key, {})

            # Zápis nové položky s hodnotou
            key = path[-1]
            current[key] = value if not structure_only else instance
            last_created_key = key

    return result


def to_dict(self):
    return _to_dict(self)

def build_structure_dict(self):
    return _to_dict(self, structure_only=True)