UNSET = None
VALUE = "_value"
OWNER_CLASS = "_owner_class"


# noinspection PyProtectedMember
def from_dict_constants(self, user_dict: dict):

    # =========================================================
    # 1. CYKLUS SKRZE NODES
    # =========================================================
    last_composite_key = UNSET
    last_composite_dict = {}

    for instance, path in self._nodes_tuple:

        # 1.1 Definice proměnných
        current_dict = user_dict
        last_key = path[-1]

        # 1.2.2 Přeskočení kompozitních hodnot
        if last_key == VALUE:
            continue

        if len(path) > 1:

            # 1.2.1 Načtení posledního a předposledního klíče
            before_last_key = path[-2]

            # 1.2.3 Pokud se jedná o stejný slovník jako poslední
            if last_composite_key == before_last_key:
                current_dict = last_composite_dict

            # 1.2.4 Pokud se jedná o jiný slovník než poslední
            else:
                for key in path[:-1]:
                    current_dict = current_dict.get(key, UNSET)
                    if not isinstance(current_dict, dict):
                        current_dict = UNSET
                        break

                if current_dict is UNSET:
                    continue

                last_composite_key = before_last_key
                last_composite_dict = current_dict


        # 1.4 Vyhledání hodnoty - pokud není nalezena, pokračuje se dále
        value = current_dict.get(last_key, UNSET)
        if value is UNSET:
            continue

        # 1.5 Zápis hodnoty přes property (validace + přepočet)
        instance.value = value