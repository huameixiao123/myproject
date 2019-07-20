import os

DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI ="mssql+pyodbc://root:qwe123@book"

SECRET_KEY = os.urandom(30)