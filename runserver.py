
from app import create_app
from app.database import init_db
import os

setting_module = os.getenv('APP_DEVEOPMENT_SETTINGS_MODULE')
app = create_app(setting_module)

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run()
