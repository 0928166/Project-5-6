from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import IpCamera
from . import db
import json

# create camera blueprint, this allows us to define functions before an actual object exists
camera = Blueprint('camera', __name__)

# this route will be the main camera page where you can view all the cameras
@camera.route('/cameras')
@login_required
def cameras():
    # render the page
    return render_template("cameras.html", user = current_user)

# this route will be the page where you can add and remove cameras
@camera.route('/add-camera', methods=['GET', 'POST'])
@login_required
def add_camera():
    if request.method == "POST":
        # get form info
        ipcam_name = request.form.get('ipcam_name')
        ipcam_ip = request.form.get('ipcam_ip')
        # if name is too short, flash error
        if len(ipcam_name) < 1 or len(ipcam_name) > 20:
            flash('Name must be 1-20 characters', category='error')
        elif len(ipcam_ip) > 400:
            flash('ip is too long', category='error')
        # else create new camera that is linked to the currentuser and add it to the database
        else: 
            ip_cam = IpCamera(name=ipcam_name,ip=ipcam_ip, user_id=current_user.id)
            db.session.add(ip_cam)
            db.session.commit()
            flash('Camera added.', category='succes')
    # if get request, render page
    return render_template("add_cameras.html", user=current_user)

# this route enables the deletion of cameras, it has no visuals. it gets the info from the deleletecamera script in index.js
@camera.route('/delete-camera', methods=['POST'])
@login_required
def delete_camera():
    # get data from the json, search it in the database
    data = json.loads(request.data)
    camera_id = data['cameraId']
    camera = db.session.query(IpCamera).get(camera_id)
    # if the camera is found, chech if the camera is linked to the current user, if so delete it
    if camera:
        if camera.user_id == current_user.id:
            db.session.delete(camera)
            db.session.commit()
            return jsonify({})