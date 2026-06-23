import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///streampy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY', '')
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB upload limit
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'media')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
