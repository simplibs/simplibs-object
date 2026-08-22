from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators.bulk.specific_bulks._validations.raise_bulk_yaml_import_failed import (
    raise_bulk_yaml_import_failed,
)


def test_raise_bulk_yaml_import_failed(subtests) -> None:
    """Tests that raise_bulk_yaml_import_failed raises SimpleRuntimeError when PyYAML is missing."""
    assert_exception_function(
        subtests,
        raise_bulk_yaml_import_failed,
        invalid_params=(),
        exception_type=SimpleRuntimeError,
        error_name="BULK YAML MISSING DEPENDENCY ERROR",
        label="bulk_yaml_import_failed",
        value="ModuleNotFoundError: yaml",
        expected="Installed 'pyyaml' package in the python environment",
        problem="Cannot execute bulk creation from YAML because the 'PyYAML' library is not installed.",
        context="Attempted to invoke 'create_simple_object_bulk_from_yaml'.",
        how_to_fix=(
            "Install the PyYAML library using pip: 'pip install pyyaml'.",
            "Alternatively, use JSON, CSV, or python dictionary runners which do not require external dependencies.",
        ),
        exception=ImportError,
        verbose=False,
    )