from typing import TypeAlias


# Reprezentuje hierarchickou sémantickou cestu k prvku (např. ("parent", "sub_node"))
PathTuple: TypeAlias = tuple[str, ... ]