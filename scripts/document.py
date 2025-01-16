from pdoc_ai import document
from pathlib import Path
import tomllib

config_path = Path(__file__).parent.parent / "config.toml"

if config_path.exists():
    with open(config_path, "r") as f:
        config = tomllib.loads(f.read()).get("pdoc_ai", {})
else:
    config = {}

package_path = Path(__file__).parent.parent / "src" / "pdoc_ai"

print(
    """
Choose a follwing option:
- Leave empty for documenting full package
- Enter path for specific file to document
- Enter `clear` to clear previous generated files
"""
)

choice = input("Enter your choice: ")
if choice.strip() == "":
    document(package=package_path, pyfile=None, **config)
elif choice.strip().lower() == "clear":
    print("Clearing previous generated files")
    for file in package_path.glob("**/nosync_*.py"):
        file.unlink()
        print(f"Removed: {str(file).replace(str(package_path), "")}")
else:
    document(package=package_path, pyfile=choice, **config)
