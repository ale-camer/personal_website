let fetchedData = [];
let filterType = '';
let filteredData = [];

document.addEventListener('DOMContentLoaded', () => {
    populateIndicators();
});

function populateIndicators() {
    fetch('/get_indicators')
        .then(response => response.json())
        .then(indicators => {
            const dropdownMenu = document.getElementById('dropdownMenu');
            indicators.forEach(indicator => {
                const option = document.createElement('a');
                option.href = '#';
                option.innerText = indicator;
                option.onclick = () => selectIndicator(indicator);
                dropdownMenu.appendChild(option);
            });
        });
}

function selectIndicator(indicator) {
    document.getElementById('dropdownButton').innerText = indicator;
    fetchData(indicator);
}

function fetchData(indicator) {
    fetch(`/fetch_data?indicator=${indicator}`)
        .then(response => response.json())
        .then(data => {
            fetchedData = data;
            showFilterTypeContainer();
        });
}

function showFilterTypeContainer() {
    document.getElementById('filterTypeContainer').style.display = 'block';
}

function showFilterValues() {
    filterType = document.getElementById('filterType').value;
    const filterValuesContainer = document.getElementById('filterValuesContainer');
    const filterValues = document.getElementById('filterValues');
    const filterValuesLabel = document.getElementById('filterValuesLabel');

    if (filterType === 'country') {
        filterValuesLabel.innerText = 'Select a country:';
        const countries = [...new Set(fetchedData.map(row => row.country))];
        filterValues.innerHTML = countries.map(country => `<option value="${country}">${country}</option>`).join('');
    } else if (filterType === 'year') {
        filterValuesLabel.innerText = 'Select a year:';
        const years = [...new Set(fetchedData.map(row => row.date.split('-')[0]))];
        filterValues.innerHTML = years.map(year => `<option value="${year}">${year}</option>`).join('');
    }

    filterValuesContainer.style.display = 'block';
    document.getElementById('showResultsButton').style.display = 'block';
}

function showFilteredResults() {
    const filterValue = document.getElementById('filterValues').value;

    if (filterType === 'country') {
        filteredData = fetchedData.filter(row => row.country === filterValue);
    } else if (filterType === 'year') {
        filteredData = fetchedData.filter(row => row.date.startsWith(filterValue));
    }

    displayResults(filteredData);
}

function displayResults(data) {
    const resultsTableBody = document.querySelector('.results-container-world-bank .results-table-world-bank-topics tbody');
    resultsTableBody.innerHTML = '';

    data.forEach(row => {
        const newRow = resultsTableBody.insertRow();
        newRow.insertCell(0).innerText = row.country;
        newRow.insertCell(1).innerText = row.date;
        newRow.insertCell(2).innerText = row.value;
    });

    document.querySelector('.results-container-world-bank').style.display = 'block';
}

function downloadCSV() {
    const indicator = document.getElementById('dropdownButton').innerText;
    window.location.href = `/download_csv?indicator=${indicator}`;
}
