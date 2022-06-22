import base64
import os
from app.database import db
from app.database.models import ProductCategory, Products, ProductsImages
from app.common.utils import CustomException
from flask import current_app as app


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
                       brand: str, model: str, condition: str, tags: str, categories_id: list[int], files: list[dict], percent_discount: float = None, state: str = 'A') -> Products:
        try:
            product = Products(
                name=name, description=description,
                stock=stock, price=price, coin=coin,
                brand=brand, model=model, condition=condition,
                tags=tags, percent_discount=percent_discount,
            )
            product.commit()

            if product.id:
                db.add_all([ProductCategory(category_id=category_id,
                                            product_id=product.id) for category_id in categories_id])
                db.commit()

            if files:
                ProductControllers.save_files(product.id, files)

            return product
        except CustomException:
            raise CustomException('unexpected value')

    @staticmethod
    def update_product(product_id, product):
        return Products.update_product(product_id, product)

    @staticmethod
    def delete_product(product_id):
        return Products().delete_product(product_id)

    @staticmethod
    def save_files(product_id: int, files: list[dict]):
        try:
            db.add_all(
                [ProductsImages(product_id=product_id,
                                extention=image.get('EXTENTION'),
                                name=image.get('NAME'),
                                img_url=image.get('IMG_URL'),
                                state=image.get('STATE')) for image in files])
            for image in files:
                if image.get('IMG_URL'):
                    file_name = image.get('NAME')
                    ext = image.get('EXTENTION')
                    with open(os.path.join(
                            app.config['UPLOAD_FOLDER_DEST'], f'{file_name}.{ext}'), 'wb') as f:
                        f.write(base64.b64decode(image.get('STRING_FILE')))

            db.commit()
        except CustomException:
            raise CustomException('unexpected value')
