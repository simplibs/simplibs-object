from typing import Callable, Any


# Reconstruction plan for pickle: (class, empty_args_tuple, state_dict)
PicklePlan = tuple[Callable[..., Any], tuple[Any, ...]]