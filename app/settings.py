from os import environ 
from dotenv import load_dotenv

load_dotenv(".flaskenv")
SECRET_KEY = environ.get('SECRET_KEY')
ENVIRONMENT = environ.get('FLASK_ENV')
