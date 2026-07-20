from .SimpleError import SimpleError


class SimpleInstanceError(SimpleError):
    """Exception for errors occurring during the instantiation of the final object."""


_DESIGN_NOTES = """
# SimpleInstanceError

## Purpose
An exception designed for errors occurring during the instantiation phase of the final object. It inherits from `SimpleError`, allowing it to be caught under the main library umbrella exception.

## Logic
This exception is typically raised when creating a runtime instance of a `SimpleConstant` or `SimpleObject`. It covers situations where the class structure and metadata are perfectly valid, but the arguments passed during instantiation fail to meet the required criteria or constraints.
"""