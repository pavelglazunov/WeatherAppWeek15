from config import load_config
from src.router import main_app


def main():
    config = load_config()

    main_app.run_server(host=config.server.host, port=config.server.port, debug=config.server.debug)


if __name__ == '__main__':
    main()
