import os
import subprocess
from subprocess import PIPE, STDOUT
from flask import Flask, request
from werkzeug.datastructures import FileStorage
from .errors import NoKeyFile, PublicKeyNotFound, SecretNotFound
from .utils import check_id

app = Flask(__name__)

SSH_KEY_PATH = "./key"

@app.route("/")
def hello_world():
    return "<p>mimi</p>"

def encrypt(id: str):
    check_id(id)
    PUBLIC_KEY_PATH = "./secrets/{}.pub".format(id)
    if not os.path.exists(PUBLIC_KEY_PATH):
        if request.method == "POST":
            recived_key = request.files.get("key", None)
            if recived_key is None:
                raise NoKeyFile()
            assert isinstance(recived_key, FileStorage)
            recived_key.save(PUBLIC_KEY_PATH)
        else:
            raise PublicKeyNotFound()
    SECRET_PATH = "./secrets/{}".format(id)
    if not os.path.exists(SECRET_PATH):
        raise SecretNotFound()
    return subprocess.check_output(["rage", "-R", PUBLIC_KEY_PATH, "-a", SECRET_PATH])

@app.route("/sign/<id>", methods=["GET", "POST"])
def sign(id):
    check_id(id)
    if not os.path.exists(SSH_KEY_PATH):
        raise NoKeyFile()
    p = subprocess.Popen(["ssh-keygen", '-Y', 'sign', '-n', 'file', '-f', SSH_KEY_PATH], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    with open("./secrets/{}".format(id), "rb") as f:
        stdout, _stderr = p.communicate(input=f.read())
    return stdout


@app.route("/get/<id>", methods=["GET", "POST"])
def fetch_secret(id):
    encrypted = encrypt(id)
    return encrypted

def main():
    app.run(port=8111)
