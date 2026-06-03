# Inners
from .utils import convert_annotation_to_type_set
from .validations import validate_method_annotation_is_valid_type


def process_bound_method_annotations(
    expected_param_types: dict[str, type],
    expected_return_type: type,
    bound_method: classmethod,
):

    # 1. Příprava dat
    method_annotations = bound_method.__func__.__annotations__ or {}
    expected_annotations = expected_param_types
    expected_annotations["result"] = expected_return_type

    # 2. Validace
    if method_annotations:

        # 2.1 Cyklus skrze uvedené anotace
        for name, annotation in method_annotations.items():

            # 2.2 Načtení očekávané anotace
            # (převod na sets, kuli UnionType)
            expected_type = expected_annotations.get(name)
            expected_type_set = convert_annotation_to_type_set(expected_type)
            annotation_set = convert_annotation_to_type_set(annotation)

            # 2.3 Kontrola zda anotace je uvedena v očekávaném
            if not annotation_set.issubset(expected_type_set):
                validate_method_annotation_is_valid_type(annotation_set, expected_type_set, bound_method)

    # 3. Zápis
    final_annotations = {
        **expected_annotations,
        **method_annotations,
    }

    # 4. Návrat finálního slovníku
    return final_annotations