import datetime
import os

from flask import Flask, session
from flask_cors import CORS
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
# from cachetools import cached, TTLCache

app = Flask(__name__)
# cache = TTLCache(maxsize=100, ttl=60)
# app.config.from_object(__name__)
ma = Marshmallow(app)
CORS(app)
api = Api(app)

#jwt
jwt = JWTManager(app)
blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

#version & Env
APP_NAME = 'ENGAGE'
VERSION = "0.0.1.1"

ACTIVE_ENV = ''
ENV_VARIABLE = os.environ.get("ENV") or os.environ.get("FLASK_ENV")
if os.environ.get("FLASK_ENV") is not None or os.environ.get("FLASK_ENV") != '':
    ENV_VARIABLE = os.environ.get("FLASK_ENV")
else:
    ENV_VARIABLE = os.environ.get("ENV")

# db
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin:admin@localhost/test_user_db"
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = '3b8d7b303173189153979542'
db = SQLAlchemy(app)
db.init_app(app)

# jwt
app.config['JWT_SECRET_KEY'] = 'thisisasecretkey'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=5)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(minutes=5)
app.config['PROPAGATE_EXCEPTIONS'] = True

#session
app.permanent_session_lifetime = datetime.timedelta(minutes=5)

#endpoints
from modules.users.login import Login
from modules.users.logout import Logout
from modules.users.profile import Profile
from modules.users.sigup import SignUp

api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Profile, '/profile')


if __name__ == '__main__':
    app.run(debug=False)

