# Inners
from .validations import (
    validate_class_name_is_identifier,
    validate_class_name_is_ascii,
    validate_class_name_has_no_underscores
)


def _class_name_splitter(
    class_name: str
) -> tuple[str, ...]:
    """
    Splits a SimpleObject class name into semantic units (words).

    This utility is tailor-made for the SimpleObject ecosystem and assumes that the name
    was obtained directly from the class attribute `__name__`. It performs specific validations
    that complement the properties guaranteed by Python.
    """

    # 1. Class name validation
    # We perform only necessary checks that the Python parser does not guarantee for __name__.
    if not class_name.isidentifier() or not class_name.isascii() or "_" in class_name:
        validate_class_name_is_identifier(class_name)
        validate_class_name_is_ascii(class_name)
        validate_class_name_has_no_underscores(class_name)

    # 2. Initialize word storage and character accumulator
    words = []
    char_stack = []

    # 3. Helper function to flush the stack and store the word
    def flush_stack() -> None:
        """
        Pops the current word from the char_stack, normalizes it, and adds it to the list.
        Then, it clears the stack.
        """
        if char_stack:
            word = "".join(char_stack)
            # Acronyms (all uppercase) remain uppercase, others are converted to lowercase.
            normalized_word = word if word.isupper() else word.lower()
            words.append(normalized_word)
            char_stack.clear()

    # 4. Iterate over individual characters of the class name
    for char in class_name:

        # 4.1 Digits: Always start a new word (User123 -> user, 123)
        if char.isdigit():

            # 4.1.1 Transition from letter to digit → terminate current word
            if char_stack and not char_stack[-1].isdigit():
                flush_stack()

            # 4.1.2 Add digit to the stack
            char_stack.append(char)

        # 4.2 Uppercase letters: Potential start of a word or acronym (PascalCase)
        elif char.isupper():

            # 4.2.1 Transition from lowercase letter or digit to uppercase → terminate word
            if char_stack and (char_stack[-1].islower() or char_stack[-1].isdigit()):
                flush_stack()

            # 4.2.2 Add uppercase letter to the stack
            char_stack.append(char)

        # 4.3 Lowercase letters: Continuation of a word or detection of the end of an acronym
        else:
            # 4.3.1 Acronym detection: If there are multiple characters in the stack and the last one is uppercase,
            # then this last uppercase letter belongs to a new word (e.g., 'HTTPServer' -> 'HTTP', 'Server')
            if len(char_stack) > 1 and char_stack[-1].isupper():
                last_uppercase = char_stack.pop()   # Extract the start of the new word
                flush_stack()                       # Close the acronym
                char_stack.append(last_uppercase)   # Start the new word

            # 4.3.2 Add lowercase letter to the stack
            char_stack.append(char)

    # 5. Process the last remaining word in the accumulator
    flush_stack()

    # 6. Return a tuple of semantic words
    return tuple(words)


_DESIGN_NOTES = """
# _class_name_splitter

## Purpose
A specialized utility for decomposing class names into semantic units (words). Within the SimpleObject ecosystem, it serves as a foundational building block for generating readable names, attributes, and parameters.

## Logic and Processing Flow
The function utilizes a **stateful stack** (`char_stack`) approach and processes the input string character by character. It is optimized for pure PascalCase without underscores.

### Character Handling
1. **Digits**: Act as transition points. If they follow letters, they always start a new block (e.g., `User123` -> `user`, `123`).
2. **Uppercase Letters**: Mark the beginning of a new word in PascalCase or a component of an acronym.
3. **Lowercase Letters**: Continuation of a standard word or an indicator of the end of an acronym.

### Handling Acronyms (4.3.1)
When a lowercase letter arrives and there are multiple uppercase letters in the stack:
- The last uppercase letter in the stack belongs to the newly starting word.
- The preceding uppercase letters form an acronym, which is closed.
- Example: `HTTPServer` -> The stack accumulates `['H', 'T', 'T', 'P']`. When the lowercase `'e'` arrives, it pops `'P'`, flushes the remaining acronym `HTTP`, and starts a new word block with `['P', 'e']`.

This ensures clean results for standard naming patterns:
- `JSONParser` -> `('json', 'parser')`
- `MyHTTPClient` -> `('my', 'http', 'client')`

## Output Normalization
The nested helper function `flush_stack()` applies the meaning-preservation rule:
- Sequences consisting exclusively of uppercase letters (acronyms) remain uppercase.
- Other words (PascalCase) are converted to lowercase.
- This allows for easy subsequent transformations (e.g., converting into snake_case).

## Why flush_stack() is Nested
- **Shared State**: It has direct access to `char_stack` and `words` without the overhead of passing parameters.
- **Locality**: It is a pure implementation detail that belongs exclusively to this function's scope.

## Validation and Integrity
The function primarily relies on the guarantee that the input comes from `ClassName.__name__`. However, it executes three complementary validations to guard against dynamically generated classes created via `type()`:
1. **is_identifier**: Catches illegal tokens such as spaces or hyphens.
2. **is_ascii**: Excludes localized diacritics (accents, hooks) that would disrupt the character splitting logic.
3. **no_underscores**: Enforces a strict PascalCase constraint, which simplifies the algorithm (eliminating the need to parse `_`).

## Edge Case Decisions
| Case | Behavior | Justification |
|---|---|---|
| Empty Name | Raises ValueError (via `type()`) | Python natively prevents the creation of a class without a name. |
| Numbers in the Middle | `('http2', 'server')` | Numbers form their own blocks; transitioning back to a letter triggers a flush. |
| Single Letter | `('a',)` | The minimum valid case functions correctly. |
| Dynamic Noise | Caught by validation | Protection against malformed names like `type("My Class", ...)` |

## Performance Notes
- **Time Complexity**: $O(n)$, where $n$ is the length of the class name string.
- **Space Complexity**: $O(w)$, where $w$ is the number of semantic words in the result.
- The algorithm is linear and processes the string in a single pass.
"""