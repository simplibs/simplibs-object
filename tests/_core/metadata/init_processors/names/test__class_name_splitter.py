from .validations import (
    validate_class_name_is_identifier,
    validate_class_name_is_ascii,
    validate_class_name_has_no_underscores,
)


def _class_name_splitter(
    class_name: str
) -> tuple[str, ...]:
    """Splits a PascalCase class name into semantic words."""

    # 1. Validate class name
    if (
        not class_name.isidentifier()
        or not class_name.isascii()
        or "_" in class_name
    ):
        validate_class_name_is_identifier(class_name)
        validate_class_name_is_ascii(class_name)
        validate_class_name_has_no_underscores(class_name)

    # 2. Prepare accumulators
    words: list[str] = []
    char_stack: list[str] = []

    # 3. Flush helper
    def flush_stack() -> None:
        """Pushes the current word into the output list."""
        if not char_stack:
            return

        word = "".join(char_stack)
        normalized = word if word.isupper() else word.lower()
        words.append(normalized)
        char_stack.clear()

    # 4. Process characters
    for char in class_name:

        # 4.1 Digits → always start a new block
        if char.isdigit():
            if char_stack and not char_stack[-1].isdigit():
                flush_stack()
            char_stack.append(char)
            continue

        # 4.2 Uppercase → start of a new word or acronym
        if char.isupper():
            if char_stack and (char_stack[-1].islower() or char_stack[-1].isdigit()):
                flush_stack()
            char_stack.append(char)
            continue

        # 4.3 Lowercase → continuation or acronym boundary
        if len(char_stack) > 1 and char_stack[-1].isupper():
            last_upper = char_stack.pop()
            flush_stack()
            char_stack.append(last_upper)

        char_stack.append(char)

    # 5. Flush last word
    flush_stack()

    # 6. Return tuple
    return tuple(words)


_DESIGN_NOTES = """
# _class_name_splitter

## Purpose
Decomposes a PascalCase class name into semantic words.  
This is the foundation for generating `name_tuple`, `name_snake`, and `name_private`
inside the metadata pipeline.

## Validation
Before splitting, the function enforces three structural rules:

1. `validate_class_name_is_identifier`  
   Removes illegal characters (spaces, hyphens, dots, leading digits).

2. `validate_class_name_is_ascii`  
   Removes diacritics and non‑ASCII letters.

3. `validate_class_name_has_no_underscores`  
   Enforces pure PascalCase without underscores.

After these checks, the input is guaranteed to contain only:

```
[a-zA-Z0-9]
```

## Processing logic
The algorithm walks the class name character by character and uses a small
state machine based on `char_stack`.

### Character rules

#### Digits
- Always form their own block.
- Transition from letters → flush current word.

Example:  
`User123` → `("user", "123")`

#### Uppercase letters
- Start a new word in PascalCase.
- May be part of an acronym.

Example:  
`JSONParser` → `("json", "parser")`

#### Lowercase letters
- Continue a word.
- If they follow multiple uppercase letters, they mark the end of an acronym.

Example:  
`HTTPServer` → `("HTTP", "server")`

### Acronym handling
When a lowercase letter arrives and the stack contains multiple uppercase letters:

1. Pop the last uppercase letter.
2. Flush the remaining acronym.
3. Start a new word with the popped letter.

This preserves acronyms cleanly.

## Output normalization
- Acronyms remain uppercase.
- Regular words are converted to lowercase.
- Output is a tuple of semantic units.

## Examples

| Input          | Output                       |
|----------------|-------------------------------|
| `MyClass`      | `("my", "class")`             |
| `HTTPServer`   | `("HTTP", "server")`          |
| `User123`      | `("user", "123")`             |
| `MyHTTPClient` | `("my", "http", "client")`    |

## Performance
- **Time:** O(n) — single pass over characters  
- **Space:** O(w) — number of words  
- No regex, no recursion, minimal branching
```
"""