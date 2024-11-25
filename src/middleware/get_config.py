from config.config import Config


class GetConfigMiddleware:

    def __init__(self, app, config: Config):
        self.app = app
        self.config = config

    def __call__(self, environ, start_response):
        environ["config"] = self.config
        return self.app(environ, start_response)
