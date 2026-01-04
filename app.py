from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from blocklist import BLOCKLIST
from db import db
import os

from dotenv import load_dotenv

from resources.user import blp as UserBluePrint
from resources.circle import blp as CircleBluePrint
from resources.circle_message import blp as CircleMessageBluePrint
from resources.goal import blp as GoalBluePrint
from resources.follow import blp as FollowBluePrint
from resources.buddy import blp as BuddyBluePrint
from resources.target import blp as TargetBluePrint
from resources.check_in import blp as CheckInBluePrint
from resources.comment import blp as CommentBluePrint
from resources.reaction import blp as ReactionBluePrint
from resources.feed import blp as FeedBluePrint



def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    # Enable CORS for frontend
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

    # Flask App configurations
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "ACCOUNTABILITY REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize a Flask-SQLAlchemy database instance with your Flask application
    db.init_app(app)

    # Set up database migrations for the Flask application using Flask-Migrate (built on Alembic)
    migrate = Migrate(app, db)

    api = Api(app)
    # app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = "Hugh_TMP"
    # app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)  # or whatever duration you want
    # app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)  # typical access token duration


    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        #admin assignment based on ID ==1
        #TODO: update this
        if int(identity) == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"message": "The token has expired.", "error": "token_expired"}
            ), 401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify(
                {"message": "Signature verification failed", "error": "invalid_token"}
            ), 401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
                {"message": "The token has been revoked", "error": "token_revoked"}
            ), 401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"description": "The token has been revoked", "error": "token_revoked"}
            ), 401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"description": "The token is not fresh.",
                 "error": "fresh_token_required"}
            ), 401
        )

    api.register_blueprint(UserBluePrint)
    api.register_blueprint(CircleBluePrint)
    api.register_blueprint(CircleMessageBluePrint)
    api.register_blueprint(GoalBluePrint)
    api.register_blueprint(FollowBluePrint)
    api.register_blueprint(BuddyBluePrint)
    api.register_blueprint(TargetBluePrint)
    api.register_blueprint(CheckInBluePrint)
    api.register_blueprint(CommentBluePrint)
    api.register_blueprint(ReactionBluePrint)
    api.register_blueprint(FeedBluePrint)

    return app



