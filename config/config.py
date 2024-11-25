from dataclasses import dataclass

from dotenv import load_dotenv

from .base import getenv


@dataclass
class Server:
    host: str
    port: int
    debug: bool


@dataclass
class Api:
    key: str


@dataclass
class Config:
    server: Server
    api: Api


def load_config() -> Config:
    load_dotenv()

    return Config(
        server=Server(
            host=getenv("SERVER_HOST"),
            port=int(getenv("SERVER_PORT")),
            debug=bool(getenv("SERVER_DEBUG")),
        ),
        api=Api(
            key=getenv("API_KEY"),
        ),
    )


config: Config = load_config()
