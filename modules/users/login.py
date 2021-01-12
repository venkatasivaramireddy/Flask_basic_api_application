from flask import request, make_response, jsonify, session
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource
from werkzeug.security import check_password_hash

from app import db
from models.user_model import Users
from schemes.user_scheme import UserSchema


class Login(Resource):

    def __init__(self):
        super().__init__()

    def post(self):
        """
        body:
        {
            "email":" ",
            "password":" "
        }
        This method is used to get Token if user credentials is valid
        :return: dict
        """
        try:
            meta_data_dict = request.get_json()
            try:
                email = meta_data_dict['email']
                password = meta_data_dict['password']
            except Exception as e:
                return make_response(
                    jsonify({'message': "Missing {} Key".format(str(e)), 'status_code': 400}), 400)
            username_check = db.session.query(Users).filter(Users.email == email).first()
            if username_check is not None:
                schema = UserSchema()
                data = schema.dump(username_check).data
                hashed_password = username_check.password
                if check_password_hash(hashed_password, password):
                    data = {
                        'access_token': create_access_token(identity=email),
                        'refresh_token': create_refresh_token(identity=email)
                    }
                    session.permanent = True
                    return make_response(jsonify({'result':data,'message': "Successfully Loged In", 'status_code': 200}), 200)
                else:
                    return make_response(jsonify({'message': 'Invalid Password', 'status_code': 401}), 401)
            else:
                return make_response(jsonify({'message': 'Invalid Email', 'status_code': 401}), 401)
        except Exception as e:
            return make_response(jsonify({'message': str(e), 'status_code': 400}), 400)
