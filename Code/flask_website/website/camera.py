#list all devices
#send list to browser
#capture images from selected devices?
#W
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import IpCamera
from . import db
import json
camera = Blueprint('camera', __name__)

@camera.route('/cameras')
@login_required
def cameras():
    return render_template("cameras.html", user = current_user)

@camera.route('/addCamera', methods=['GET', 'POST'])
@login_required
def addCamera():
    if request.method == "POST":
        ipcam_name = request.form.get('ipcam_name')
        ipcam_ip = request.form.get('ipcam_ip')
        if len(ipcam_name) < 1:
            flash('Name must be at least 1 character', 'error')
        else: 
            ip_cam = IpCamera(name=ipcam_name,ip=ipcam_ip, user_id=current_user.id)
            db.session.add(ip_cam)
            db.session.commit()
            flash('Camera added.', category='succes')
    return render_template("add_cameras.html", user=current_user)

@camera.route('/delete-camera', methods=['POST'])
@login_required
def delete_camera():
    data = json.loads(request.data)
    cameraId = data['cameraId']
    camera = IpCamera.query.get(cameraId)
    if camera:
        if camera.user_id == current_user.id:
            db.session.delete(camera)
            db.session.commit()
            return jsonify({})