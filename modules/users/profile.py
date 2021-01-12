from flask import make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app import db
from models.user_model import Users
from schemes.user_scheme import UserSchema


class Profile(Resource):
    @jwt_required
    def __init__(self):
        super().__init__()
        self.email = get_jwt_identity()

    def get(self):
        """
        This method is used to get the user profile information if user access token is valid
        :return: dict
        """
        schema = UserSchema()
        user = db.session.query(Users).filter(Users.email == self.email).one()
        data = schema.dump(user).data
        return make_response(jsonify({'result': data, 'status_code': 200}), 200)
