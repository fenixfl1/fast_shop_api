from app.extensions import ma
from app.database.models import Categories, Products, User
from marshmallow import fields

category_url = 'api_bp.categories'


class CategorySchema(ma.SQLAlchemySchema):
    global category_url

    class Meta:
        model = Categories

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor(category_url, values=dict(id="<id>")),
            "collection": ma.URLFor(category_url),
        }
    )


class ProductSchema(ma.SQLAlchemySchema):
    global category_url

    class Meta:
        model = Products

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    price = ma.auto_field()
    category = ma.List(ma.HyperlinkRelated("api_bp.categories"))

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api_bp.products", values=dict(id="<id>")),
            "related": ma.URLFor(category_url, values=dict(id="<id>")),
            "collection": ma.URLFor(category_url),
        }
    )


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()
    email = ma.auto_field()
    last_login = ma.auto_field()
    date_joined = ma.auto_field()

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api_bp.users", values=dict(id="<id>")),
            "collection": ma.URLFor("api_bp.users"),
        }
    )
