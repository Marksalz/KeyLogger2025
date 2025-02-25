document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const password = document.getElementById('password').value;

    getPasswords().then(passwords => {
        if (Object.values(passwords).includes(password)) {
            window.location.href = 'index.html';
        } else {
            alert('Incorrect password. Please try again.');
        }
    }).catch(error => {
        console.error('Error fetching passwords:', error);
        alert('An error occurred. Please try again later.');
    });

    function getPasswords() {
        return fetch('http://127.0.0.1:5000/api/get_passwords')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    }
});