import datetime
# from sqlalchemy.orm import validates
from app import db

""" This section defines the Users model to create table in the database """


# Users Details  model
class Users(db.Model):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    mobile = db.Column(db.String(15),nullable=False,unique=True)
    createdAt = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updatedAt = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())

    # @validates('email')
    # def validate_email(self, key, address):
    #     if re.search('@',address) is None:
    #         return {"message":"invalid Emailid Formate"}
    #     if re.search('.',address) is None:
    #         return {"message":"invalid Emailid Formate"}