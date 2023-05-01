import importlib
import os

from flask import Flask

from app.helpers import project_path


def build_app():
    http = Flask(__name__)

    for filename in os.listdir(os.path.join(project_path, 'app', 'routers')):
        if not filename.endswith('.py') or filename in ['__init__.py']:
            continue

        router_name = filename[:-3]
        router_module = importlib.import_module(f'app.routers.{router_name}')

        if hasattr(router_module, 'router'):
            http.register_blueprint(router_module.router)

    return http


app = build_app()
