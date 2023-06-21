import os
import re
from getpass import getpass
from subprocess import check_call
import subprocess
from typing import Optional

from .errors import InvaildNodeId, NoKeyFile

def secrets_path() -> str:
    return "./secrets"

def get_secret_path(id: str, filename: Optional[str] = None) -> str:
    if filename is None:
        return os.path.join(secrets_path(), id)
    return os.path.join(secrets_path(), id, filename)

def get_key_path(check_exists=False) -> str:
    if check_exists and not os.path.exists("./key"):
        raise NoKeyFile()
    return "./key"

def check_id(hostname) -> bool:
    if re.match(r"^[a-zA-Z0-9\-_.]+$", hostname) is None:
        raise InvaildNodeId()

def get_passphrase() -> str:
    return getpass("Enter SSH key passphrase: ")

# Check ssh key passphrase
def check_passphrase(passphrase: str) -> bool:
    try:
        check_call(["ssh-keygen", "-y", "-f", get_key_path(), '-P', passphrase])
    except subprocess.CalledProcessError:
        raise RuntimeError("Wrong passphrase")
