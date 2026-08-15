from dataclasses import dataclass
from typing import Any, Iterable
from simplibs.sentinels import UNSET


@dataclass(frozen=True)
class InnerValue:
    """
    Represents an update to a specific inner value.

    Path may be:
        - "age"
        - "address.city.zip"
        - ("address", "city", "zip")

    The path is normalized to tuple[str] in __post_init__.
    """

    path: str | Iterable[str]
    value: Any

    def __post_init__(self):
        # Normalize path → tuple[str]
        if isinstance(self.path, str):
            parts = self.path.split(".")
        else:
            parts = tuple(self.path)

        if not parts:
            raise ValueError("InnerValue.path cannot be empty.")

        if not all(isinstance(p, str) for p in parts):
            raise TypeError("InnerValue.path must contain only strings.")

        object.__setattr__(self, "path", tuple(parts))

    def as_instance_tuple(self, instance: Any):
        """
        Navigate through nested inner instances and return (inner_instance, value).

        If any part of the path cannot be resolved, UNSET is returned.
        """
        current = instance

        for part in self.path:
            inner_prop = f"{part}_instance"

            if not hasattr(current, inner_prop):
                return UNSET

            current = getattr(current, inner_prop)

            if current is None:
                return UNSET

        return current, self.value
