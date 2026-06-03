# class InPlaceNumeric(IaddMixin, IsubMixin, ImulMixin, IdivMixin, IfloordivMixin, ImodMixin, IpowMixin):
#     """Podporuje +=, -=, *=, /=, //=, %=, **="""
#     __slots__ = ()

from .atoms import (
    IaddMixin,
    IsubMixin,
    ImulMixin,
    IdivMixin,
    IfloordivMixin,
    ImodMixin,
    IpowMixin,
)


class InPlaceNumericMixin(
    IaddMixin,
    IsubMixin,
    ImulMixin,
    IdivMixin,
    IfloordivMixin,
    ImodMixin,
    IpowMixin,
):
    """Podporuje +=, -=, *=, /=, //=, %=, **="""
    __slots__ = ()


IaddIsubImulIdivIfloordivImodIpowMixin = InPlaceNumericMixin
