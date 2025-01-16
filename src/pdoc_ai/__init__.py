"""
.. include:: ../../README.md
"""

from rich.console import Console
from rich.panel import Panel

from .utils.logger import log


def debug(status=False):
    """Import this in a new module and enable debug to use debug"""
    if status:
        log.setLevel(10)  # debug
        log.debug(f"Debug Mode: {status}")
    else:
        log.setLevel(20)  # info


debug(status=False)
