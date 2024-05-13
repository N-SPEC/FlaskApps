from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class area(db.Model):
    area_id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, area_id, area_name):
        self.area_id = area_id
        self.area_name = area_name

class position(db.Model):
    position_id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, nullable=False)
    position_name = db.Column(db.String(100), nullable=False, unique=True)   

    def __init__(self, position_id, area_id, position_name):
        self.position_id = position_id
        self.area_id = area_id
        self.position_name = position_name

class areapositionxref(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id'), nullable=False)

    def __init__(self, area_id, position_id):
        self.area_id = area_id
        self.position_id = position_id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))

    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username
