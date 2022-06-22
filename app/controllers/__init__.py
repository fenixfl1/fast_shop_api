from .users import UserControllers
from .products import ProductControllers

# user controllers
authenticate = UserControllers.authenticate
create_user = UserControllers.create_user

# product controllers
create_products = ProductControllers.create_product
get_products = ProductControllers.get_products
get_product = ProductControllers.get_product
