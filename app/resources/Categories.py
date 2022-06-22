import json
from flask import request, jsonify
from flask_restful import Resource
from app.common.models import Categories as ct
from app.common.schemas import CategorySchema


class Categories(Resource):
    def get(self, *args, **kwargs):
        try:
            category: ct
            categories_schema: CategorySchema

            part_url: list = request.path.split('/')
            id_from_query: str = request.query_string.decode('utf-8')

            id_from_url: int = int(part_url[-1])

            part_url: list = request.path.split('/')

            if id_from_query or id_from_url > 0:
                category = ct.query.filter_by(
                    id=id_from_query.split('=')[1]).first()
                categories_schema = CategorySchema()
            else:
                category = ct.query.all()
                categories_schema = CategorySchema()

            return json.loads(categories_schema.dumps(category))
        except Exception as e:
            return jsonify({"error": str(e)})

    def put(self): ...
