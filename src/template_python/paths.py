from pathlib import Path

_this = Path(__file__)

dir_pkg = _this.parent
dir_src = dir_pkg.parent
dir_tests = dir_src / "tests"
dir_logs = dir_src / "logs"

name_pkg = dir_pkg.name
