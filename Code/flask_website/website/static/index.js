function deleteCamera(cameraId) {
    fetch('/delete-camera', {
        method: 'POST',
        body: JSON.stringify( {cameraId: cameraId}),  
    }).then((_res) => {
        window.location.href = '/addCamera';
    });
}