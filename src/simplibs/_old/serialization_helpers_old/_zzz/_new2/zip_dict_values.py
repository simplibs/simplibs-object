def zip_dict_values(dict1, dict2):

    result = []

    def walk(node1, node2):

        if isinstance(node1, dict):

            if not isinstance(node2, dict):
                raise ValueError("Structure mismatch")

            if node1.keys() != node2.keys():
                raise ValueError("Structure mismatch")

            for key in node1:
                walk(node1[key], node2[key])

        else:

            if isinstance(node2, dict):
                raise ValueError("Structure mismatch")


            result.append((node1, node2))

    walk(dict1, dict2)

    return tuple(result)

