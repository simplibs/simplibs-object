def calculate_default(logic, params):
    try:
        cls = None
        return logic(cls, *params)
    except Exception as e:
        raise "nevalidní operace"