from app import routes
from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config['JSON_SORT_KEYS'] = False

    routes.init_app(app)

    return app