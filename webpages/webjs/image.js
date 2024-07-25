document.addEventListener('DOMContentLoaded', () => {
    const uploadImagesLink = document.getElementById('uploadImagesLink');
    const googleDriveLink = document.getElementById('googleDriveLink');
    const dropboxLink = document.getElementById('dropboxLink');

    // Upload local files
    if (uploadImagesLink) {
        uploadImagesLink.addEventListener('click', () => {
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = 'image/*';
            fileInput.addEventListener('change', async () => {
                const file = fileInput.files[0];
                const formData = new FormData();
                formData.append('image', file);

                try {
                    const response = await fetch('http://127.0.0.1:5000/api/images/upload', {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}` // Changed 'authToken' to 'token'
                        },
                        body: formData
                    });

                    if (response.ok) {
                        const result = await response.json();
                        console.log('Upload successful:', result);
                        alert('Image uploaded and compressed successfully!');
                    } else {
                        const error = await response.json();
                        console.error('Upload error:', error);
                        alert(`Upload failed: ${error.message}`);
                    }
                } catch (error) {
                    console.error('Error during upload:', error);
                    alert('An unexpected error occurred during upload.');
                }
            });
            fileInput.click();
        });
    }

    // Google Drive upload
    if (googleDriveLink) {
        googleDriveLink.addEventListener('click', () => {
            const url = prompt('Enter Google Drive image URL:');
            const accessToken = prompt('Enter your Google Drive access token:');
            if (url && accessToken) {
                uploadFromUrl(url, 'google_drive', accessToken);
            }
        });
    }

    // Dropbox upload
    if (dropboxLink) {
        dropboxLink.addEventListener('click', () => {
            const url = prompt('Enter Dropbox image URL:');
            const accessToken = prompt('Enter your Dropbox access token:');
            if (url && accessToken) {
                uploadFromUrl(url, 'dropbox', accessToken);
            }
        });
    }

    async function uploadFromUrl(url, service, accessToken) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/images/upload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}` // Changed 'authToken' to 'token'
                },
                body: JSON.stringify({ url: url, service: service, access_token: accessToken })
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Upload successful:', result);
                alert('Image uploaded and compressed successfully!');
            } else {
                const error = await response.json();
                console.error('Upload error:', error);
                alert(`Upload failed: ${error.message}`);
            }
        } catch (error) {
            console.error('Error during upload:', error);
            alert('An unexpected error occurred during upload.');
        }
    }

    // Optional: Handle download links if needed
    document.body.addEventListener('click', (event) => {
        if (event.target && event.target.matches('.btn-download')) {
            // Example handling code if needed
            console.log('Download link clicked:', event.target.href);
        }
    });
});
