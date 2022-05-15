from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config as config
from .database.database import db, base


def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_tables():
            base.metadata.create_all(db)


# def setup_jwt(app):
#     jwt = JWTManager(app)
#
#     from app.models import RevokedTokenModel
#
#     @jwt.token_in_blocklist_loader
#     def check_if_token_in_blacklist(jwt_header, jwt_payload):
#         jti = jwt_payload['jti']
#         return RevokedTokenModel.is_jti_blacklisted(jti)


def create_app():
    app = Flask(__name__)
    setup_database(app)
    # app.config.from_object(Config)
    # setup_jwt(app)

    from .views import directors_bp, genres_bp, actors_bp, movies_bp, \
        auditoriums_bp, movie_sessions_bp, users_bp, tickets_bp
    app.register_blueprint(directors_bp)
    app.register_blueprint(genres_bp)
    app.register_blueprint(actors_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(auditoriums_bp)
    app.register_blueprint(movie_sessions_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tickets_bp)


    return app
