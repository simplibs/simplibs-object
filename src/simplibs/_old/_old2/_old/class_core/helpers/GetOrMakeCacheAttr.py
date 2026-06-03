from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from ...._metadata.SimpleObjectMetadata import SimpleObjectMetadata

from simplibs.exception import SimpleException


class GetOrMakeCacheAttr:
    """Mixin pro automatickou správu cache v metadatech."""

    meta: 'SimpleObjectMetadata'


    @classmethod
    def _get_or_make_cache_attr(cls, cache_attr: str, method_name: str) -> Any:
        """
        Univerzální logika pro cache:
        Pokud hodnota v metadatech chybí, vyrobí ji a uloží.
        """

        # 1. Kontrola existence atributu v metadatech
        if not hasattr(cls.meta, cache_attr):
            raise SimpleException(
                error_name="CACHE ATTRIBUTE ERROR",
                value_label="cache_attr",
                value=cache_attr,
                expected="A valid attribute name in 'SimpleObjectMetadata'",
                problem=f"The metadata object does not contain a defined slot for cache '{cache_attr}'.",
                how_to_fix=(
                    "Check the '__slots__' definition in 'SimpleObjectMetadata'.",
                    f"Ensure the parameter name '{cache_attr}' in the mixin call is spelled correctly."
                ),
                context=f"Metadata storage validation for {cls.__name__}",
                exception=AttributeError
            )

        # 2. Zkusíme vytáhnout z cache
        cached_val = getattr(cls.meta, cache_attr)

        if cached_val is not None:
            return cached_val

        # 3. Pokud není, zavoláme výrobnu
        if not hasattr(cls, method_name):
            raise SimpleException(
                error_name="MISSING METHOD ERROR",
                value_label="method_name",
                value=method_name,
                expected=f"A defined factory method in class {cls.__name__}",
                problem=f"The class is missing the required factory method '{method_name}' to populate the cache.",
                how_to_fix=(
                    f"Implement '@classmethod {method_name}' within the '{cls.__name__}' class.",
                    "This method must return the object (e.g., a validator or logic instance) to be cached."
                ),
                context=f"Factory method validation for {cls.__name__}",
                exception=AttributeError
            )
        factory_method = getattr(cls, method_name)
        new_class = factory_method()

        # 4. Uložíme do cache v metadatech
        setattr(cls.meta, cache_attr, new_class)
        return new_class