import os
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

def get_secret_output(id):
    secret_path = get_secret_path(id, 'secret')
    if os.path.isdir(secret_path):
        return subprocess.check_output(["tar", "-czf", "-", secret_path])
    else:
        with open(secret_path, "rb") as f:
            return f.read()

@app.route("/sign/<id>", methods=["GET", "POST"])
def sign(id):
    check_id(id)
    passphrase = current_app.config.get("PASSPHRASE", '')
    if not os.path.exists(SSH_KEY_PATH):
        raise NoKeyFile()
    sign_process = subprocess.Popen(["ssh-keygen", '-Y', 'sign', '-n', 'file', '-f', SSH_KEY_PATH, '-P', passphrase], stdin=PIPE, stderr=PIPE, stdout=PIPE)
    stdout, stderr = sign_process.communicate(get_secret_output(id))
    return stdout


@app.route("/get/<id>", methods=["GET", "POST"])
def fetch_secret(id):
    check_id(id)
    public_key_path = get_secret_path(id, "host.pub") 
    if not os.path.exists(public_key_path):
        print(public_key_path)
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
    
