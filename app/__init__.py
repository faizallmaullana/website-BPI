from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS


db = SQLAlchemy()
api = Api()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'apdfbap9IBIUtvivTviutIjbKhg77tHGjhGIbuyt7t7'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['JWT_SECRET_KEY'] = 'JKHBIB986kjskjJBDKJBjbdkkjbk86KJBkjbbKb'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

    jwt = JWTManager(app)
    db.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    from app.urls import __URLPATH__

    __URLPATH__()
    api.init_app(app)
    from app.models.user import Users
    from app.models.gallery import Galleries, Galleries_img
    from app.models.bpi_article import Articles_bpi, Articles_img

    Migrate(app, db)
    return app