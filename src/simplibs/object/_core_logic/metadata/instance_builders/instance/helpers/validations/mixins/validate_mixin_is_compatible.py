from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike
    from ........protocols.mixins.base_class import SimpleMixinProtocol


def validate_mixin_is_compatible(
    cls: "SimpleClassLike",
    mixin: "SimpleMixinProtocol",
    is_atom: bool
) -> None:
    """
    Validuje, že mixin je kompatibilní s režimem Atom/Composite.
    """

    # Podmínka, která vede k vyvolání výjimky:
    # if is_atom and getattr(mixin, "_composite_only", False):

    if is_atom and getattr(mixin, "_composite_only", False):

        raise SimpleMixinError(
            error_name="INCOMPATIBLE MIXIN",
            label="Mixin incompatible with Atom mode",
            expected="Mixin, který lze použít i v Atom režimu.",
            value=mixin,
            problem=(
                f"Mixin '{mixin.__name__}' je označen jako '_composite_only', "
                "a proto jej nelze použít při vytváření Atom instance "
                f"třídy '{cls.__name__}'."
            ),
            context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
            how_to_fix=(
                "Použijte tento mixin pouze v Composite režimu.",
                "Příklad:",
                "    create_instance(MyClass, mixins=(MyCompositeMixin,), as_atom=False)",
                "",
                "Pokud má být mixin použitelný i pro Atom instance, odstraňte "
                "atribut '_composite_only = True'."
            ),
            exception=TypeError
        )
