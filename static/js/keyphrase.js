// Keyphrase Extraction Functionalities

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file');
    const fileError = document.getElementById('fileError');
    const downloadBtn = document.getElementById('downloadBtn');
    const submitBtn = document.getElementById('submitBtn');
    const resultSection = document.getElementById('result-section');
    const loadingSection = document.getElementById('loading-section');
    const firstSection = document.getElementById('first-container');
    const form = document.getElementById('inputForm');
    const hasResultsDisplayed = resultSection && resultSection.querySelector('table');

    if (submitBtn && form) {
        form.addEventListener('submit', (event) => {
            fileError.textContent = '';
            if (!fileInput.files.length) {
                fileError.textContent = 'Please select a .txt file to upload.';
                event.preventDefault();
                return;
            }

            if (loadingSection) {
                loadingSection.style.display = 'flex';
                loadingSection.style.flexDirection = 'column';
                loadingSection.style.alignItems = 'center';
                firstSection.style.display = 'none';
                if (resultSection) resultSection.style.display = 'none';

                setTimeout(() => {
                    updateProgress();
                }, 100);
            }
        });
    }

    if (downloadBtn) {
        downloadBtn.addEventListener('click', function (event) {
            fileError.textContent = '';
            const hasResultsDisplayed = resultSection && resultSection.querySelector('table');
            let isValid = true;

            if (!hasResultsDisplayed) {
                fileError.textContent = 'Por favor, procesa un archivo primero para poder descargar los resultados.';
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault(); // ¡Esta es la línea clave!
            }
        });
    }

    if (resultSection && resultSection.querySelector('table')) {
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }

    if (hasResultsDisplayed && window.history && window.history.replaceState) {
        const cleanUrl = 'keyphrase_extraction';
        window.history.replaceState(null, document.title, cleanUrl);
        console.log("URL reemplazada en el historial a:", cleanUrl);
    }
});

function updateProgress() {
    const progressBar = document.getElementById('progress-bar');
    const progressPercentage = document.getElementById('progress-percentage');

    if (!progressBar || !progressPercentage) return;

    fetch('/progress')
        .then(response => response.json())
        .then(data => {
            progressBar.style.width = data.value + '%';
            progressPercentage.textContent = data.value + '%';

            if (data.value < 100) {
                setTimeout(updateProgress, 500);
            }
        })
        .catch(error => {
            console.error('Error fetching progress:', error);
            setTimeout(updateProgress, 1000);
        });
}