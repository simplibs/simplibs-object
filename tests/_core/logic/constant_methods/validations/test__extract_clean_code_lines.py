from simplibs.object._core.logic.constant_methods.validations._extract_clean_code_lines import (
    _extract_clean_code_lines,
)


def target_function_with_docstring_and_comments(value: int) -> bool:
    """This is a dummy docstring.

    Multi-line explanation here.
    """
    # Comment line to be stripped
    result = value > 10  # Inline comment preserved on code line

    if result:
        # Inner comment
        return True

    return False


def test_extract_clean_code_lines() -> None:
    """Test that function body is cleaned of headers, docstrings, and standalone comment lines."""

    lines = _extract_clean_code_lines(target_function_with_docstring_and_comments)

    expected_lines = [
        "    result = value > 10  # Inline comment preserved on code line",
        "    if result:",
        "        return True",
        "    return False",
    ]

    assert lines == expected_lines