let selectedIndicator = null;
let selectedType = null;
let selectedOption = null;
let resultsShown = false;

function selectIndicator(key, value) {
    selectedIndicator = value;
    document.getElementById('dropdownButton').innerText = key;
    document.getElementById('typeButton').innerText = 'Select Type';
    document.getElementById('optionsButton').innerText = 'Select an Option';
    fetchOptions();
    closeDropdown('dropdownMenu');
}

function selectType(type) {
    selectedType = type;
    document.getElementById('typeButton').innerText = type === 'country' ? 'Country' : 'Year';
    document.getElementById('optionsButton').innerText = 'Select an Option';
    fetchOptions();
    closeDropdown('typeMenu');
}

function fetchOptions() {
    if (selectedIndicator && selectedType) {
        fetch(`/fetch_options?indicator=${selectedIndicator}&type=${selectedType}`)
            .then(response => response.json())
            .then(data => {
                const optionsMenu = document.getElementById('optionsMenu');
                optionsMenu.innerHTML = '';
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

function selectOption(option) {
    selectedOption = option;
    document.getElementById('optionsButton').innerText = option;
    closeDropdown('optionsMenu');
}

// Función para mostrar los resultados y guardar el archivo CSV
function showResults() {
    if (selectedIndicator && selectedType && selectedOption) {
        fetchData(selectedIndicator, selectedType, selectedOption);
        resultsShown = true;
    } else {
        alert("Please make sure all selections are made before showing results.");
    }
}


function fetchData(indicator, type, option) {
    fetch(`/fetch_data?indicator=${indicator}&type=${type}&option=${option}`)
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        });
}

function displayResults(data) {
    const resultsTableBody = document.querySelector('.results-container-world-bank .results-table-world-bank-topics tbody');
    resultsTableBody.innerHTML = '';
    data.forEach(row => {
        const newRow = resultsTableBody.insertRow();
        newRow.insertCell(0).innerText = row['COUNTRY'];
        newRow.insertCell(1).innerText = row['DATE'];
        // Convertir a número y luego formatear el valor con separadores de miles y dos decimales
        const value = parseFloat(row['VALUE']);
        const formattedValue = value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        const valueCell = newRow.insertCell(2);
        valueCell.innerText = formattedValue;
        valueCell.classList.add('value-column');  // Agregar clase para alinear a la derecha
    });
    const resultsContainer = document.querySelector('.results-container-world-bank');
    resultsContainer.style.display = 'block';
}



function closeDropdown(menuId) {
    document.getElementById(menuId).style.display = 'none';
}

document.addEventListener('click', function (event) {
    const dropdownButtons = document.querySelectorAll('.dropbtn-world-bank-topics');
    if (!event.target.matches('.dropbtn-world-bank-topics')) {
        const dropdowns = document.getElementsByClassName('dropdown-content-world-bank-topics');
        for (let i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.style.display === 'block') {
                openDropdown.style.display = 'none';
            }
        }
    }
    // Agrega este bloque para abrir nuevamente los menús desplegables
    else {
        dropdownButtons.forEach(button => {
            if (event.target === button) {
                const dropdownContent = event.target.nextElementSibling;
                if (dropdownContent.style.display === 'none') {
                    dropdownContent.style.display = 'block';
                } else {
                    dropdownContent.style.display = 'none';
                }
            }
        });
    }
});

// Función para ordenar la tabla
function sortTable(columnIndex, ascending) {
    const sortedData = [...currentData].sort((a, b) => {
        let aValue = Object.values(a)[columnIndex];
        let bValue = Object.values(b)[columnIndex];

        if (columnIndex === 2) { // Si es la columna de valores, comparar como números
            aValue = parseFloat(aValue);
            bValue = parseFloat(bValue);
        }

        if (aValue < bValue) return ascending ? -1 : 1;
        if (aValue > bValue) return ascending ? 1 : -1;
        return 0;
    });
    displayResults(sortedData);
}

// Agregar manejadores de eventos para los encabezados de la tabla
document.querySelectorAll('.results-table-world-bank-topics th').forEach((header, index) => {
    header.addEventListener('click', () => {
        const ascending = !header.classList.contains('asc');
        document.querySelectorAll('.results-table-world-bank-topics th').forEach(th => th.classList.remove('asc', 'desc'));
        header.classList.toggle('asc', ascending);
        header.classList.toggle('desc', !ascending);
        sortTable(index, ascending);
    });
});

// Función para ordenar la tabla
function sortTable(columnIndex, ascending) {
    const rows = document.querySelectorAll('.results-container-world-bank .results-table-world-bank-topics tbody tr');
    const sortedRows = Array.from(rows).sort((a, b) => {
        const aValue = a.cells[columnIndex].innerText;
        const bValue = b.cells[columnIndex].innerText;

        // Convertir los valores a números solo si es la columna 'Value'
        if (columnIndex === 2) {
            const aNumValue = parseFloat(aValue.replace(/[^0-9.]/g, '')); // Elimina todos los caracteres que no sean dígitos o puntos
            const bNumValue = parseFloat(bValue.replace(/[^0-9.]/g, ''));

            return ascending ? aNumValue - bNumValue : bNumValue - aNumValue; // Ordenar como números
        }

        // Si no es la columna 'Value', ordenar como cadenas
        return ascending ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
    });

    const tableBody = document.querySelector('.results-container-world-bank .results-table-world-bank-topics tbody');
    sortedRows.forEach(row => tableBody.appendChild(row));
}


// Agregar manejadores de eventos para los encabezados de la tabla
document.querySelectorAll('.sortable').forEach(header => {
    let ascending = true; // Variable para controlar el orden ascendente/descendente

    header.addEventListener('click', () => {
        const icon = header.querySelector('.sort-icon');
        if (ascending) {
            icon.innerHTML = '&#8593;'; // Unicode para flecha hacia arriba
        } else {
            icon.innerHTML = '&#8595;'; // Unicode para flecha hacia abajo
        }

        ascending = !ascending; // Cambia el estado de la variable para el próximo clic
        const columnIndex = Array.from(header.parentNode.children).indexOf(header); // Obtiene el índice de la columna

        // Remueve las clases de ordenamiento de todos los encabezados
        document.querySelectorAll('.results-container-world-bank .results-table-world-bank-topics th').forEach(th => th.classList.remove('asc', 'desc'));
        header.classList.toggle('asc', ascending);
        header.classList.toggle('desc', !ascending);

        sortTable(columnIndex, ascending);
    });
});

// Función para descargar el CSV
function downloadCSV() {
    if (!resultsShown) {
        alert("Please show results before downloading CSV.");
        return;
    }
    if (selectedIndicator && selectedType && selectedOption) {
        const url = `/download_csv?indicator=${selectedIndicator}&type=${selectedType}&option=${selectedOption}`;
        window.location.href = url;
    } else {
        alert("Please make sure all selections are made.");
    }
}

document.querySelector('.interactive-graph').addEventListener('click', function () {
    if (!resultsShown) {
        alert("Please show results before viewing the interactive graph.");
        return;
    }
    if (selectedIndicator && selectedType && selectedOption) {
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