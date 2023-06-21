import os
from getpass import getpass
from subprocess import STDOUT, check_call

from mimi.utils import get_passphrase, get_key_path, secrets_path

def init():
    # Check if key exists
    if os.path.exists(get_key_path()):
        print("Key already exists")
    else:
        passphrase = get_passphrase()
        check_call(["ssh-keygen", "-t", "ed25519", "-f", get_key_path(), "-C", "mimi", "-N", passphrase], stderr=STDOUT)

    check_call(["mkdir", "-p", './staging'])
    check_call(["chmod", "700", './staging'])
    check_call(["mkdir", "-p", secrets_path()])
    check_call(["chmod", "700", secrets_path()])
