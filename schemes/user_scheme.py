from app import ma
from models.user_model import Users


class UserSchema(ma.ModelSchema):
    class Meta:
       model = Users
