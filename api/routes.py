from api.user import UserApi, UsersApi
from flask_restx import Api

from api.authentication import SignUpApi, TokenApi, RefreshTokenApi
from api.subject import SubjectApi, SubjectsApi


def create_route(api: Api):
    # OAuth
    api.add_resource(SignUpApi, '/authentication/signup')
    api.add_resource(TokenApi, '/authentication/token')
    api.add_resource(RefreshTokenApi, '/authentication/token/refresh')

    # Users
    api.add_resource(UsersApi, '/users')
    api.add_resource(UserApi, '/users/<user_id>')

    # Subjects
    api.add_resource(SubjectsApi, '/subjects')
    api.add_resource(SubjectApi, '/subjects/<subject_id>')