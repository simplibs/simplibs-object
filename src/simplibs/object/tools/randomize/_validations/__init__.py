from .raise_random_data_filler_exhausted import raise_random_data_filler_exhausted
from .validate_instance_is_simple_constant_base import validate_instance_is_simple_constant_base
from .validate_registry_is_randomize_registry_base import validate_registry_is_randomize_registry_base
from .validate_retries_is_greater_than_zero import validate_retries_is_greater_than_zero
from .validate_retries_is_int import validate_retries_is_int
from .validate_skip_immutable_is_bool import validate_skip_immutable_is_bool
from .validate_skip_unregistered_is_bool import validate_skip_unregistered_is_bool


_DESIGN_NOTES = """
# Randomize Internal Validations

## Purpose
Provides guard clause validation functions and error raisers for randomization utilities.
Note: Since this folder starts with an underscore (`_`), its components remain strictly internal.

## Internal Components Registry

| Component                                       | Type     | Description                                                               |
| :---------------------------------------------- | :------- | :------------------------------------------------------------------------ |
| `raise_random_data_filler_exhausted`            | Function | Raises a structured error when random generation runs out of retries.     |
| `validate_instance_is_simple_constant_base`     | Function | Validates that target object is an instance of `SimpleConstant`.          |
| `validate_registry_is_randomize_registry_base`  | Function | Validates that registry is `None` or an instance of `RegistryBase`.       |
| `validate_retries_is_greater_than_zero`         | Function | Validates that retry count is strictly greater than zero.                 |
| `validate_retries_is_int`                       | Function | Validates that retries parameter is an integer (and not bool).            |
| `validate_skip_immutable_is_bool`              | Function | Validates that `skip_immutable` argument is a boolean flag.               |
| `validate_skip_unregistered_is_bool`           | Function | Validates that `skip_unregistered` argument is a boolean flag.            |
"""