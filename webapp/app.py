from flask import Flask
from webapp.api.user_routes import user_routes
from webapp.api.image_routes import image_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(user_routes, url_prefix='/api/users')
    app.register_blueprint(image_routes, url_prefix='/api/images')

    @app.route('/test', methods=['GET'])
    def test():
        return "Test route is working!", 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
