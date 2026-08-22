# Inners
from .validations import (
    validate_class_name_is_identifier,
    validate_class_name_is_ascii,
    validate_class_name_has_no_underscores,
)


def _class_name_splitter(
    class_name: str,
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

        words.append("".join(char_stack))
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
            if char_stack and (
                char_stack[-1].islower()
                or char_stack[-1].isdigit()
            ):
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

The function performs only structural decomposition. It preserves the
original capitalization of each semantic unit and does not normalize
the resulting words.

The resulting tuple is used as the source representation for generating
`name_tuple`, `name_snake`, and `name_private` inside the metadata pipeline.

## Validation
Before splitting, the function enforces three structural rules:

1. `validate_class_name_is_identifier`
   Validates that the class name is a valid Python identifier.

2. `validate_class_name_is_ascii`
   Validates that the class name contains only ASCII characters.

3. `validate_class_name_has_no_underscores`
   Validates that the class name does not contain underscores.

The validators do not modify the input. They only validate it and raise
an appropriate exception when a structural rule is violated.

After validation, the input is guaranteed to contain only:

```

[a-zA-Z0-9]

```

## Processing logic
The algorithm walks the class name character by character and uses a small
state machine based on `char_stack`.

The splitter identifies semantic boundaries while preserving the original
characters of each resulting word.

### Character rules

#### Digits
- Always form their own block.
- Transition from letters to digits flushes the current word.
- Consecutive digits remain in the same block.

Example:

`User123` → `("User", "123")`

#### Uppercase letters
- Start a new word when following a lowercase letter.
- Start a new block when following a digit.
- May belong to an acronym when followed by another uppercase letter.

Examples:

`MyClass` → `("My", "Class")`

`HTTPServer` → `("HTTP", "Server")`

#### Lowercase letters
- Continue the current word.
- When following multiple uppercase letters, they mark the boundary
  between an acronym and the following word.

Example:

`HTTPServer` → `("HTTP", "Server")`

## Acronym handling
When a lowercase letter arrives and the stack contains multiple
uppercase letters:

1. Pop the last uppercase letter.
2. Flush the remaining uppercase letters as the acronym.
3. Start the next word with the popped uppercase letter.
4. Continue with the lowercase character.

This separates an acronym from the following PascalCase word while
preserving the capitalization of both parts.

Example:

`HTTPServer`

is decomposed as:

```

HTTP | Server

````

resulting in:

```python
("HTTP", "Server")
````

## Output preservation

The splitter does not normalize the resulting words.

Each semantic unit preserves the capitalization present in the original
class name.

Therefore:

```text
MyClass       → ("My", "Class")
HTTPServer    → ("HTTP", "Server")
User123       → ("User", "123")
MyHTTPClient  → ("My", "HTTP", "Client")
```

Normalization is intentionally left to the caller.

For example, `create_names` can derive:

```text
("My", "HTTP", "Client")
        ↓
"my_http_client"
        ↓
"_my_http_client"
```

This keeps the responsibilities separated:

* `_class_name_splitter` → decomposes the original name
* `name_tuple` → preserves the semantic components
* `name_snake` → provides the normalized `snake_case` representation
* `name_private` → provides the private `snake_case` representation

## Examples

| Input          | Output                     |
| -------------- | -------------------------- |
| `MyClass`      | `("My", "Class")`          |
| `HTTPServer`   | `("HTTP", "Server")`       |
| `User123`      | `("User", "123")`          |
| `MyHTTPClient` | `("My", "HTTP", "Client")` |

## Design principle

The splitter follows a strict separation-of-concerns rule:

> Split first, normalize later.

The function must not change the semantic content or capitalization of
the original class name. Its only responsibility is to identify the
boundaries between semantic units.

This allows the resulting `name_tuple` to remain a faithful structural
representation of the original class name while allowing derived names
to apply their own normalization rules.

## Performance

* **Time:** O(n) — single pass over characters
* **Space:** O(w) — number of words plus the current character stack
* No regex
* No recursion
* Minimal branching
  """

