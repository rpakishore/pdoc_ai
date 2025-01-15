import typer
from rich.console import Console

from template_python import test_configs

app = typer.Typer()
console = Console()


@app.command()
def encode_base64(text: str) -> str:
    """converts base string to base64 string. Useful for filling out `config.toml`"""
    import base64

    return base64.b64encode(text.encode()).decode()


test = typer.Typer()


@test.command()
def test():
    test_configs()
