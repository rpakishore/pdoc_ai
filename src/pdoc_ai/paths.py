from pathlib import Path

_this = Path(__file__)

dir_pkg = _this.parent
"""Path to the package directory."""

dir_src = dir_pkg.parent
"""Path to the source directory."""

dir_tests = dir_src / "tests"
"""Path to the tests directory."""

dir_logs = dir_src / "logs"
"""Path to the logs directory."""

name_pkg = dir_pkg.name
"""Name of the package."""
