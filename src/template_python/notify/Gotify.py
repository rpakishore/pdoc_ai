import requests

from template_python.utils.config_parser import config

from ..utils.logger import log

log.debug("Sending No")


def notify(title: str, message: str = "", priority: int = 2) -> None:
    log.debug(f"Sending message {title} to Gotify with priority:{priority}")
    resp = requests.post(
        f"{config.get(keys=('gotify', 'url'))}/message?token={config.get(keys=('gotify', 'key'))}",
        json={"message": message, "priority": priority, "title": title},
    )
    log.info(f"[GOTIFY]Response: {resp}")
