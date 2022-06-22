from flask import Blueprint
from flask_restful import Api

from app.resources.products import Products, Product
from app.resources.user import LoginUser, Users
from .categories import Categories
from app.common.routes import *

api_bp = Blueprint('api_bp', __name__)
api = Api(api_bp, catch_all_404s=True)


api.add_resource(Product, '/product/filtered')
api.add_resource(Products, GET_PRODUCTS_LIST_PATH,
                 f'{GET_PRODUCTS_LIST_PATH}/add_products', endpoint='products')
api.add_resource(Categories, GET_CATEGORIES_PATH,
                 f'{GET_CATEGORIES_PATH}/<int:id>', endpoint='categories')
api.add_resource(Users, REGISTER_PATH,
                 F'{GET_USERS_PATH}/<int:id>', UPDATE_USER_PATH, endpoint='users')
api.add_resource(LoginUser, LOGIN_PATH, endpoint='login')
