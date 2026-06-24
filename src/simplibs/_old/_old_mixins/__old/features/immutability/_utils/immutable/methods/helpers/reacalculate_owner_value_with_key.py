# Inners
from .reacalculate_owner_value import reacalculate_owner_value


def reacalculate_owner_value_with_key(nodes_tuple, node_names_set_tuple, snapshot_dict, key):
    """Metoda pro dopočet pomoziční hodnoty na základě hodnot jeho innerů"""

    # Vytažení indexu
    node_index = node_names_set_tuple.index(key)

    # Vytažení instance
    instance = nodes_tuple[node_index][0]

    # Zápis nové hodnoty kompozice
    reacalculate_owner_value(snapshot_dict, instance)
