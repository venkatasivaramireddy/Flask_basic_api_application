from app import ma, db
from models.user_model import Users


class UserSchema(ma.ModelSchema):
    class Meta:
       model = Users
       fields = ("id", "username", "email", "mobile", "password", "createdAt")
       sqla_session = db.session
