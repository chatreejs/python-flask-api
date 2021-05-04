from flask import json, request, Response, jsonify
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from mongoengine import NotUniqueError, DoesNotExist
from kanpai import Kanpai

from models.users import Users
from models.subjects import Subjects


class UsersApi(Resource):
    @jwt_required()
    def get(self) -> Response:
        users = Users.objects().exclude('password')
        if len(users) > 0:
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
                'password').get(user_id=user_id).to_json()

            return Response(user, mimetype="application/json", status=200)
        except DoesNotExist:
            return Response(status=404)

    @jwt_required()
    def patch(self, user_id: str) -> Response:
        schema = Kanpai.Object({
            'username': Kanpai.String(),
            'firstName': Kanpai.String(),
            'lastName': Kanpai.String(),
            'email': Kanpai.String(),
            'subjects_id': Kanpai.Array()
        })

        validate_result = schema.validate(request.get_json())
        if validate_result.get('success', False) is False:
            return Response(status=400)

        body = request.get_json()
        try:
            if len(body.get("subjects_id")) > 0:
                subjects_id = body.get("subjects_id")
                subject_list = []

                for i in subjects_id:
                    subject_list.append(Subjects.objects.get(subject_id=i))

            del body['subjects_id']

            Users.objects.get(user_id=user_id).update(
                **body, subjects=subject_list)

            return Response(status=200)
        except DoesNotExist:
            return Response(status=404)

    @jwt_required()
    def delete(self, user_id: str) -> Response:
        try:
            Users.objects.get(user_id=user_id).delete()
            return Response(status=200)
        except DoesNotExist:
            return Response(status=404)
