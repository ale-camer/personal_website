//World Bank Functionalities

let selectedIndicator = null;
let selectedIndicatorKey = null;
let selectedType = null;
let selectedTypeKey = null;
let selectedOptionValue = null;
let currentTableData = [];

function closeDropdown(menuId) {
    const menu = document.getElementById(menuId);
    if (menu) {
        menu.style.display = 'none';
    }
}

function selectIndicator(event, key, value) {
    event.preventDefault();
    if (selectedIndicator !== value) {
        selectedIndicator = value;
        selectedIndicatorKey = key;
        document.getElementById('dropdownButton').innerText = key;
        selectedOptionValue = null;
        document.getElementById('optionsButton').innerText = 'Country/Year';
        const optionsMenu = document.getElementById('optionsMenu');
        if (optionsMenu) {
            optionsMenu.innerHTML = selectedType ? '<a href="#" class="options-message">Loading options...</a>' : '<a href="#" class="options-message">Select type to see options...</a>';
        }
        document.getElementById('wb-results').style.display = 'none';
        document.getElementById('wb_tbody').innerHTML = '';
        currentTableData = [];
        checkAndLoadOptions();
    }
    closeDropdown('dropdownMenu');
}

function selectType(event, type) {
    event.preventDefault();
    if (selectedType !== type) {
        selectedType = type;
        selectedTypeKey = type.charAt(0).toUpperCase() + type.slice(1);
        document.getElementById('typeButton').innerText = selectedTypeKey;
        selectedOptionValue = null;
        document.getElementById('optionsButton').innerText = 'Country/Year';
        const optionsMenu = document.getElementById('optionsMenu');
        if (optionsMenu) {
            optionsMenu.innerHTML = selectedIndicator ? '<a href="#" class="options-message">Loading options...</a>' : '<a href="#" class="options-message">Select indicator to see options...</a>';
        }
        document.getElementById('wb-results').style.display = 'none';
        document.getElementById('wb_tbody').innerHTML = '';
        currentTableData = [];
        checkAndLoadOptions();
    }
    closeDropdown('typeMenu');
}

function selectOption(event, optionValue, optionText) {
    event.preventDefault();
    document.getElementById('optionsButton').innerText = optionText;
    selectedOptionValue = optionValue;
    closeDropdown('optionsMenu');
    console.log("Selected option value:", selectedOptionValue, "Display text:", optionText);
    document.getElementById('wb-results').style.display = 'none';
    document.getElementById('wb_tbody').innerHTML = '';
    currentTableData = [];
}

function checkAndLoadOptions() {
    const optionsMenu = document.getElementById('optionsMenu');
    const optionsButton = document.getElementById('optionsButton');
    if (!optionsMenu || !optionsButton) return;

    if (!selectedIndicator || !selectedType) {
        let message = "First choose an indicator and type.";
        if (!selectedIndicator && !selectedType) message = "First choose an indicator and type.";
        else if (!selectedIndicator) message = "First choose an indicator.";
        else message = "First choose a type.";
        optionsButton.innerText = 'Country/Year';
        optionsMenu.innerHTML = `<a href="#" class="options-message">${message}</a>`;
        return;
    }

    optionsMenu.innerHTML = '<a href="#" class="options-message">Loading options...</a>';

    fetch(`/download_data?indicator=${encodeURIComponent(selectedIndicator)}&type=${encodeURIComponent(selectedType)}`)
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`Save data failed: ${response.status} ${response.statusText}. ${text}`);
                });
            }
            return;
        })
        .then(() => {
            return fetch(`/show_options?indicator=${encodeURIComponent(selectedIndicator)}&type=${encodeURIComponent(selectedType)}`);
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errData => {
                    throw new Error(`Fetch options failed: ${response.status}. ${errData.message || 'Server error'}`);
                }).catch(() => {
                    throw new Error(`Fetch options failed: ${response.status} ${response.statusText}`);
                });
            }
            return response.json();
        })
        .then(data => {
            optionsMenu.innerHTML = '';
            if (data && data.length > 0) {
                data.forEach(option => {
                    const optionElement = document.createElement('a');
                    optionElement.href = '#';
                    let optionValue, optionText;
                    if (typeof option === 'object' && option !== null && option.hasOwnProperty('value') && option.hasOwnProperty('text')) {
                        optionValue = option.value;
                        optionText = option.text;
                    } else {
                        optionValue = option;
                        optionText = option;
                    }
                    // optionElement.innerText = optionText;
                    optionElement.classList.add('dropdown-item', 'd-block', 'text-center', 'fs-6');
                    optionElement.innerText = optionText;
                    optionElement.onclick = (e) => selectOption(e, optionValue, optionText);
                    optionsMenu.appendChild(optionElement);
                });
            } else {
                optionsMenu.innerHTML = '<a href="#" class="options-message">No options available.</a>';
            }
        })
        .catch(error => {
            console.error('Error in checkAndLoadOptions:', error);
            optionsMenu.innerHTML = `<a href="#" class="options-message">Error: ${error.message}. Try again.</a>`;
        });
}

