from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class IpCamera(db.Model): #change to camera stuff later
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    ip = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    user_cameras = db.relationship('IpCamera')

