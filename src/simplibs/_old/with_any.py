from typing import Any
# Inners
from .with_constant import with_constant
from .with_composite import with_composite
from .with_constants import with_constants
from .helpers import (
    get_top_composite_paths,
    split_constants_paths,
    create_new_instance,
    create_snapshot_dict
)


def with_any(
    self,
    changes: tuple[str, Any] | tuple[tuple[str, Any], ...] | None = None
):

    instance = None

    # Pokud není zadaná žádná hodnota vrací se immutable verze stejné třídy:
    if not changes:
        instance = create_new_instance(self, self._build_snapshot())

    # zachycení nevalidní hodnoty:
    elif not isinstance(changes, tuple):
        raise ...

    # Pokud je zadaná jen jedna hodnota
    elif not isinstance(changes[0], tuple):

        # výjimka kontrolující že jsou dvě položky a první je str
        if (len(changes) != 2
            or not isinstance(changes[0], str)):
            raise ...

        # Načtení name_snake a hodnoty
        name, value = changes

        # Pokud je hodnota konstanta
        if name in self._constant_names:
            instance = with_constant(self, name, value)

        # Pokud je hodnota kompozice
        elif name in self.meta.node_names_set:
            instance = with_composite(self, name, value)

    # Pokud je zadáno více položek
    else:

        # vytvoření kontejnerů
        constants = []
        composite = []

        # Průchod skrze jednotlivé prvky
        for inner_tuple in changes:

            # Vyvolání výjimky pokud vnitřní prvek není tuple s jménem a hodnotu
            if (not isinstance(inner_tuple, tuple)
                or len(inner_tuple) != 2
                or not isinstance(inner_tuple[0], str)):
                raise ...

            # Vytažení jména
            name = inner_tuple[0]

            # Zpracování klonstanty
            if name in self._constant_names:
                constants.append(inner_tuple)

            # Zpracování kompozice
            elif name in self.meta.node_names_set:
                composite.append(inner_tuple)

            # Pokud hodnota není ani jedno - vyvolá se výjimka
            else:
                raise ...

        # Pokud byli předané pouze konstanty
        if not composite:
            instance = with_constants(self, changes)

        # Vyřízení pokud jsou zadané i kompozice
        else:

            # Vytvoření changes slovníku
            changes_dict = {key: value for key, value in changes}

            # Získání nejvíš umístěných kompozic
            comopsite_roots = get_top_composite_paths(composite, self._nodes_path_dict)

            # Vytvoření základní instance
            _instance = create_new_instance(self, self._build_snapshot())

            # Přepsání instance skrze nejvýše umístěné kompozice kompozice
            for name, _ in comopsite_roots:
                value = changes_dict[name]
                _instance = with_composite(_instance, name, value)

            # Získání slovníku snapshotu
            _instance_snapshot_dict = create_snapshot_dict(_instance._nodes_tuple)

            # Kontrola zda všechny zadané hodnoty kompozic odpovídají vypočítanému
            for name, value in composite:
                if _instance_snapshot_dict[name] != value:
                    raise ...

            # Kontrola zda mezi konstantami jsou nějaké jedinečné adresy
            contained, unique = split_constants_paths(constants, comopsite_roots, self._nodes_path_dict)

            # Kontrola zda všechny zadané hodnoty konstant odpovídají vypočítanému
            for name, _ in contained:
                value = changes_dict[name]
                if _instance_snapshot_dict[name] != value:
                    raise ...

            # Nový výpočet konečné hodnoty na základě constant
            new_changes = []
            for name, _ in unique:
                value = changes_dict[name]
                new_changes.append((name, value))
            instance = with_constants(_instance, tuple(new_changes))

    # Návrat instance a nebo hodnoty podle měnitelnosti objektu
    return instance if not self.__mutable__ else instance.value




