from flask import current_app, jsonify, Response
from flask_jwt_extended import create_access_token
from flask_principal import identity_changed, Identity
from app.database.models import User


def get_access_token(user: User, expire=0) -> Response:
    access_token = create_access_token(
        identity=user.id, expires_delta=False)

    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(user.id))

    return jsonify({
        'data': {
            'username': user.first_name,
            'userId': user.id,
            'name': f'{user.first_name} {user.last_name}',
            'sessionCookie': {
                'token': f'Bearer {access_token}',
                'expires': f'{expire}'
            }
        },
        'message': f'Wellcome {user.first_name} {user.last_name}'
    })
