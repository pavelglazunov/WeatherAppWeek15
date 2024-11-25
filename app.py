from flask import Flask

from config import load_config
from src.router import routers


def main():
    app = Flask(__name__)
    config = load_config()

    for router in routers:
        app.register_blueprint(router)

    app.run(host=config.server.host, port=config.server.port, debug=config.server.debug)


if __name__ == '__main__':
    main()
