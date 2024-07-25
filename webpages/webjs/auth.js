// auth.js

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const logoutButton = document.getElementById('logoutButton');

    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(loginForm);
            const data = {};

            // Convert FormData to JSON object
            formData.forEach((value, key) => {
                data[key] = value;
            });

            console.log('Login data:', data); // Log data being sent

            try {
                const response = await fetch('http://127.0.0.1:5000/api/users/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)  // Convert data object to JSON
                });

                if (response.ok) {
                    const result = await response.json();
                    console.log('Login successful:', result);
                    localStorage.setItem('token', result.token);
                    window.location.href = 'dashboard.html'; // Redirect to dashboard
                } else {
                    const error = await response.json();
                    console.log('Login error:', error);
                    alert(`Login failed: ${error.message}`);
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('An unexpected error occurred during login.');
            }
        });
    }

    // Handle signup form submission
    if (signupForm) {
        signupForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(signupForm);
            const data = {};

            // Convert FormData to JSON object
            formData.forEach((value, key) => {
                data[key] = value;
            });

            // Map fields to match backend expectations
            const mappedData = {
                username: data.uname,  // Map 'uname' to 'username'
                password: data.passwd, // Map 'passwd' to 'password'
                email: data.email,     // Ensure your form has an email field
                firstname: data.fname, // Map 'fname' to 'firstname'
                lastname: data.lname   // Map 'lname' to 'lastname'
            };

            console.log('Signup data:', mappedData); // Log data being sent

            try {
                const response = await fetch('http://127.0.0.1:5000/api/users/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(mappedData)  // Convert data object to JSON
                });

                if (response.ok) {
                    alert('Signup successful! Please log in.');
                    window.location.href = 'login.html'; // Redirect to login page
                } else {
                    const error = await response.json();
                    console.log('Signup error:', error); // Log error details
                    alert(`Signup failed: ${error.message}`);
                }
            } catch (error) {
                console.error('Error during signup:', error);
                alert('An unexpected error occurred during signup.');
            }
        });
    }

    // Handle logout button click
    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/users/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });

                if (response.ok) {
                    console.log('Logout successful');
                } else {
                    console.log('Logout error');
                }

                // Remove the token from localStorage
                localStorage.removeItem('token');

                // Redirect to the homepage or login page
                window.location.href = 'app.html'; // Change as needed
            } catch (error) {
                console.error('Error during logout:', error);
                // Optionally handle errors here
                window.location.href = 'index.html'; // Change as needed
            }
        });
    }
});
