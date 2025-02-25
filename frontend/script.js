document.addEventListener('DOMContentLoaded', function () {
    const machinesList = document.getElementById('machinesList');
    machinesList.innerHTML = '';
    getMachinesList().then(function (machines) {
        machines.forEach(function (machine) {
            const li = document.createElement('li');
            li.textContent = machine;
            li.addEventListener('click', function () {
                window.open(`machine.html?machine=${machine}`, '_blank');
            });
            machinesList.appendChild(li);
        });
    });
});

document.getElementById('refreshButton').addEventListener('click', function () {
    const machinesList = document.getElementById('machinesList');
    machinesList.innerHTML = '';
    getMachinesList().then(function (machines) {
        machines.forEach(function (machine) {
            const li = document.createElement('li');
            li.textContent = machine;
            machinesList.appendChild(li);
        });
    });
});

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