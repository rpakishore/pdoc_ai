from gitingest import ingest
from pathlib import Path
from typing import Literal


def _begin_quotes(line: str) -> bool:
    """Check if a line starts with a docstring delimiter.

    Args:
        line (str): The line of text to check.

    Returns:
        bool: True if the line starts with a docstring delimiter, False otherwise.
    """
    if line.strip().startswith('"""') or line.strip().startswith("'''"):
        return True
    return False


def _find_docstrings(text: str) -> list[tuple[int, int]]:
    """Get range of docstrings from text.

    Args:
        text (str): The text to search for docstrings.

    Returns:
        list[tuple[int, int]]: A list of tuples containing the start and end indices of each docstring.
    """
    ranges: list[tuple[int, int]] = []
    _start: int | None = None
    _start_type: Literal['"""', "'''", None] = None
    _skip_next: bool = False

    for idx, line in enumerate(text.split("\n")):
        if (_start is None) and (_begin_quotes(line)) and (not _skip_next):
            _start = idx
            _start_type = line.strip()[:3]
            line = line.strip()[3:]
            _skip_next = False

        if _start is None or _start_type is None:
            if '"""' in line or "'''" in line:
                _skip_next = not _skip_next
            continue
        elif _start_type in line.strip():
            ranges.append((_start, idx + 1))
            _start = None
            _start_type = None
    return ranges


def _strip_docstring(doc: str):
    """Remove docstrings from the given text.

    Args:
        doc (str): The text containing docstrings.

    Returns:
        str: The text with docstrings removed.
    """
    _doc: list[str] = doc.split("\n")
    new_doc = doc[:]
    ranges = _find_docstrings(doc)
    for range in ranges:
        _txt = "\n".join(_doc[range[0] : range[1]])
        # print(_txt)
        new_doc = new_doc.replace(_txt, "")
    return new_doc


def generate_context(
    package: str | Path,
    include_patterns: list[str] = [],
    exclude_patterns: list[str] = [],
) -> str:
    """Generate context for the given package.

    Args:
        package (str | Path): The package path.
        include_patterns (list[str], optional): Patterns to include. Defaults to [].
        exclude_patterns (list[str], optional): Patterns to exclude. Defaults to [].

    Returns:
        str: The generated context as a string.
    """
    package = str(package)

    _, tree, content = ingest(
        source=str(package),
        include_patterns=["*.py", *include_patterns],
        exclude_patterns=["**/tests/*", "**/nosync**", *exclude_patterns],
    )

    context = f"""
<DIRECTORY_STRUCTURE>
{tree}
</DIRECTORY_STRUCTURE>

<FILE_CONTENTS>
{_strip_docstring(content)}
</FILE_CONTENTS>
    """
    return context


def generate_system(
    package: str | Path,
    include_patterns: list[str] = [],
    exclude_patterns: list[str] = [],
) -> str:
    """Generate a system message for the given package.

    Args:
        package (str | Path): The package path.
        include_patterns (list[str], optional): Patterns to include. Defaults to [].
        exclude_patterns (list[str], optional): Patterns to exclude. Defaults to [].

    Returns:
        str: The generated system message as a string.
    """

    SYSTEM_MSG: str = f"""
You are an experienced python programming assistant and a documentation specialist.
Your task is to add documentation comments to code in google format to enable autogeneration of useful and descriptive pdoc documents.
You will not make any changes to the code itself but only generate documentation comments (docstrings).

Given below are the directory structure, file contents of the project.

{generate_context(package = package, include_patterns = include_patterns, exclude_patterns = exclude_patterns,)}
    """
    return SYSTEM_MSG
