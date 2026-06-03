from .Bool import BoolMixin
from .Bytes import BytesMixin
from .Format import FormatMixin
from .Repr import ReprMixin
from .Str import StrMixin

__all__ = (
    "BoolMixin",
    "BytesMixin",
    "FormatMixin",
    "ReprMixin",
    "StrMixin",
)


__DOCT__ = """
# GROUP: `representation/`

> **Group purpose:**
> How an object *presents itself* to the outside world — as text, as bytes, as a boolean,
> and in formatted strings. These dunders are called by Python's built-in functions (`str()`,
> `repr()`, `format()`, `bytes()`, `bool()`) and by the REPL, `print()`, f-strings, and
> logging systems. Getting these right makes a class vastly more debuggable and usable.
"""