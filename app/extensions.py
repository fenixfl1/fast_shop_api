from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_principal import Principal
from flask_jwt_extended import JWTManager


ma = Marshmallow()
mi = Migrate()
cors = CORS()
principal = Principal()
jwt = JWTManager()
