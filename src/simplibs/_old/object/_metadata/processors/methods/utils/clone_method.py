from types import FunctionType

def clone_method(method):
    func = method.__func__
    new_func = FunctionType(
        func.__code__,
        func.__globals__,
        name=func.__name__,
        argdefs=func.__defaults__,
        closure=func.__closure__,
    )
    return new_func.__get__(method.__self__, method.__self__)
