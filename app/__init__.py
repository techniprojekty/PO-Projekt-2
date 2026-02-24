from flask import Flask

from persistence.user_repository import UserRepository
from services.user_service import UserService


def create_app():
    app = Flask(__name__)

    repo = UserRepository()
    service = UserService(repo)

    from app.routes import register_routes
    register_routes(app, service)

    return app
