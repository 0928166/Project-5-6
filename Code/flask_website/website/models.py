from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

# this contains the database models, these models what the tables in the database will look like
# IpCamera is the model where the Ip camera data will be stored, and what user it is linked to
class IpCamera(db.Model): #change to camera stuff later
    id = db.Column(db.Integer, primary_key=True) # unique id to make sure all cameras are identifable
    name = db.Column(db.String(20)) # name
    ip = db.Column(db.String(400)) # the ip to the camera stream
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # user the camera is linked to

# User will be used to store the userdata
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # unique id to make sure the users are unique
    username = db.Column(db.String(20), unique=True) # username, must be unique
    password = db.Column(db.String(40)) # password
    first_name = db.Column(db.String(20)) # first name
    is_admin = db.Column(db.Boolean, default=False, nullable= False) # check if the user is an admin user, by default only the admin account will be admin
    user_cameras = db.relationship('IpCamera') # the ids of the cameras that are linked to the user
