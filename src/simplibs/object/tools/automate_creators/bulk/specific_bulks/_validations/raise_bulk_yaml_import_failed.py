from typing import NoReturn
from ......exceptions import SimpleRuntimeError


def raise_bulk_yaml_import_failed() -> None | NoReturn:
    """Raises SimpleRuntimeError when PyYAML package is missing during YAML parsing."""

    raise SimpleRuntimeError(
        error_name="BULK YAML MISSING DEPENDENCY ERROR",
        label="bulk_yaml_import_failed",
        expected="Installed 'pyyaml' package in the python environment",
        value="ModuleNotFoundError: yaml",
        problem=(
            "Cannot execute bulk creation from YAML because the 'PyYAML' library is not installed."
        ),
        context="Attempted to invoke 'create_simple_object_bulk_from_yaml'.",
        how_to_fix=(
            "Install the PyYAML library using pip: 'pip install pyyaml'.",
            "Alternatively, use JSON, CSV, or python dictionary runners which do not require external dependencies.",
        ),
        exception=ImportError,
    )