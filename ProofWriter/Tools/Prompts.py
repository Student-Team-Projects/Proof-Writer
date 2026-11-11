import re
from importlib.resources import files

# Folder holding every prompt template (ProofWriter/resources).
RESOURCES_DIR = files("ProofWriter") / "resources"

# Placeholders look like STATEMENT_HERE, PROOF_HERE, ...
PLACEHOLDER = re.compile(r"\b([A-Z]+)_HERE\b")


def fill_prompt(relative_path: str, **values: str) -> str:
    """
    Loads a prompt template from resources/ and fills in its placeholders.

    Each keyword fills one placeholder: STATEMENT="..." replaces STATEMENT_HERE.
    All placeholders are filled in a single pass, so text inserted for one
    placeholder is never scanned for another.

    Raises ValueError if the template's placeholders don't match the given
    keywords exactly, which catches a typo on either side.

    Example:
        If resources/Demo/demo.txt contains:
            Statement: STATEMENT_HERE
            Proof: PROOF_HERE
        then
            fill_prompt("Demo/demo.txt", STATEMENT="1 + 1 = 2", PROOF="By arithmetic.")
        returns:
            Statement: 1 + 1 = 2
            Proof: By arithmetic.
    """
    template = (RESOURCES_DIR / relative_path).read_text(encoding="utf-8")

    expected = set(PLACEHOLDER.findall(template))
    if expected != set(values):
        raise ValueError(
            f"{relative_path}: template has placeholders {sorted(expected)}, "
            f"but got values for {sorted(values)}"
        )

    return PLACEHOLDER.sub(lambda match: values[match.group(1)], template)
