document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const password = document.getElementById('password').value;

    checkPassword(password).then(response => {
        if (response) {
            localStorage.setItem('isLoggedIn', 'true');
            window.location.href = 'index.html';
        } else {
            alert('Wrong password!');
        }
    });
});

function checkPassword(password) {
    return fetch('http://127.0.0.1:5000/api/check_passwords', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ passwords: password })
    }).then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
