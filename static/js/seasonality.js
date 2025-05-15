//Seasonality Prediction Functionalities

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('predictionForm');
    const fileInput = document.getElementById('file');
    const fileError = document.getElementById('fileError');
    const downloadBtn = document.getElementById('downloadBtn');
    const resultSection = document.getElementById("result-section");

    if (fileInput) {
        fileInput.value = null;
    }

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            if (fileError) fileError.textContent = '';
            let isValid = true;
            if (!fileInput || !fileInput.files.length) {
                if (fileError) fileError.textContent = 'Please select a file.';
                isValid = false;
            } else if (fileInput.files[0].size === 0) {
                if (fileError) fileError.textContent = 'The selected file is empty.';
                isValid = false;
            }
            if (isValid) {
                this.submit();
            }
        });
    }

    if (downloadBtn) {
        downloadBtn.addEventListener('click', function () {
            if (fileError) fileError.textContent = '';
            const hasContentInResults = resultSection && resultSection.innerHTML.trim() !== "";
            if ((!fileInput || !fileInput.files.length) && !hasContentInResults) {
                if (fileError) fileError.textContent = 'Please select a file and calculate predictions first.';
            } else if (!hasContentInResults && (fileInput && fileInput.files.length > 0)){
                if (fileError) fileError.textContent = 'Please calculate prediction before downloading.';
            }
            else {
                window.location.href = "/download_predictions";
            }
        });
    }

    const hasResultsDisplayed = resultSection && resultSection.innerHTML.trim() !== "";

    if (hasResultsDisplayed) {
        if (resultSection) {
            resultSection.scrollIntoView({ behavior: "smooth" });
        }
    }

    if (hasResultsDisplayed && window.history && window.history.replaceState) {
        const cleanUrl = '/seasonality_prediction';
        window.history.replaceState(null, document.title, cleanUrl);
    }
});