import os
import re
import subprocess
from flask import Flask, request
from werkzeug.datastructures import FileStorage

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>mimi</p>"

@app.route("/get/<hostname>", methods=["GET", "POST"])
def fetch_secret(hostname):
    if re.match(r"^[a-zA-Z0-9\-_.]+$", hostname) is None:
        return "Invalid hostname", 400
    PUBLIC_KEY_PATH = "./secrets/{}.pub".format(hostname)
    if not os.path.exists(PUBLIC_KEY_PATH):
        if request.method == "POST":
            recived_key = request.files.get("key", None)
            if recived_key is None:
                return "No key file", 400
            assert isinstance(recived_key, FileStorage)
            recived_key.save(PUBLIC_KEY_PATH)
        else:
            return "Public key not found", 404
    SECRET_PATH = "./secrets/{}".format(hostname)
    if not os.path.exists(SECRET_PATH):
        return "Secret not found", 404
    return subprocess.check_output(["rage", "-R", PUBLIC_KEY_PATH, "-a", SECRET_PATH])

def main():
    app.run(port=8111)
