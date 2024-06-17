// Initialize variables to store selected values and state
let selectedIndicator = null;
let selectedType = null;
let selectedOption = null;
let resultsShown = false;

// Function to handle selection of an indicator
function selectIndicator(key, value) {
    selectedIndicator = value;
    // Update UI elements with selected indicator information
    document.getElementById('dropdownButton').innerText = key;
    document.getElementById('typeButton').innerText = 'Select Type';
    document.getElementById('optionsButton').innerText = 'Select an Option';
    // Fetch options based on selected indicator and type
    fetchOptions();
    // Close the dropdown menu after selection
    closeDropdown('dropdownMenu');
}

// Function to handle selection of a type (country or year)
function selectType(type) {
    selectedType = type;
    // Update UI element with selected type information
    document.getElementById('typeButton').innerText = type === 'country' ? 'Country' : 'Year';
    document.getElementById('optionsButton').innerText = 'Select an Option';
    // Fetch options based on selected indicator and type
    fetchOptions();
    // Close the dropdown menu after selection
    closeDropdown('typeMenu');
}

// Function to fetch options based on selected indicator and type
function fetchOptions() {
    if (selectedIndicator && selectedType) {
        // Make a fetch request to retrieve options based on indicator and type
        fetch(`/fetch_options?indicator=${selectedIndicator}&type=${selectedType}`)
            .then(response => response.json()) // Parse the JSON response
            .then(data => {
                const optionsMenu = document.getElementById('optionsMenu');
                optionsMenu.innerHTML = ''; // Clear existing options
                // Create and append new option elements based on fetched data
                data.forEach(option => {
                    const optionElement = document.createElement('a');
                    optionElement.href = '#';
                    optionElement.innerText = option;
                    optionElement.onclick = () => selectOption(option);
                    optionsMenu.appendChild(optionElement);
                });
            });
    }
}

// Function to handle selection of an option
function selectOption(option) {
    selectedOption = option;
    // Update UI element with selected option information
    document.getElementById('optionsButton').innerText = option;
    // Close the options dropdown menu after selection
    closeDropdown('optionsMenu');
}

// Function to show results after selections are made
function showResults() {
    if (selectedIndicator && selectedType && selectedOption) {
        // If all selections are made, fetch and display results
        fetchData(selectedIndicator, selectedType, selectedOption);
        resultsShown = true; // Mark results as shown
    } else {
        // Alert the user if selections are incomplete
        alert("Please make sure all selections are made before showing results.");
    }
}

// Function to fetch data based on selected indicator, type, and option
function fetchData(indicator, type, option) {
    fetch(`/fetch_data?indicator=${indicator}&type=${type}&option=${option}`)
        .then(response => response.json()) // Parse the JSON response
        .then(data => {
            // Display fetched data in the results table
            displayResults(data);
        });
}

// Function to display results in the results table
function displayResults(data) {
    const resultsTableBody = document.querySelector('.results-container-world-bank .results-table-world-bank-topics tbody');
    resultsTableBody.innerHTML = ''; // Clear existing table rows
    // Iterate through fetched data and populate the table rows
    data.forEach(row => {
        const newRow = resultsTableBody.insertRow();
        newRow.insertCell(0).innerText = row['COUNTRY'];
        newRow.insertCell(1).innerText = row['DATE'];
        // Format and display numeric values with two decimal places
        const value = parseFloat(row['VALUE']);
        const formattedValue = value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        const valueCell = newRow.insertCell(2);
        valueCell.innerText = formattedValue;
        valueCell.classList.add('value-column'); // Add class for right alignment
    });
    const resultsContainer = document.querySelector('.results-container-world-bank');
    resultsContainer.style.display = 'block'; // Show the results container
}

// Function to close a dropdown menu by hiding it
function closeDropdown(menuId) {
    document.getElementById(menuId).style.display = 'none';
}

