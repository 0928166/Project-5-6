// script to delete the camera, sends cameraId to the python method in /delete-camera section of camera.py
function deleteCamera(cameraId) {
    fetch('/delete-camera', {
        method: 'POST',
        body: JSON.stringify( {cameraId: cameraId}),  
    }).then((_res) => {
        window.location.href = '/add-camera';
    });
}
// script to remove a user, sends userId to the python method in /delete-user section of admin.py
function deleteUser(userId) {
    fetch('/delete-user', {
        method: 'POST',
        body: JSON.stringify( {userId: userId}),  
    }).then((_res) => {
        window.location.href = '/admin-page';
    });
}
