document.getElementById('id_video').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const videoPreview = document.getElementById('videoPreview');
    const errorMessage = document.getElementById('errorMessage');

    // Clear previous error messages and video source
    errorMessage.textContent = '';
    videoPreview.src = '';

    if (file) {
        // Check file size (30MB = 30 * 1024 * 1024 bytes)
        if (file.size > 30 * 1024 * 1024) {
            errorMessage.textContent = 'Error: Video file size exceeds 30MB.';
            return;
        }

        // Check video duration
        const videoElement = document.createElement('video');
        videoElement.preload = 'metadata';

        videoElement.onloadedmetadata = function() {
            window.URL.revokeObjectURL(videoElement.src);
            const duration = videoElement.duration;

            if (duration > 300) { // 300 seconds = 5 minutes
                errorMessage.textContent = 'Error: Video duration exceeds 5 minutes.';
            } else {
                // Video is valid, show preview
                videoPreview.src = URL.createObjectURL(file);
                videoPreview.load();
            }
        };

        videoElement.onerror = function() {
            errorMessage.textContent = 'Error: Unable to load video metadata.';
        };

        videoElement.src = URL.createObjectURL(file);
    } else {
        errorMessage.textContent = 'Please select a video file.';
    }
});

document.getElementById('post').addEventListener('submit', function(event) {
    event.preventDefault();

    // Show the uploading overlay
    document.getElementById('uploadingOverlay').classList.remove('hidden');
    
    // Show the loading bar
    document.getElementById('loading-bar-container').style.display = 'block';

    // Submit the form programmatically with fetch
    const form = event.target; // Use event.target to reference the form
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle successful response
        console.log(data);
        document.getElementById('uploadingOverlay').classList.add('hidden');
        document.getElementById('loading-bar-container').style.display = 'none';
    })
    .catch(error => {
        // Handle error
        console.error('There has been a problem with your fetch operation:', error);
        document.getElementById('uploadingOverlay').classList.add('hidden');
        document.getElementById('loading-bar-container').style.display = 'none';
    });
});