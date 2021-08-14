from my_secrets import db_login, db_password, secret_key


SQLALCHEMY_DATABASE_URI = f'postgresql://{db_login}:{db_password}@localhost/oonote'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SECRET_KEY = secret_key
