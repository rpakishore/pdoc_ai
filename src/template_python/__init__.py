"""
.. include:: ../../README.md
"""

from rich.console import Console
from rich.panel import Panel

from .utils.config_parser import config
from .utils.logger import log


def debug(status=False):
    """Import this in a new module and enable debug to use debug"""
    if status:
        log.setLevel(10)  # debug
        log.debug(f"Debug Mode: {status}")
    else:
        log.setLevel(20)  # info


def test_configs():
    """Tests if the config_file is correctly set up"""
    console = Console()

    module_name = __name__
    console.rule(f"[bold magenta]Module: {module_name}[/bold magenta]\n")

    def _config_vals_ok(keys: tuple[str, ...], default="NAN") -> bool:
        return config.get(keys=keys, default=default) != default

    # Define a helper to format the output
    def check_configs(title, vals_to_check):
        with console.status(f"[bold cyan]Checking {title} configs...", spinner="dots"):
            if all([_config_vals_ok(x) for x in vals_to_check]):
                console.print(
                    Panel("[green bold]OK", title=title, border_style="green")
                )
            else:
                console.print(
                    Panel("[red bold]Not OK", title=title, border_style="red")
                )

    # OpenAI
    check_configs("LLM", [("llm", "url"), ("llm", "key"), ("llm", "model")])

    # Gotify
    check_configs("Gotify", [("gotify", "url"), ("gotify", "key")])


debug(status=False)
