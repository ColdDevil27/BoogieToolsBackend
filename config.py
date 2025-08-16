import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

config = {'default': Config}