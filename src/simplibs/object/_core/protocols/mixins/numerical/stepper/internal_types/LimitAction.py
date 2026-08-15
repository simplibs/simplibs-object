from typing import TypeAlias, Any, Callable


# Callback/Action triggered when hitting a limit (accepts instance/value or Unset)
LimitAction: TypeAlias = Callable[..., Any] | Any