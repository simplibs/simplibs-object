from typing import Protocol, Any, runtime_checkable, Callable


@runtime_checkable
class FunctionProtocol(Protocol):
    """
    Auxiliary protocol matching the underlying function object (__func__)
    of a bound method, providing access to function metadata and bytecode attributes.
    """
    __annotations__: dict[str, Any]
    __defaults__: tuple[Any, ...] | None
    __kwdefaults__: dict[str, Any] | None
    __code__: Any
    __globals__: dict[str, Any]
    __closure__: tuple[Any, ...]


@runtime_checkable
class ClassMethodProtocol(Protocol):
    """
    Protocol representing a bound classmethod retrieved from a definition class
    (such as user-defined `_validate`, `_logic`, or `_decompose`).

    Provides structural typing for metadata validation helpers that need access
    to the bound class (`__self__`) and underlying function (`__func__`).
    """
    __func__: FunctionProtocol
    __self__: type
    __call__: Callable[..., Any]