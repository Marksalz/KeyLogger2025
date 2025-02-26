document.addEventListener('DOMContentLoaded', function () {
    if (localStorage.getItem('isLoggedIn') !== 'true') {
        window.location.href = 'login.html';
    }

    loadMachinesList();

    // Update clock every second
    setInterval(updateClock, 1000);
    updateClock();

    // Profile button click event
    document.getElementById('profileButton').addEventListener('click', function () {
        alert('Profile button clicked!');
    });

    // Logout button click event
    document.getElementById('logoutButton').addEventListener('click', function () {
        localStorage.removeItem('isLoggedIn');
        window.location.href = 'login.html';
    });

    // Refresh button click event
    document.getElementById('refreshButton').addEventListener('click', function () {
        loadMachinesList();
    });
});

function loadMachinesList() {
    const machinesList = document.getElementById('machinesList');
    machinesList.innerHTML = '';
    getMachinesList().then(function (machines) {
        machines.forEach(function (machine) {
            const row = document.createElement('tr');
            const machineCell = document.createElement('td');
            machineCell.textContent = machine;
            const actionsCell = document.createElement('td');
            const viewButton = document.createElement('button');
            viewButton.textContent = 'View Logs';
            viewButton.className = 'btn btn-info';
            viewButton.addEventListener('click', function () {
                window.open(`machine.html?machine=${machine}`, '_blank');
            });
            actionsCell.appendChild(viewButton);
            row.appendChild(machineCell);
            row.appendChild(actionsCell);
            machinesList.appendChild(row);
        });
    });
}

function getMachinesList() {
    return fetch('http://127.0.0.1:5000/api/get_target_machines_list')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            return data.machines;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const timeString = `${hours}:${minutes}:${seconds}`;
    document.getElementById('clock').textContent = timeString;
}

function loadHostagesTicker() {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "https://bringthemhomenow.net/1.1.0/hostages-ticker.js";
    script.setAttribute(
        "integrity",
        "sha384-DHuakkmS4DXvIW79Ttuqjvl95NepBRwfVGx6bmqBJVVwqsosq8hROrydHItKdsne"
    );
    script.setAttribute("crossorigin", "anonymous");
    document.head.appendChild(script);
}

document.addEventListener("DOMContentLoaded", loadHostagesTicker);
