import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:admin@localhost/paciente_enfermero"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    LOG_FILE = "log.txt"
