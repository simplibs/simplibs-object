def validate_structure2(expected_dict, input_dict):
    def _walk(expected, actual, path=()):

        # 1. typová shoda
        if type(expected) is dict:
            if not isinstance(actual, dict):
                raise TypeError(f"Structure mismatch at {path}")

            # 2. klíče musí být stejné (včetně pořadí)
            if list(expected.keys()) != list(actual.keys()):
                raise ValueError(f"Key/order mismatch at {path}")

            # 3. rekurze přes klíče
            for k in expected.keys():
                _walk(expected[k], actual[k], path + (k,))

        else:
            # leaf node
            return

    _walk(expected_dict, input_dict)

def validate_object_is_dict(input_dict):
    if not isinstance(input_dict, dict):
        raise ...

def validate_dict_structure(expected_dict, input_dict):
    # Zde už vím že jsou oba slovníky

    for key1, value1, key2, value2 in zip(expected_dict.items(), input_dict.items()):

        # Kontrola klíčů
        if not key1 == key2:
            raise ...

        if isinstance(value1, dict):

            if not isinstance(value2, dict):
                raise ...

            validate_dict_structure(value1, value2)