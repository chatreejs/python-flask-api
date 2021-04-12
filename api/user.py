from flask import request, Response, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from mongoengine import NotUniqueError, DoesNotExist
from kanpai import Kanpai

from models.users import Users


class UsersApi(Resource):
    @jwt_required()
    def get(self) -> Response:
        users = Users.objects().exclude('password')
        if len(users) > 0:
            del users[0].password
            response = jsonify(users)
            response.status_code = 200
            return response
        else:
            response = Response()
            response.status_code = 204
            return response


class UserApi(Resource):
    @jwt_required()
    def get(self, user_id: str = None) -> Response:
        try:
            user = Users.objects.exclude(
                'password').get(id=user_id).to_json()
            return Response(user, mimetype="application/json", status=200)
        except DoesNotExist:
            return Response(status=404)

    @jwt_required()
    def patch(self, user_id: str) -> Response:
        schema = Kanpai.Object({
            'username': Kanpai.String(),
            'firstName': Kanpai.String(),
            'lastName': Kanpai.String(),
            'email': Kanpai.String()
        })

        validate_result = schema.validate(request.get_json())
        if validate_result.get('success', False) is False:
            return Response(status=400)

        body = request.get_json()
        try:
            Users.objects.get(id=user_id).update(**body)
            return Response(status=200)
        except DoesNotExist:
            return Response(status=404)

    @jwt_required()
    def delete(self, user_id: str) -> Response:
        try:
            Users.objects.get(id=user_id).delete()
            return Response(status=200)
        except DoesNotExist:
            return Response(status=404)
