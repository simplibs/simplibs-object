from typing import TYPE_CHECKING
from ...SimpleConstant import SimpleConstant
if TYPE_CHECKING:
    from ..._core.protocols import SimpleClassLike


def load_parameters_from_inners(inners: tuple):

    if not isinstance(inners, tuple):
        raise "Invalid param"

    params = dict()

    for inner in inners:
        if not issubclass(inner, SimpleConstant):
            raise "Unvalid inner"
        inner: "SimpleClassLike"
        params[inner.meta.name_snake] = inner.meta.default

    return params