function populateTable(data) {
    const tableBody = document.getElementById('wb_tbody');
    if (!tableBody) {
        console.error("Table body 'wb_tbody' not found!");
        return;
    }
    tableBody.innerHTML = '';

    if (!data || data.length === 0) {
        const row = tableBody.insertRow();
        const cell = row.insertCell();
        cell.colSpan = 3;
        cell.textContent = 'No data available for the selected criteria.';
        cell.style.textAlign = 'center';
        return;
    }

    data.forEach(item => {
        const newRow = tableBody.insertRow();
        newRow.insertCell(0).innerText = item['COUNTRY'] || 'N/A';
        newRow.insertCell(1).innerText = item['DATE'] || 'N/A';

        const value = parseFloat(item['VALUE']);
        const valueCell = newRow.insertCell(2);
        if (!isNaN(value)) {
            valueCell.innerText = value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        } else {
            valueCell.innerText = item['VALUE'] || 'N/A';
        }
        valueCell.classList.add('value-column');
    });
}

async function fetchAndShowResults() {
    if (!selectedIndicator || !selectedType || !selectedOptionValue) {
        alert('Please make sure all selections are made before showing results.');
        return;
    }

    const resultsDiv = document.getElementById('wb-results');
    const tableBody = document.getElementById('wb_tbody');

    tableBody.innerHTML = '';
    const loadingRow = tableBody.insertRow();
    const loadingCell = loadingRow.insertCell();
    loadingCell.colSpan = 3;
    loadingCell.textContent = 'Loading data...';
    loadingCell.style.textAlign = 'center';

    resultsDiv.style.display = 'block';

    try {
        const response = await fetch(`/show_data?indicator=${encodeURIComponent(selectedIndicator)}&type=${encodeURIComponent(selectedType)}&option=${encodeURIComponent(selectedOptionValue)}`);

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Network response was not ok (${response.status}): ${errorText || response.statusText}`);
        }

        const data = await response.json();
        currentTableData = data;
        populateTable(data);

        resultsDiv.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });

    } catch (error) {
        console.error('Error fetching or processing results:', error);
        tableBody.innerHTML = '';
        const errorRow = tableBody.insertRow();
        const errorCell = errorRow.insertCell();
        errorCell.colSpan = 3;
        errorCell.textContent = `Error loading data: ${error.message}`;
        errorCell.style.textAlign = 'center';
        errorCell.style.color = 'red';
    }
}

function makeTableSortable() {
    const table = document.querySelector('.wb-table');
    if (!table) return;
    const headers = table.querySelectorAll('th.sortable');
    let sortStates = {};

    headers.forEach(header => {
        const dataKey = header.getAttribute('data-translate-key').toUpperCase();
        
        if (!dataKey) {
            console.warn(`Header sin el atributo data-translate-key requerido.`);
            return;
        }

        header.addEventListener('click', () => {
            if (currentTableData.length === 0) return;

            const currentDirection = sortStates[dataKey] || 'none';
            let newDirection;
            if (currentDirection === 'asc') newDirection = 'desc';
            else newDirection = 'asc';

            Object.keys(sortStates).forEach(key => sortStates[key] = 'none');
            headers.forEach(h => {
                h.classList.remove('asc', 'desc');
                const icon = h.querySelector('.sort-icon');
                if (icon) icon.innerHTML = '↕';
            });

            sortStates[dataKey] = newDirection;
            header.classList.add(newDirection);
            const icon = header.querySelector('.sort-icon');
            if (icon) icon.innerHTML = newDirection === 'asc' ? '↑' : '↓';

            currentTableData.sort((a, b) => {
                let valA = a[dataKey];
                let valB = b[dataKey];

                if (dataKey === 'VALUE') {
                    valA = parseFloat(String(valA).replace(/,/g, ''));
                    valB = parseFloat(String(valB).replace(/,/g, ''));
                    if (isNaN(valA)) valA = newDirection === 'asc' ? Infinity : -Infinity;
                    if (isNaN(valB)) valB = newDirection === 'asc' ? Infinity : -Infinity;
                } else if (dataKey === 'DATE') {
                    const numA = parseFloat(valA);
                    const numB = parseFloat(valB);
                    if (!isNaN(numA) && !isNaN(numB)) {
                        valA = numA;
                        valB = numB;
                    } else {
                        valA = String(valA).toLowerCase();
                        valB = String(valB).toLowerCase();
                    }
                } else {
                    valA = String(valA).toLowerCase();
                    valB = String(valB).toLowerCase();
                }

                if (valA < valB) return newDirection === 'asc' ? -1 : 1;
                if (valA > valB) return newDirection === 'asc' ? 1 : -1;
                return 0;
            });
            populateTable(currentTableData);
        });
    });
}

function downloadDataAsCSV() {
    if (!currentTableData || currentTableData.length === 0) {
        alert("No data available to download. Please 'Show Results' first.");
        return;
    }

    const headers = ["Country", "Date", "Value"];
    const dataKeys = ["COUNTRY", "DATE", "VALUE"];
    let csvContent = "data:text/csv;charset=utf-8," + headers.join(",") + "\n";

    currentTableData.forEach(item => {
        const row = dataKeys.map(key => {
            let cellData = item[key];
            if (typeof cellData === 'string' && (cellData.includes(',') || cellData.includes('"') || cellData.includes('\n'))) {
                cellData = `"${cellData.replace(/"/g, '""')}"`;
            }
            if (key === 'VALUE') {
                const numericValue = parseFloat(item['VALUE']);
                cellData = !isNaN(numericValue) ? numericValue.toString() : (item['VALUE'] || '');
            }
            return cellData;
        });
        csvContent += row.join(",") + "\n";
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    const indicatorName = selectedIndicatorKey ? selectedIndicatorKey.replace(/[^a-z0-9]/gi, '_').toLowerCase() : 'data';
    const optionName = selectedOptionValue ? String(selectedOptionValue).replace(/[^a-z0-9]/gi, '_').toLowerCase() : 'all';
    const typeName = selectedTypeKey ? selectedTypeKey.toLowerCase() : 'selection';
    const fileName = `world_bank_${indicatorName}_${typeName}_${optionName}.csv`;
    link.setAttribute("download", fileName);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

