from typing import TypeAlias
from collections.abc import Mapping


# Indexová mapa určující přesné pořadí pozice sub-nodu v původní sekvenci
NodesIndexMap: TypeAlias = Mapping[str, int]