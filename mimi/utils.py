import re

from .errors import InvaildHostname

def check_hostname(hostname) -> bool:
    if re.match(r"^[a-zA-Z0-9\-_.]+$", hostname) is None:
        raise InvaildHostname()
