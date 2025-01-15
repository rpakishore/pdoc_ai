from base64 import b64decode, b64encode

from template_python.utils.config_parser import config


def get_password(item: str, username: str):
    """Retrieve base64 encoded password from config files"""
    # Check the `config.toml` file
    pwd = config.get(keys=(item, username), default="")
    return decode(text=pwd)


def encode(text: str) -> str:
    return b64encode(text.encode()).decode()


def decode(text: str) -> str:
    return b64decode(text.encode()).decode()
