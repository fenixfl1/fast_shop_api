from flask import request, jsonify
from flask_restful import Resource
from app.common.schemas import ProductSchema
from app.database import db
from app.database.models import ProductCategory, Products as Product, ProductsImages
from app.common.utils import CustomException, eval_request, jsonify_schema
from app.controllers import create_products, get_products


class Products(Resource):
    def get(self):
        product = ProductCategory.query.all()
        return jsonify({'data': f'{product}'})

    def post(self):
        try:
            data: Products = request.json
            allowed_fields = ['NAME', 'DESCRIPTION', 'PRICE',
                              'CATEGORY_ID', 'STOCK', 'BRAND',
                              'MODEL', 'CONDITION', 'STATE',
                              'TAGS', 'PERCENT_DISCOUNT', 'COIN',
                              'CATEGORY_ID', 'FILES']

            if not data:
                raise CustomException('Missing JSON in request', 400)

            eval_request(allowed_fields, data, [
                'STATE', 'PERCENT_DISCOUNT', 'TAGS', 'FILES'])

            product = create_products(
                name=data.get('NAME'),
                description=data.get('DESCRIPTION'),
                price=float(data.get('PRICE')),
                stock=int(data.get('STOCK')),
                brand=data.get('BRAND'),
                model=data.get('MODEL'),
                coin=data.get('COIN'),
                condition=data.get('CONDITION'),
                state=data.get('STATE'),
                tags=data.get('TAGS'),
                percent_discount=float(data.get('PERCENT_DISCOUNT', 0.00)),
                categories_id=data.get('CATEGORY_ID'),
                files=list(data.get('FILES', []))
            )

            return jsonify_schema(ProductSchema, product)
        except CustomException as e:
            return jsonify({'message': e.message, 'status': e.status_code})

    def put(self): ...


class Product(Resource):
    def get(self, id):
        product = Product.query.get(id)
        return jsonify({'data': f'{product}'})

    def post(self):
        data = request.json
        product = get_products(category=data.get(
            'CATEGORY_ID'), product=data.get('NAME'), state=data.get('STATE'))

        return jsonify_schema(ProductSchema(many=True), product)

    def put(self, id): ...
    def delete(self, id): ...
