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
                    console.log('Uploading image...');
                    const response = await fetch('http://127.0.0.1:5000/api/images/upload', {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        },
                        body: formData
                    });

                    if (response.ok) {
                        const result = await response.json();
                        console.log('Upload successful:', result);
                        alert('Image uploaded successfully!');

                        // Extract image ID from the result object
                        const imageId = result.image.id;

                        // Update the compression button with the image ID
                        updateCompressionButton(imageId);
                        updateDownloadButton(imageId);
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

    // Function to update the compression button
    function updateCompressionButton(imageId) {
        const compressButton = document.querySelector('.btn-compress');
        if (compressButton) {
            console.log(`Updating compression button with image ID: ${imageId}`);
            compressButton.href = '#';  // Update href to prevent default anchor behavior
            compressButton.setAttribute('data-id', imageId);
        }
    }

    // Function to update the download button
    function updateDownloadButton(imageId) {
        const downloadButton = document.querySelector('.btn-download');
        if (downloadButton) {
            console.log(`Updating download button with image ID: ${imageId}`);
            downloadButton.setAttribute('data-id', imageId);
        }
    }

    // Handle compression button click
    document.body.addEventListener('click', async (event) => {
        if (event.target && event.target.matches('.btn-compress')) {
            event.preventDefault();  // Prevent default anchor behavior
            const imageId = event.target.getAttribute('data-id');
            console.log(`Compress button clicked for image ID: ${imageId}`);
            await compressImage(imageId);
        }
    });

    async function compressImage(imageId) {
        try {
            console.log(`Compressing image with ID: ${imageId}`);
            const response = await fetch('http://127.0.0.1:5000/api/images/compress', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image_id: imageId })
            });

            console.log(`Fetch response status: ${response.status}`);
            if (response.ok) {
                const result = await response.json();
                console.log('Compression successful:', result);
                alert('Image compressed successfully!');
            } else {
                const error = await response.json();
                console.error('Compression error:', error);
                alert(`Compression failed: ${error.message}`);
            }
        } catch (error) {
            console.error('Error during compression:', error);
            alert('An unexpected error occurred during compression.');
        }
    }

    // Handle download button click
    document.body.addEventListener('click', async (event) => {
        if (event.target && event.target.matches('.btn-download')) {
            event.preventDefault();  // Prevent default anchor behavior
            const imageId = event.target.getAttribute('data-id');
            console.log(`Download button clicked for image ID: ${imageId}`);
            await downloadImage(imageId);
        }
    });

    async function downloadImage(imageId) {
        try {
            console.log(`Downloading image with ID: ${imageId}`);
            const response = await fetch('http://127.0.0.1:5000/api/images/download', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image_id: imageId })
            });

            if (response.ok) {
                const result = await response.blob();
                // Create a temporary link to download the file
                const url = window.URL.createObjectURL(result);
                const a = document.createElement('a');
                a.href = url;
                a.download = `image_${imageId}.zst`; // Modify as needed
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                console.log('Download successful!');
            } else {
                const error = await response.json();
                console.error('Download error:', error);
                alert(`Download failed: ${error.message}`);
            }
        } catch (error) {
            console.error('Error during download:', error);
            alert('An unexpected error occurred during download.');
        }
    }
});
