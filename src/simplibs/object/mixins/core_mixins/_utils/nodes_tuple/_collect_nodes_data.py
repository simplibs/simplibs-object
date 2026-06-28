from typing import TYPE_CHECKING
# Outers
from ...._common.constants import VALUE
# Annotations
if TYPE_CHECKING:
    from .....protocols.instance import SimpleInstanceLike
    from .....protocols.alias_typings import PathTuple, NodeItem


def _collect_nodes_data(
    instance: "SimpleInstanceLike",
    path: "PathTuple",
    nodes_list: list["NodeItem"]
) -> None:
    """
    Rekurzivně projde celou strukturu a vytvoří
    seznam dvojic:

        (instance, path)
    """

    # 1. Přidání aktuálního uzlu (konstanta)
    if instance.meta.is_constant:
        nodes_list.append((instance, path))
        return

    # 2. Přidání aktuálního uzlu (kompozice)
    else:
        nodes_list.append((instance, path + (VALUE,)))

    # 3. Zpracování kompozice (cyklus skrze inners)
    for inner in instance.meta.inners:

        # 3.1 Vytvoření proměnné meta
        inner_meta = inner.meta

        # 3.2 Načtení instance
        inner_instance = getattr(
            instance,
            inner_meta.name_private
        )

        # 3.3 Rekurzní volání pro další vnoření
        _collect_nodes_data(
            instance=inner_instance,
            path=path + (inner_meta.name_snake,),
            nodes_list=nodes_list
        )