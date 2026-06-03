from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from ...._metadata.SimpleObjectMetadata import SimpleObjectMetadata


class CreateMixinParameters:

    meta: 'SimpleObjectMetadata'
    _get_or_make_cache_attr: Callable

    @classmethod
    def MIXIN_PARAMS(cls):
        """Cachovaná brána k parametrům."""
        # Využijeme tvou logiku pro cache v metadatech
        return cls._get_or_make_cache_attr(
            cache_attr="mixin_parameters",
            method_name="collect_mixin_parameters"
        )


    @classmethod
    def collect_mixin_parameters(cls):
        mixin_parameters = [cls.meta.atom_param_signature]
        for inner in cls.meta.inners:
            mixin_parameters.extend(inner.collect_mixin_parameter())
        return mixin_parameters

