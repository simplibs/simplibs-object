import inspect
import ast
from typing import Callable

def extract_clean_code_lines(
    function: Callable
) -> list[str]:
    """
    Vrátí čisté řádky kódu z těla funkce:
    - bez hlavičky
    - bez dekorátorů
    - bez docstringu
    - bez komentářů
    - každý řádek jako samostatný string
    """

    # 1. Získání zdrojového kódu
    source = inspect.getsource(function)

    # 2. Parse do AST
    tree = ast.parse(source)

    # 3. Najdeme první funkci v AST
    func_node = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    )

    # 4. Získáme řádky zdrojáku jako list
    lines = source.splitlines()

    # 5. Určíme rozsah těla funkce
    body_start = func_node.body[0].lineno - 1
    body_end = func_node.body[-1].end_lineno

    body_lines = lines[body_start:body_end]

    # 6. Odstraníme docstring (pokud existuje)
    if (
        isinstance(func_node.body[0], ast.Expr) and
        isinstance(func_node.body[0].value, ast.Constant)
    ):
        docstring_end = func_node.body[0].end_lineno - func_node.body[0].lineno + 1
        body_lines = body_lines[docstring_end:]

    # 7. Očistíme řádky:
    code_line_list = []
    for line in body_lines:
        stripped = line.strip()

        # přeskočíme prázdné řádky
        if not stripped:
            continue

        # přeskočíme komentáře a returny
        if stripped.startswith("#"):
            continue

        code_line_list.append(line)

    return code_line_list
