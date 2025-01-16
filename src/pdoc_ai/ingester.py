from gitingest import ingest
from pathlib import Path
from typing import Literal


def _begin_quotes(line: str) -> bool:
    """Check if a line begins with triple quotes."""
    if line.strip().startswith('"""') or line.strip().startswith("'''"):
        return True
    return False


def _find_docstrings(text: str) -> list[tuple[int, int]]:
    """Get range of docstrings from text"""
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
    """Remove all existing docstrings from the code."""
    _doc: list[str] = doc.split("\n")
    new_doc = doc[:]
    ranges = _find_docstrings(doc)
    for range in ranges:
        _txt = "\n".join(_doc[range[0] : range[1]])
        # print(_txt)
        new_doc = new_doc.replace(_txt, "")
    return new_doc


def generate_system(
    package: str | Path,
    include_patterns: list[str] = [],
    exclude_patterns: list[str] = [],
) -> str:
    """Generate a system message for document generation."""
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

    SYSTEM_MSG: str = f"""
You are an experienced python programming assistant and a documentation specialist.
Your task is to add documentation comments to code in google format to enable autogeneration of useful and descriptive pdoc documents.
You will not make any changes to the code itself but only generate documentation comments (docstrings).

Given below are the directory structure, file contents of the project.

{context}
    """
    return SYSTEM_MSG
