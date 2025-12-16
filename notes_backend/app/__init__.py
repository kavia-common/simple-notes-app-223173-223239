from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .routes.health import blp as health_blp
from .routes.notes import blp as notes_blp
from .models import db, Note

import os


app = Flask(__name__)
app.url_map.strict_slashes = False

# CORS for all origins (sufficient for local preview)
CORS(app, resources={r"/*": {"origins": "*"}})

# OpenAPI / Swagger configuration
app.config["API_TITLE"] = "Notes API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# SQLite configuration - simple self-contained persistence
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notes.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize DB
db.init_app(app)
with app.app_context():
    # Create tables if not exists
    db.create_all()

# Register API blueprints
api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(notes_blp)
