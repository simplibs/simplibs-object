from simplibs.sentinels import UNSET
# Outers
from ..utils import exception_info_for_classmethod, clone_classmethod
from ....._types import SimpleClassType
# Inners
from .validations import (
    validate_row_method_is_defined,
    validate_row_method_is_callable,
    validate_row_method_is_classmethod
)


def verify_classmethod_existence(
    method_name: str,
    owner_class: SimpleClassType,
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
) -> tuple[bool, classmethod]:  # tuple[bool(má se validovat), návratový objekt]

    # 1. Příprava dat
    row_method = owner_class.__dict__.get(method_name, None)
    bound_method = getattr(owner_class, method_name)

    # 2.Kontrola zda je definovaná jako classmethod
    if isinstance(bound_method, classmethod):

        # 2.1 Vyřízení pro nově definované metody
        if row_method:
            return True, bound_method

        # 2.2 Vyřízení pro _validate (pokud se dědí nikdy se nevaliduje)
        if method_name == "_validate":
            return False, bound_method

        # 2.3 Kontrola zda se jedná o přímého potomka SimpleObject třídy
        from ....SimpleObject import SimpleObject
        is_direct_descendant = SimpleObject in owner_class.__bases__

        # 2.4 Vyřízení pro _logic a _decompose (když se nejedná o přímého potomka)
        if not is_direct_descendant:
            need_validations = bool(owner_class.__dict__.keys() & {"_inners", "_type", "_default", "_logic"})
            output_bound_method = clone_classmethod(bound_method) if need_validations else bound_method
            return need_validations, output_bound_method

        # 2.5 Vyřízení _decompose, pokud není definovaná (_logic propadává na výjimku)
        if method_name == "_decompose":
                return False, UNSET

    # 4. Vytvoření infa pro výjimky
    base_info_for_exception = exception_info_for_classmethod(
        bound_method=bound_method,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count
    )

    # 5. Provedení validací
    validate_row_method_is_defined(method_name, owner_class, base_info_for_exception)
    validate_row_method_is_callable(row_method, base_info_for_exception)
    validate_row_method_is_classmethod(row_method, base_info_for_exception)
    return False, UNSET  # Nikdy by neměl nastat

