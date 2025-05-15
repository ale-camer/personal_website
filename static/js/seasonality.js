//Seasonality Prediction Functionalities

const form = document.getElementById('predictionForm');
form.addEventListener('submit', function (event) {
    event.preventDefault();

    const fileInput = document.getElementById('file');
    const fileError = document.getElementById('fileError');

    fileError.textContent = ''; // Limpia los mensajes de error
    let isValid = true;

    if (!fileInput.files.length) {
        fileError.textContent = 'Please select a file to process.';
        isValid = false;
    } else if (fileInput.files[0].size === 0) {
        fileError.textContent = 'The selected file is empty.';
        isValid = false;
    }

    if (isValid) {
        this.submit();
    }
});

const downloadBtn = document.getElementById('downloadBtn');
downloadBtn.addEventListener('click', function () {
    const fileInput = document.getElementById('file');
    const fileError = document.getElementById('fileError');
    const resultSection = document.getElementById('result-section');

    fileError.textContent = '';

    if (!fileInput.files.length && !resultSection) {
        fileError.textContent = 'Please select a file and process it.';
    } else {
        window.location.href = "{{ url_for('download_predictions') }}";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const resultSection = document.getElementById("result-section");
    if (resultSection) {
        resultSection.scrollIntoView({ behavior: "smooth" });
    }
});