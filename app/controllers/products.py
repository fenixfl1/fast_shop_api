import json
from app.common.models import Products
from app.common.utils import CustomException


class ProductControllers(object):

    @staticmethod
    def get_product(product_id) -> Products:
        return Products.get_by_id(product_id)

    @staticmethod
    def get_products(category: int = None, product: str = None, state: str = 'A') -> list[Products]:
        if category is not None:
            return Products.filter_by_category(category_id=category, product_name=product, state=state)
        elif product is not None:
            return Products.filter_by(dict(name=product, state=state))
        else:
            return Products.get_all()

    @staticmethod
    def create_product(name: str, description: str, stock: int, price: float, coin: str,
                       brand: str, model: str, condition: str, tags: str, category_id: int, percent_discount: float = None, added_at: str = None, state: str = 'A') -> Products:
        try:
            product = Products(
                name=name, description=description,
                stock=stock, price=price, coin=coin,
                brand=brand, model=model, condition=condition,
                tags=tags, percent_discount=percent_discount,
                added_at=added_at, state=state
            )
            product.commit()
            return product
        except CustomException:
            raise CustomException('unexpected value')

    @staticmethod
    def update_product(product_id, product):
        return Products.update_product(product_id, product)

    @staticmethod
    def delete_product(product_id):
        return Products().delete_product(product_id)
