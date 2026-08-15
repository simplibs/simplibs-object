from typing import TypeVar, ParamSpec, Protocol
# Outers
from ..classes import SimpleObjectProtocol


# Type variables for signature transfer magic
# (MUST be directly present at runtime)
P = ParamSpec("P")
R = TypeVar("R")


class LogicSignature(Protocol[P, R]):
    """
    Protocol stating: I am a class that has a _logic method with parameters P and return type R.
    Serves as a type anchor for decorators and calculation methods propagating signatures.
    """

    @classmethod
    def _logic(cls, *args: P.args, **kwargs: P.kwargs) -> R:
        ...