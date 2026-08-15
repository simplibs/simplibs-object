from typing import TypeAlias, Any


# Reconstruction plan for pickle: (class, empty_args_tuple, state_dict)
PicklePlan: TypeAlias = tuple[type, tuple[()], dict[str, Any]]