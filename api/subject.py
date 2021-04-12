from flask import request, Response, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from mongoengine import NotUniqueError, DoesNotExist
from kanpai import Kanpai

from models.subjects import Subjects


class SubjectsApi(Resource):
    @jwt_required()
    def get(self) -> Response:
        subjects = Subjects.objects()
        if len(subjects) > 0:
            response = jsonify(subjects)
            response.status_code = 200
            return response
        else:
            response = Response()
            response.status_code = 204
            return response

    @jwt_required()
    def post(self) -> Response:
        schema = Kanpai.Object({
            'code': Kanpai.String().required(),
            'name': Kanpai.String().required(),
            'instructor': Kanpai.String().required(),
        })

        validate_result = schema.validate(request.get_json())
        if validate_result.get('success', False) is False:
            return Response(status=400)

        body = request.get_json()
        try:
            Subjects(**body).save()
            return Response(status=201)
        except NotUniqueError:
            return Response("Subject code is already exist", status=400)


class SubjectApi(Resource):
    @jwt_required()
    def get(self, subject_id: str = None) -> Response:
        try:
            subject = Subjects.objects.get(id=subject_id).to_json()
            return Response(subject, mimetype="application/json", status=200)
        except DoesNotExist:
            return Response(status=404)

    @jwt_required()
    def patch(self, subject_id: str) -> Response:
        schema = Kanpai.Object({
            'name': Kanpai.String(),
            'instructor': Kanpai.String()
        })

        validate_result = schema.validate(request.get_json())
        if validate_result.get('success', False) is False:
            return Response(status=400)

        body = request.get_json()
        try:
            Subjects.objects.get(id=subject_id).update(**body)
            return Response(status=200)
        except DoesNotExist:
            return Response(status=404)

    @jwt_required()
    def delete(self, subject_id: str) -> Response:
        try:
            Subjects.objects.get(id=subject_id).delete()
            return Response(status=200)
        except DoesNotExist:
            return Response(status=404)
