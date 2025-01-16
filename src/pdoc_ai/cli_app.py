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
    """Generate documentation (docstrings) for provided file

    Args:
        package (str): The path to directory to parse.
        file (str): Path to file to document
        llm_baseurl (str, optional): The base URL for the LLM service. Defaults to "http://100.99.54.84:11434/v1".
        llm_key (str, optional): The key for the LLM service. Defaults to "ollama".
        llm_model (str, optional): The model to use for encoding. Defaults to "code_assist_large".
        exclude_pattern (str, optional): A pattern to exclude files from processing. Defaults to an empty string.
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
    for file in Path(package).glob("**/nosync_*.py"):
        file.unlink()
        print(f"Removed: {str(file).replace(str(package), "")}")
