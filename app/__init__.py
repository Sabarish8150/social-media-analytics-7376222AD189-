from flask import Flask
from .routes import register_routes

def create_app():
    app = Flask(__name__)

    # Store data in memory
    app.config['USER_POST_COUNT'] = {}
    app.config['POST_TIMESTAMP'] = []
    app.config['POST_COMMENT_COUNT'] = []

    register_routes(app)

    return app
