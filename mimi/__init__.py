
from mimi.utils import check_passphrase, get_passphrase
from .app import app
import argparse

from mimi import app, init
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help', dest="command")
serve_parser = subparsers.add_parser('serve', help='run mimi server')
serve_parser.add_argument('--port', type=int, default=8111, help='port to run server on')
serve_parser.add_argument('--debug', action='store_true', help='run server in debug mode');

init_parser = subparsers.add_parser('init', help='initialize key')


def main():
    args = parser.parse_args()
    match args.command:
        case "serve":
            passpharse = get_passphrase()
            check_passphrase(passpharse)
            with app.app_context():
                app.config["PASSPHRASE"] = passpharse
            app.run(port=args.port, debug=args.debug)
        case "init":
            init.init()