async function showInteractiveGraph() {
    if (!selectedIndicator || !selectedType || !selectedOptionValue) {
        alert('Please make sure all selections are made before requesting the graph.');
        return;
    }

    const interactiveGraphBtn = document.getElementById('interactiveGraphBtn');
    const originalButtonText = interactiveGraphBtn?.innerHTML;

    if (interactiveGraphBtn) {
        interactiveGraphBtn.innerHTML = 'Generating...';
        interactiveGraphBtn.disabled = true;
    }

    const formData = new FormData();
    formData.append('indicator', selectedIndicator);
    formData.append('type', selectedType);
    formData.append('option', selectedOptionValue);

    try {
        const response = await fetch('/plot_graph', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Graph generation request failed (${response.status}): ${errorText || response.statusText}`);
        }

        const data = await response.json();
        console.log('Server response for graph:', data);

        if (data.plot_url) {
            window.open(data.plot_url, '_blank');
            alert(data.message + "\n\nThe graph should open in a new tab. If not, please check your browser's pop-up blocker.");
        } else {
            alert(data.message || "Graph generated, but no URL provided to open.");
        }

    } catch (error) {
        console.error('Error requesting interactive graph:', error);
        alert(`Error: ${error.message}`);
    } finally {
        if (interactiveGraphBtn && originalButtonText) {
            interactiveGraphBtn.innerHTML = originalButtonText;
            interactiveGraphBtn.disabled = false;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.wb-topics').forEach(topicsDiv => {
        const contentElement = topicsDiv.querySelector('.wb-content');
        if (contentElement) {
            topicsDiv.addEventListener('mouseleave', function () {
                contentElement.style.removeProperty('display');
            });
        }
    });

    checkAndLoadOptions();

    const showResultsButton = document.querySelector('.upload-form button[type="submit"]');
    if (showResultsButton) {
        showResultsButton.addEventListener('click', function (event) {
            event.preventDefault();
            fetchAndShowResults();
        });
    } else {
        console.warn('Show Results button not found.');
    }

    const downloadCSVButton = document.getElementById('downloadCSVBtn');
    if (downloadCSVButton) {
        downloadCSVButton.addEventListener('click', function (event) {
            event.preventDefault();
            downloadDataAsCSV();
        });
    } else {
        console.warn('Download CSV button (id="downloadCSVBtn") not found.');
    }

    const interactiveGraphButton = document.getElementById('interactiveGraphBtn');
    if (interactiveGraphButton) {
        interactiveGraphButton.addEventListener('click', function (event) {
            event.preventDefault();
            showInteractiveGraph();
        });
    } else {
        console.warn('Interactive Graph button (id="interactiveGraphBtn") not found.');
    }

    makeTableSortable();
});