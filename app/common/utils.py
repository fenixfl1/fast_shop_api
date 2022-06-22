import json
from flask import Response
from app.database import db


class ModelMixing(object):

    def commit(self):
        db.add(self)
        db.commit()

    def delete(self):
        db.delete(self)
        db.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.commit()
        return self


class CustomException(Exception):
    status_code = 400

    def __init__(self, message, code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if code is not None:
            self.status_code = code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def eval_request(fields: list[str], request: dict, exclude: list[str] = None) -> None:
    for field in fields:
        if field in exclude:
            continue
        if field not in request:
            raise CustomException(f'Missing "{field}" in parameter')


def jsonify_schema(schema, object) -> Response:
    return json.loads(schema.dumps(object))
