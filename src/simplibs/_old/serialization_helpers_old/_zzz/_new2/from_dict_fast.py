def from_dict_fast(self, resived_dict):

    default_dict = self._structure_dict

    result = []

    def walk(resived_dict_data, default_dict_data):

        if isinstance(resived_dict_data, dict):

            if not isinstance(default_dict_data, dict):
                raise ValueError("Structure mismatch")

            if resived_dict_data.keys() != default_dict_data.keys():
                raise ValueError("Structure mismatch")

            for key in resived_dict_data:
                walk(resived_dict_data[key], default_dict_data[key])

        else:

            if isinstance(default_dict_data, dict):
                raise ValueError("Structure mismatch")

            default_dict_data.validation(resived_dict_data)
            result.append((resived_dict_data, default_dict_data))

    walk(resived_dict, default_dict)

    for value, instance in result:
        # object.__setattr__(instance, "_value", value)
        instance._value = value

    _log_this()