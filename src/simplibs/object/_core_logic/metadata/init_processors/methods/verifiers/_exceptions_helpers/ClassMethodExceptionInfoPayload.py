from typing import TypedDict


class ClassMethodExceptionInfoPayload(TypedDict):
    """Precise structural type definition describing every field inside the generated diagnostic metadata payload."""
    class_name: str
    method_name: str
    expected_structure: tuple[str, ...]
    context: str