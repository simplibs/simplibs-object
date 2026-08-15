import inspect
import ast
from typing import Callable


def _extract_clean_code_lines(
    function: Callable,
) -> list[str]:
    """
    Returns cleaned code lines from the body of a function:
    - without the function header
    - without decorators
    - without docstring
    - without comments
    - each line preserved with original indentation
    """

    # 1. Retrieve source code
    source = inspect.getsource(function)

    # 2. Parse into AST
    tree = ast.parse(source)

    # 3. Locate the first function definition
    func_node = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    )

    # 4. Split source into lines
    lines = source.splitlines()

    # 5. Determine body range
    body_start = func_node.body[0].lineno - 1
    body_end = func_node.body[-1].end_lineno
    body_lines = lines[body_start:body_end]

    # 6. Remove docstring if present
    if (
        isinstance(func_node.body[0], ast.Expr)
        and isinstance(func_node.body[0].value, ast.Constant)
    ):
        docstring_end = func_node.body[0].end_lineno - func_node.body[0].lineno + 1
        body_lines = body_lines[docstring_end:]

    # 7. Clean lines
    code_line_list = []
    for line in body_lines:
        stripped = line.strip()

        if not stripped:
            continue
        if stripped.startswith("#"):
            continue

        code_line_list.append(line)

    return code_line_list


_DESIGN_NOTES = """
# extract_clean_code_lines

## Purpose
Extracts a clean, human-readable representation of the logical body of a Python
function. This is used primarily for error reporting, allowing users to see the
exact validation logic they wrote inside `_validate`.

## Behavior
- Retrieves the function’s source code using `inspect.getsource`.
- Parses the code into an AST to locate the function body.
- Removes:
  - decorators
  - the function header
  - docstring
  - comments
  - empty lines
- Preserves original indentation and formatting of logical lines.

## Notes
- Intended exclusively for user-defined validation methods (`_validate`).
- If the source code cannot be retrieved (e.g., builtins, lambdas, REPL-defined
  functions), the caller should fall back to a placeholder message.
- This function is used inside `raise_validation_error` to display the user’s
  validation logic directly in the error message.
"""