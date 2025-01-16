from pathlib import Path
from pdoc_ai.llm import LLM
from pathlib import Path
from .ingester import generate_system


def document(
    package: Path,
    pyfile: Path | None = None,
    include_patterns: list[str] = [],
    exclude_patterns: list[str] = [],
    llm_baseurl: str = "http://100.99.54.84:11434/v1",
    llm_key: str = "ollama",
    llm_model: str = "code_assist_large",
    **kwargs,
) -> None:
    """Generate documentation comments (docstrings) for the given package using a specified language model.

    Args:
        package (Path): The root directory of the Python package to document.
        include_patterns (list[str], optional): Patterns to include when scanning files. Defaults to [].
        exclude_patterns (list[str], optional): Patterns to exclude when scanning files. Defaults to [].
        llm_baseurl (str, optional): The base URL for the language model API. Defaults to "http://100.99.54.84:11434/v1".
        llm_key (str, optional): The key used to authenticate with the language model API. Defaults to "ollama".
        llm_model (str, optional): The name of the language model to use. Defaults to "code_assist_large".
    """
    pyfile = Path(pyfile)
    assert pyfile.is_file()
    llm = LLM(base_url=llm_baseurl, model=llm_model, key=llm_key)

    USER_MSG: str = """
    Rewrite the contents of `File: {}` to include documentation comments (docstrings).
    Ensure that all docstrings are in google format.
    Do not change any other part of the code.
    Output only the contents of the file, do not add any additional text. Do not add any explainations.
    """

    llm.SYSTEM = generate_system(
        package=package,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
    )

    def document_file(filepath: Path):
        _str_filepath = str(filepath).replace(str(package), "")
        print(f"Generating docstrings for {_str_filepath}")
        resp = llm.response(
            messages=llm.msg(user_content=USER_MSG.format(_str_filepath)),
        )

        if resp.strip().startswith("```"):
            resp = "\n".join(resp.strip().split("\n")[1:-1])

        new_filepath = filepath.with_stem(f"nosync_{filepath.stem}")
        with open(new_filepath, "w") as f:
            f.write(resp)

    if pyfile is None:
        for file in package.glob("**/*.py"):
            document_file(file)
    else:
        document_file(pyfile)
