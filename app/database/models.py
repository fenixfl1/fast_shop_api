from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, CHAR, and_, select
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..common.utils import ModelMixing
from werkzeug.security import generate_password_hash, check_password_hash
from . import Base, db


class Categories(Base, ModelMixing):
    __tablename__ = 'CATEGORIES'

    id = Column('CATEGORY_ID', Integer, primary_key=True)
    name = Column('NAME', String(50), nullable=False, unique=True)
    description = Column('DESCRIPTION', String(150), nullable=False)
    state = Column('STATE', CHAR(1), nullable=False, default='A')

    def __repr__(self) -> str:
        return f'{self.name}'

    @staticmethod
    def get_by_id(id: int) -> 'Categories':
        return Categories.query.get(id)

    @staticmethod
    def get_by_name(name: str) -> 'Categories':
        return Categories.query.filter_by(name=name).first()

    @staticmethod
    def get_all() -> 'User':
        return User.query.all()


class ProductCategory(Base, ModelMixing):
    __tablename__ = 'PRODUCT_CATEGORY'

    id = Column('PRODUCTS_CATEGORY_ID', Integer, primary_key=True)
    category_id = Column('CATEGORY_ID', Integer,
                         ForeignKey('CATEGORIES.CATEGORY_ID'))
    product_id = Column('PRODUCT_ID', Integer,
                        ForeignKey('PRODUCTS.PRODUCT_ID'))
    state = Column('STATE', CHAR(1), nullable=False, default='A')

    def __init__(self, category_id: int, product_id: int, state: str = 'A'):
        self.category_id = category_id
        self.product_id = product_id
        self.state = state

    def __repr__(self) -> str:
        return f'{self.id}'

    @staticmethod
    def get_by_id(id: int) -> 'ProductCategory':
        return ProductCategory.query.get(id)

    @staticmethod
    def get_all() -> 'User':
        return User.query.all()


class Products(Base, ModelMixing):
    __tablename__ = 'PRODUCTS'

    id = Column('PRODUCT_ID', Integer, primary_key=True)
    name = Column('NAME', String(100), nullable=False)
    description = Column('DESCRIPTION', String(500))
    stock = Column('STOCK', Integer, nullable=False)
    price = Column('PRICE', Float(2), nullable=False)
    coin = Column('COIN', String(5), nullable=False, default='RD')
    percent_discount = Column('PERCENT_DISCOUNT', Float(2), default=0.00)
    brand = Column('BRAND', String(50))
    model = Column('MODEL', String(50))
    condition = Column('CONDITION', String(50), nullable=False,
                       default='NEW', comment='NEW, USED, USED LIKE NEW, ....')
    tags = Column('TAGS', String(150),
                  comment='Each tag must be separated by #')
    added_at = Column('ADDEDD_AT', Date(), nullable=False, default=func.now())
    images = relationship('ProductsImages', back_populates='')
    state = Column('STATE', CHAR(1), nullable=False, default='A')

    # constructor
    def __init__(self, name: str, description: str, stock: int, price: float, coin: str,
                 brand: str, model: str, condition: str, tags: str, percent_discount: float = None, added_at: str = None, state: str = 'A'):
        self.name = name
        self.description = description
        self.stock = stock
        self.price = price
        self.coin = coin
        self.percent_discount = percent_discount
        self.brand = brand
        self.model = model
        self.condition = condition
        self.tags = tags
        self.added_at = added_at
        self.state = state

    def __repr__(self) -> str:
        return f'{self.name}'

    @staticmethod
    def get_by_id(id: int) -> 'Products':
        return Products.query.get(id)

    @staticmethod
    def filter_by(**kwargs: dict) -> 'Products':
        return Products.query.filter_by(**kwargs)

    @staticmethod
    def filter_by_category(category_id: int, product_name: str, state: str = 'A') -> list['Products']:
        return Products.query.filter(and_(Products.state == state, Products.name.like(f'%{product_name}%'), Products.id.in_(select([ProductCategory.product_id])
                                                                                                                            .where(ProductCategory.category_id == category_id)))).all()

    @staticmethod
    def get_all() -> 'Products':
        return Products.query.all()

    def add_images(self, **kwargs):
        image = ProductsImages(**kwargs)
        image.product_id = self.id
        image.commit()


class ProductsImages(Base, ModelMixing):
    __tablename__ = 'PRODUCTS_IMAGES'

    id = Column('PRODUCT_IMAGE_ID', Integer, primary_key=True)
    name = Column('NAME', String(50), nullable=False)
    extention = Column('EXTENTION', String(5), nullable=False)
    img_url = Column('IMG_URL', String(100), nullable=False)
    product_id = Column(Integer, ForeignKey(
        'PRODUCTS.PRODUCT_ID', ondelete='CASCADE'))
    product = relationship('Products', back_populates='images')
    state = Column('STATE', CHAR(1), nullable=False, default='A')

    def __init__(self, name: str, extention: str, img_url: str, product_id: int, state: str = 'A'):
        self.name = name
        self.extention = extention
        self.img_url = img_url
        self.product_id = product_id
        self.state = state

    def __repr__(self) -> str:
        return f'{self.img_url}'

    @staticmethod
    def get_by_id(id: int) -> 'ProductsImages':
        return ProductsImages.query.get(id)


class User(Base, ModelMixing):
    __tablename__ = 'USERS'

    id = Column('USER_ID', Integer, primary_key=True, autoincrement=True)
    username = Column('USERNAME', String(50), nullable=False, unique=True)
    password = Column('PASSWORD', String(255), nullable=False)
    email = Column('EMAIL', String(50), nullable=False, unique=True)
    first_name = Column('FIRST_NAME', String(50), nullable=False)
    last_name = Column('LAST_NAME', String(50), nullable=False)
    state = Column('STATE', CHAR(1), nullable=False, default='A')
    last_login = Column('LAST_LOGIN', Date())
    date_joined = Column('DATE_JOINED', Date(),
                         nullable=False, default=func.now())

    def __init__(self, **kwargs):
        self.username = kwargs.get('USERNAME')
        self.email = kwargs.get('EMAIL')
        self.first_name = kwargs.get('FIRST_NAME')
        self.last_name = kwargs.get('LAST_NAME')
        self.state = kwargs.get('STATE', 'A')
        self.date_joined = kwargs.get('DATE_JOINED', func.now())

    def __repr__(self) -> str:
        return f'{self.username}'

    @staticmethod
    def get_by_id(id: int) -> 'User':
        return User.query.get(id)

    @staticmethod
    def filter_by(**kwargs: dict) -> 'User':
        return User.query.filter_by(**kwargs)

    @staticmethod
    def get_all() -> 'User':
        return User.query.all()

    def set_password(self, password: str) -> str:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def is_authenticated(self) -> bool:
        return True
