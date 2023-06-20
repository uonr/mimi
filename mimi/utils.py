import re

from .errors import InvaildNodeId

def check_id(hostname) -> bool:
    if re.match(r"^[a-zA-Z0-9\-_.]+$", hostname) is None:
        raise InvaildNodeId()
