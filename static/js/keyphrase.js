//Keyphrase Extraction Functionalities

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file');
    const fileError = document.getElementById('fileError');
    const downloadBtn = document.getElementById('downloadBtn');
    const submitBtn = document.getElementById('submitBtn');
    const resultSection = document.getElementById('result-section');
    const hasResultsDisplayed = resultSection && resultSection.querySelector('table');

    if (submitBtn) {
        submitBtn.addEventListener('click', (event) => {
            fileError.textContent = '';
            if (!fileInput.files.length) {
                fileError.textContent = 'Please select a .txt file to upload.';
                event.preventDefault();
            }
        });
    }

    if (downloadBtn) {
        downloadBtn.addEventListener('click', function (event) {
            fileError.textContent = '';

            const hasResultsDisplayed = resultSection && resultSection.querySelector('table');
            if (!fileInput.files.length && !hasResultsDisplayed) {
                fileError.textContent = 'Please upload a .txt file and extract keyphrases first.';
            } else if (!hasResultsDisplayed) {
                fileError.textContent = 'Please extract keyphrases first to see results and later download them.';
            } else {
                window.location.href = "/download_keyphrases";
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