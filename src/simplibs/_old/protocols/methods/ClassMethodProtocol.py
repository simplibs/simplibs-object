from typing import Protocol, Any, Callable, runtime_checkable


@runtime_checkable
class FunctionProtocol(Protocol):
    __annotations__: dict[str, Any]
    __defaults__: tuple[Any, ...] | None
    __kwdefaults__: dict[str, Any] | None
    __code__: Any
    __globals__: dict[str, Any]
    __closure__: tuple[Any]


@runtime_checkable
class ClassMethodProtocol(Protocol):
    __func__: FunctionProtocol
    __self__: type
    __call__: Callable[..., Any]

