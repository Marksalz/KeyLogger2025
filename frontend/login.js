document.getElementById('loginForm').addEventListener('submit', function (event) {
    /**
     * Event listener for the login form submission.
     * Prevents the default form submission behavior and checks the password.
     *
     * @param {Event} event - The form submission event.
     */
    event.preventDefault();
    const password = document.getElementById('password').value;

    checkPassword(password).then(response => {
        /**
         * Handles the response from the password check.
         * If the password is correct, stores a login flag in local storage and redirects to the index page.
         * Otherwise, alerts the user that the password is incorrect.
         *
         * @param {boolean} response - The response indicating if the password is correct.
         */
        if (response) {
            localStorage.setItem('isLoggedIn', 'true');
            window.location.href = 'index.html';
        } else {
            alert('Wrong password!');
            document.getElementById('password').value = '';
        }
    });
});

/**
 * Checks the provided password by sending it to the server.
 *
 * @param {string} password - The password to check.
 * @returns {Promise<boolean>} A promise that resolves to a boolean indicating if the password is correct.
 */
function checkPassword(password) {
    return fetch('http://127.0.0.1:5000/api/check_passwords', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({passwords: password})
    }).then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    }).catch(error => {
    });
}