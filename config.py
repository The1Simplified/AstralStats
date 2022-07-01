import secrets
import os


class Config:
    SECRET_KEY = f'{secrets.token_hex(16)}'
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username="Simpl1f1ed",
        password=os.environ.get("DB_PASSOWRD"),
        hostname="Simpl1f1ed.mysql.pythonanywhere-services.com",
        databasename=
        "Simpl1f1ed$AstralStats_DB",
    )
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    