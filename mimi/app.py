import os
import tarfile
import tempfile
import subprocess
from subprocess import PIPE, STDOUT, Popen
from flask import Flask, current_app, request
from werkzeug.datastructures import FileStorage
from .errors import NoKeyFile, PublicKeyNotFound, SecretNotFound
from .utils import check_id, get_key_path, get_secret_path

app = Flask(__name__)

SSH_KEY_PATH = get_key_path()

@app.route("/")
def hello_world():
    return "<p>mimi</p>"

def reset_tarinfo(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo:
    tarinfo.uid = 0
    tarinfo.gid = 0
    tarinfo.mtime = 0
    return tarinfo

def get_secret_output(id: str, refresh_cache: bool = False) -> bytes:
    if not refresh_cache:
        cached = current_app.config.get("DB", {}).get(id, None)
        if cached is not None:
            return cached
    secret_path = get_secret_path(id, 'secret')
    if not os.path.exists(secret_path):
        raise SecretNotFound()
    result = None
    if os.path.isdir(secret_path):
        with tempfile.TemporaryFile() as f:
            with tarfile.open(fileobj=f, mode="w:gz") as tar:
                tar.add(secret_path, arcname=".", filter=reset_tarinfo, recursive=True)
            f.seek(0)
            result = f.read()
    else:
        with open(secret_path, "rb") as f:
            result = f.read()
    assert isinstance(result, bytes)
    current_app.config["DB"][id] = result
    return result


@app.route("/sign/<id>", methods=["GET", "POST"])
def sign(id):
    check_id(id)
    passphrase = current_app.config.get("PASSPHRASE", '')
    if not os.path.exists(SSH_KEY_PATH):
        raise NoKeyFile()
    sign_process = subprocess.Popen(["ssh-keygen", '-Y', 'sign', '-n', 'file', '-f', SSH_KEY_PATH, '-P', passphrase], stdin=PIPE, stderr=PIPE, stdout=PIPE)
    stdout, stderr = sign_process.communicate(get_secret_output(id, refresh_cache=True))
    return stdout


@app.route("/get/<id>", methods=["GET", "POST"])
def fetch_secret(id):
    check_id(id)
    public_key_path = get_secret_path(id, "host.pub") 
    if not os.path.exists(public_key_path):
        if not os.path.exists(get_secret_path(id)):
            raise SecretNotFound()
        if request.method == "POST":
            recived_key = request.files.get("key", None)
            if recived_key is None:
                raise NoKeyFile()
            assert isinstance(recived_key, FileStorage)
            recived_key.save(public_key_path)
        else:
            raise PublicKeyNotFound()
    secret_path = get_secret_path(id, 'secret')

    if not os.path.exists(secret_path):
        raise SecretNotFound()
    encrypt_process = subprocess.Popen(["rage", "-R", public_key_path, "-a"], stdin=PIPE, stderr=PIPE, stdout=PIPE)
    stdout, stderr = encrypt_process.communicate(get_secret_output(id))
    return stdout
    
