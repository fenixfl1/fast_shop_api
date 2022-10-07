from datetime import datetime, timedelta
import json
from flask import Response, jsonify, request
from flask_restful import Resource
from app.database.models import User
from app.common.schemas import UserSchema
from app.common.utils import CustomException
from app.common.session import get_access_token
from app.controllers import authenticate, create_user
from flask_jwt_extended import get_jwt_identity
from cerberus import Validator
from app.common.rules import *

validator = Validator()


class Users(Resource):
    global validator

    def post(self) -> Response:

        try:
            data = request.json

            if not validator.validate(data, rules['user_schema']):
                return jsonify({'message': validator.errors, 'status': 400})

            user = create_user(**data)

            if user is not None:
                user_schema = UserSchema()
                return json.loads(user_schema.dumps(user))
        except CustomException as e:
            return jsonify({'message': e.message, 'status': e.status_code})

    def get(self, id: str) -> Response: ...

    def put(self) -> Response:
        data = request.json
        user_id = get_jwt_identity()

        current_user = User.get_by_id(user_id)

        updated_user = current_user.update(**data)
        return json.loads(UserSchema().dumps(updated_user))


class LoginUser(Resource):
    global validator

    def post(self) -> Response:
        data: dict = request.json

        if not data:
            return jsonify({'message': 'Missing JSON in request'})

        if not validator.validate(data, rules['login_schema']):
            return jsonify({'message': validator.errors, 'status': 400})
        else:
            try:
                expires = datetime.now() + timedelta(days=1)
                if data.get('REMEMBER_ME'):
                    expires = datetime.now() + timedelta(days=30)
                user = authenticate(data.get('USERNAME'), data.get('PASSWORD'))

                return get_access_token(user, expires)
            except CustomException as e:
                return jsonify({'message': e.message, 'status': e.status_code})