// Event listener to handle clicks outside dropdowns to close them
document.addEventListener('click', function (event) {
    const dropdownButtons = document.querySelectorAll('.dropbtn-world-bank-topics');
    if (!event.target.matches('.dropbtn-world-bank-topics')) {
        // Close all dropdown menus if clicked outside
        const dropdowns = document.getElementsByClassName('dropdown-content-world-bank-topics');
        for (let i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.style.display === 'block') {
                openDropdown.style.display = 'none';
            }
        }
    } else {
        // Toggle visibility of dropdown content when dropdown button is clicked
        dropdownButtons.forEach(button => {
            if (event.target === button) {
                const dropdownContent = event.target.nextElementSibling;
                dropdownContent.style.display = dropdownContent.style.display === 'none' ? 'block' : 'none';
            }
        });
    }
});

// Function to sort the results table by clicking on table headers
function sortTable(columnIndex, ascending) {
    const rows = document.querySelectorAll('.results-container-world-bank .results-table-world-bank-topics tbody tr');
    const sortedRows = Array.from(rows).sort((a, b) => {
        const aValue = a.cells[columnIndex].innerText;
        const bValue = b.cells[columnIndex].innerText;
        // Convert values to numbers if sorting by 'Value' column
        if (columnIndex === 2) {
            const aNumValue = parseFloat(aValue.replace(/[^0-9.]/g, ''));
            const bNumValue = parseFloat(bValue.replace(/[^0-9.]/g, ''));
            return ascending ? aNumValue - bNumValue : bNumValue - aNumValue;
        }
        // Sort as strings for other columns
        return ascending ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
    });

    // Update table with sorted rows
    const tableBody = document.querySelector('.results-container-world-bank .results-table-world-bank-topics tbody');
    sortedRows.forEach(row => tableBody.appendChild(row));
}

// Event listeners to sort the table when table headers are clicked
document.querySelectorAll('.sortable').forEach(header => {
    let ascending = true; // Variable to control ascending/descending order
    header.addEventListener('click', () => {
        // Toggle sort order icon and class on header
        const icon = header.querySelector('.sort-icon');
        icon.innerHTML = ascending ? '&#8593;' : '&#8595;'; // Unicode for up and down arrows
        ascending = !ascending; // Toggle ascending/descending order
        const columnIndex = Array.from(header.parentNode.children).indexOf(header); // Get column index
        // Remove sort classes from all headers and apply to current header
        document.querySelectorAll('.results-container-world-bank .results-table-world-bank-topics th').forEach(th => th.classList.remove('asc', 'desc'));
        header.classList.toggle('asc', ascending);
        header.classList.toggle('desc', !ascending);
        // Sort table based on clicked header column
        sortTable(columnIndex, ascending);
    });
});

// Function to download CSV file
function downloadCSV() {
    if (!resultsShown) {
        alert("Please show results before downloading CSV.");
        return;
    }
    if (selectedIndicator && selectedType && selectedOption) {
        // If all selections are made, construct download URL and initiate download
        const url = `/download_csv?indicator=${selectedIndicator}&type=${selectedType}&option=${selectedOption}`;
        window.location.href = url;
    } else {
        alert("Please make sure all selections are made.");
    }
}

// Event listener to handle interactive graph generation
document.querySelector('.interactive-graph').addEventListener('click', function () {
    if (!resultsShown) {
        alert("Please show results before viewing the interactive graph.");
        return;
    }
    if (selectedIndicator && selectedType && selectedOption) {
        // If all selections are made, prepare data and make POST request to generate interactive graph
        const indicator = selectedIndicator;
        const type = selectedType === 'country' ? 'country' : 'year';
        const option = selectedOption;
        fetch('/interactive_graph', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `indicator=${encodeURIComponent(indicator)}&type=${encodeURIComponent(type)}&option=${encodeURIComponent(option)}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            console.log('Interactive graph generated.');
        })
        .catch(error => {
            console.error('There was a problem with the interactive graph request:', error);
        });
    } else {
        alert("Please make sure all selections are made.");
    }
});
