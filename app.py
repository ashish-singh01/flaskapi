import os
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager


from db import db
import models

from resource.item import blp as ItemBlueprint
from resource.store import blp as StoreBlueprint
from resource.tag import blp as TagBlueprint
from resource.user import blp as UserBlueprint
def create_app(db_url = None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATBASE_URI", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config["PROPOGATE_EXCEPTION"] = True

    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "36606403240331702591982952080740427072"

    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    return app