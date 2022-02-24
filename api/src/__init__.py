from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException

from src.models.document import db, Document, Image
from src.utils.exceptions import ErrorException


def create_app():
# Aplication factory

    app = Flask(__name__)

    # Possible to expand - Using config loader
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:toor@db:5432/rossum"
    #app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:toor@localhost/rossum"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    swagger_url = '/doc'
    api_url = '/static/swagger.json'
    swagger_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={
            "app_name": "PDF render API"
        }
    )

    # Possible to expand - Using sessions in db, instead one instance
    db.init_app(app)

    from .resources.document import document
    from .resources.upload import upload
    app.register_blueprint(document)
    app.register_blueprint(upload)
    app.register_blueprint(swagger_blueprint, url_prefix=swagger_url)

    # Possible to expand - Make file with all errorhandlers and inicializing all in this file
    @app.errorhandler(ErrorException)
    def handle_exception(error):
    
        response = {"status_code": error.status_code, "status_message": error.status_message, "description": error.data}

        app.logger.error(f"{error.status_message}: {error.data}")

        return jsonify(response), error.status_code

    @app.errorhandler(HTTPException)
    def handle_exception(error):
        
        response = {"status_code": error.code, "status_message": error.name, "description": error.description}

        app.logger.error(f"{error.name}: {error.description}")

        return jsonify(response), error.code
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        
        response = {"status_code": 500, "status_message": "Internal server error", "description": f"{error.__class__}: {error}"}

        app.logger.error(f"{response['status_message']}: {response['description']}")

        return jsonify(response), 500
    
    db.create_all(app=app)

    return app
