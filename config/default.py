import os
from os.path import abspath, dirname
from dotenv import load_dotenv

APP_ROOT = dirname(dirname(abspath(__file__)))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

DEBUG = False
TESTING = False

ENV = os.getenv('FLASK_DEFAULT_ENV')

UPLOAD_FOLDER_DEST = os.getenv('UPLOAD_FOLDER')

SQLALCHEMY_TRACK_MODIFICATIONS = False
