import os

class Config:
    SECRET_KEY = os.urandom(32)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'