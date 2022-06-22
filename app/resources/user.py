import json
from flask import Response, jsonify, request
from flask_restful import Resource
from app.common.models import User
from app.common.schemas import UserSchema
from app.common.utils import CustomException, eval_request
from app.common.session import get_access_token
from app.controllers import authenticate, create_user
from flask_jwt_extended import get_jwt_identity


class Users(Resource):
    def post(self) -> Response:
        try:
            fields = ['EMAIL', 'FIRST_NAME', 'LAST_NAME',
                      'PASSWORD', 'STATE', 'USERNAME']
            data = request.json

            if not data:
                return jsonify({'message': 'Missing JSON in request', 'status': 400})

            eval_request(fields, data, ['STATE'])

            for field in data:
                if field not in fields:
                    return jsonify({'message': f'"{field}" is not allowed.', 'status': 400})

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

    def post(self) -> Response:
        data: dict = request.json

        if not data:
            return jsonify({'message': 'Missing JSON in request'})

        username: str = data.get('USERNAME')
        password: str = data.get('PASSWORD')

        if not password:
            return jsonify({'message': 'Missing "PASSWORD" parameter'})
        if not username:
            return jsonify({'message': 'Missing "USERNAME" parameter'})
        try:
            user = authenticate(username, password)

            return get_access_token(user)
        except CustomException as e:
            return jsonify({'message': e.message, 'status': e.status_code})
