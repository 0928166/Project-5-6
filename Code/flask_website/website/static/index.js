function deleteCamera(cameraId) {
    fetch('/delete-camera', {
        method: 'POST',
        body: JSON.stringify( {cameraId: cameraId}),  
    }).then((_res) => {
        window.location.href = '/add-camera';
    });
}
function deleteUser(userId) {
    fetch('/delete-user', {
        method: 'POST',
        body: JSON.stringify( {userId: userId}),  
    }).then((_res) => {
        window.location.href = '/admin-page';
    });
}