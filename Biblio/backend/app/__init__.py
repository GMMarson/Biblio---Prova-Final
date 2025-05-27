from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from dotenv import load_dotenv
import os

db = None

def create_app():
    global db
    load_dotenv()

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    CORS(app)
    JWTManager(app)

    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["biblioteca_db"]

    from .auth import auth_bp
    from .users import users_bp
    from .livros import livros_bp
    from .reservas import reservas_bp

    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(users_bp, url_prefix='/')
    app.register_blueprint(livros_bp, url_prefix='/')
    app.register_blueprint(reservas_bp, url_prefix='/')
    

    return app
