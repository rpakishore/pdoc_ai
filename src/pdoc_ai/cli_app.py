import typer
from rich.console import Console
from .main import document
from pathlib import Path

app = typer.Typer()
console = Console()


@app.command()
def package(
    path: str,
    llm_baseurl: str = "http://100.99.54.84:11434/v1",
    llm_key: str = "ollama",
    llm_model: str = "code_assist_large",
    exclude_pattern: str = "",
) -> str:
    """Generate documentation (docstrings) for provided project directory

    Args:
        path (str): The path to the file or directory to parse.
        llm_baseurl (str, optional): The base URL for the LLM service. Defaults to "http://100.99.54.84:11434/v1".
        llm_key (str, optional): The key for the LLM service. Defaults to "ollama".
        llm_model (str, optional): The model to use for encoding. Defaults to "code_assist_large".
        exclude_pattern (str, optional): A pattern to exclude files from processing. Defaults to an empty string.
    """
    document(
        package=Path(path),
        pyfile=None,
        exclude_patterns=[exclude_pattern],
        llm_baseurl=llm_baseurl,
        llm_key=llm_key,
        llm_model=llm_model,
    )


@app.command()
def file(
    package: str,
    file: str,
    llm_baseurl: str = "http://100.99.54.84:11434/v1",
    llm_key: str = "ollama",
    llm_model: str = "code_assist_large",
    exclude_pattern: str = "",
) -> str:
    """Generate documentation for a specific file in a package.

    Args:
        package (str): The path to the package.
        file (str): The path to the file.
        llm_baseurl (str, optional): The base URL for the LLM. Defaults to "http://100.99.54.84:11434/v1".
        llm_key (str, optional): The key for the LLM. Defaults to "ollama".
        llm_model (str, optional): The model to use for the LLM. Defaults to "code_assist_large".
        exclude_pattern (str, optional): Patterns to exclude from documentation generation. Defaults to "".

    Returns:
        str: The result of the documentation generation.
    """

    document(
        package=Path(package),
        pyfile=Path(file),
        exclude_patterns=[exclude_pattern],
        llm_baseurl=llm_baseurl,
        llm_key=llm_key,
        llm_model=llm_model,
    )


@app.command()
def clean(package: str):
    """Remove temporary files from the package.

    Args:
        package (str): The path to the package.
    """
    for file in Path(package).glob("**/nosync_*.py"):
        file.unlink()
        print(f"Removed: {str(file).replace(str(package), "")}")
