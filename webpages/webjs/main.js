document.addEventListener('DOMContentLoaded', function () {
    const loginButton = document.querySelector('.login');
    const signupButton = document.querySelector('.signup');
    const slider = document.querySelector('.slider');

    // Function to update slider position based on the saved state
    function updateSliderPosition() {
        const lastClicked = localStorage.getItem('lastClickedButton');
        if (lastClicked === 'signup') {
            slider.style.left = '100px';
        } else {
            slider.style.left = '0';
        }
    }

    // Function to set the slider position and navigate
    function handleButtonClick(buttonType) {
        if (buttonType === 'login') {
            slider.style.left = '0';
            localStorage.setItem('lastClickedButton', 'login');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 500); // Adjust delay based on the slider's animation duration
        } else if (buttonType === 'signup') {
            slider.style.left = '100px';
            localStorage.setItem('lastClickedButton', 'signup');
            setTimeout(() => {
                window.location.href = 'signup.html';
            }, 500); // Adjust delay based on the slider's animation duration
        }
    }

    loginButton.addEventListener('click', function () {
        handleButtonClick('login');
    });

    signupButton.addEventListener('click', function () {
        handleButtonClick('signup');
    });

    // Update slider position when the page loads
    updateSliderPosition();
});
