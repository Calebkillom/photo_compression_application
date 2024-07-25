from flask import Flask
from .user_routes import user_routes
from .image_routes import image_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_routes, url_prefix='/api/users')
    app.register_blueprint(image_routes, url_prefix='/api/images')
    return app
