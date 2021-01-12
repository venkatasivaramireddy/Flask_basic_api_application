import re

from flask import request, make_response, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from app import db
from models.user_model import Users
from schemes.user_scheme import UserSchema


class SignUp(Resource):
    def __init__(self):
        self.mandatory_keys = ['username','email','password','mobile']
        self.invalid_keys = []
        self.missing_keys = []

    def post(self):
        """
        body:
        {
            "username":"",
            "email":"",
            "mobile":"",
            "password":""
        }

        This method is used to register the user into db
        :return: dict
        """
        try:
            meta_data_dict = request.get_json()
            for keys in meta_data_dict.keys():
                if keys not in self.mandatory_keys:
                    self.invalid_keys.append(keys)

            for x in self.mandatory_keys:
                if x not in meta_data_dict.keys():
                    self.missing_keys.append(x)

            if len(self.missing_keys) >0:
                return make_response(
                    jsonify({'message': "Missing {} Key".format(self.missing_keys), 'status_code': 400}), 400)

            if len(self.invalid_keys) >0:
                return make_response(jsonify({'message': "{} Is In_Valid Key".format(self.invalid_keys), 'status_code': 400}), 400)

            try:
                name = meta_data_dict['username']
                email = meta_data_dict['email']
                password = meta_data_dict['password']
                mobile = meta_data_dict["mobile"]
            except Exception as e:
                return make_response(
                    jsonify({'message': "Missing {} Key".format(str(e)), 'status_code': 400}), 400)

            email_status = self.validate_email(address=email)
            if 'ErrorMessage' in email_status:
                return make_response(jsonify({'message': email_status['ErrorMessage'], 'status_code': 400}), 400)

            dict ={"email" :email ,"password" :password ,"username" :name,"mobile" :mobile}
            status = bool(Users.query.filter_by(email=email).first())
            email_id = db.session.query(Users).filter(Users.email == email).first()
            if email_id is None and status is False:
                name_status = self.validate_user_name(address=name)
                if 'ErrorMessage' in name_status:
                    return make_response(jsonify({'message': name_status['ErrorMessage'], 'status_code': 400}), 400)
                mobile_status = self.validate_mobile_number(address=mobile)
                if 'ErrorMessage' in mobile_status:
                    return make_response(jsonify({'message': mobile_status['ErrorMessage'], 'status_code': 400}), 400)
                password_status = self.validate_password(password=password)
                if 'ErrorMessage' in password_status:
                    return make_response(jsonify({'message': password_status['ErrorMessage'], 'status_code': 400}), 400)

                hash_password = generate_password_hash(password)
                schema = UserSchema()
                new_signup = schema.load(dict, session = db.session).data
                new_signup.password = hash_password
                db.session.add(new_signup)
                db.session.commit()
                schema = UserSchema()
                user = db.session.query(Users).filter(Users.email == email).one()
                data = schema.dump(new_signup).data
                print(data)
                return make_response(jsonify({'message': "Successfully Register, Login Using Email & Password", 'status_code': 201}), 201)
            else:
                return make_response(jsonify({'message': "Email Already Exist", 'status_code': 400}), 400)
        except Exception as e:
            try:
                error = e.args[0]
            except:
                error = "Data Insertion Error"
            return make_response(jsonify({'message': str(error), 'status_code': 400}), 400)

    def validate_email(self,address):
        if re.search('@', address) is None:
            return {"ErrorMessage": "Email Should have @ -> Ex: a@b.c"}
        if re.search('.', address) is None:
            return {"ErrorMessage": "Email Should have . -> Ex: a@b.c"}
        return {}

    def validate_user_name(self,address):
        length = len(address)
        if length >8:
            return {"ErrorMessage": "Username max length should be 8"}
        return {}

    def validate_mobile_number(self,**kwrg):
        number = kwrg.get('address')
        if re.match('^[6-9]\d{9}$',number) is None:
            return {"ErrorMessage": "Phone Number must be a valid Indian Cell phone number -> Ex. 9876543210"}
        return {}

    def validate_password(self, password):
        if re.match('^(?=.*?[A-Za-z])(?=.*?[0-9])(?=.*?[#_-]).{6,}$', password) is None:
            return {"ErrorMessage": "Password must contain at least one character, one number "
                               "and any one of these (underscore, hyphen, hash) and max length should be 6"}
        return {}
