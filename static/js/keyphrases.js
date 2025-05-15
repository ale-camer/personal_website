// document.addEventListener('DOMContentLoaded', () => {
//     const fileInput = document.getElementById('file');
//     const fileError = document.getElementById('fileError');
//     const downloadBtn = document.getElementById('downloadBtn');
//     const submitBtn = document.getElementById('submitBtn');
//     const resultSection = document.getElementById('result-section');

//     let extractionDone = window.extractionDone || false;

//     if (submitBtn) {
//         submitBtn.addEventListener('click', (event) => {
//             fileError.textContent = '';
//             if (!fileInput.files.length) {
//                 fileError.textContent = 'ERROR 1';
//                 event.preventDefault();
//                 extractionDone = false;
//             } else {
//                 extractionDone = true; // <-- Marca que se hizo extracción (asumido exitoso)
//             }
//         });
//     }

//     if (downloadBtn) {
//         downloadBtn.addEventListener('click', function (event) {
//             fileError.textContent = '';

//             if (!fileInput.files.length) {
//                 fileError.textContent = 'ERROR 2';
//             } else if (!extractionDone) {
//                 fileError.textContent = 'ERROR 3';
//             } else {
//                 window.location.href = "/download_keyphrases";
//             }
//         });
//     }

//     if (resultSection && resultSection.textContent.trim().length > 0) {
//         resultSection.scrollIntoView({ behavior: 'smooth' });
//     }
// });

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file');
    const fileError = document.getElementById('fileError');
    const downloadBtn = document.getElementById('downloadBtn');
    const submitBtn = document.getElementById('submitBtn');
    const resultSection = document.getElementById('result-section'); // El div que contiene los resultados

    if (submitBtn) {
        submitBtn.addEventListener('click', (event) => {
            fileError.textContent = ''; // Limpiar errores
            if (!fileInput.files.length) {
                fileError.textContent = 'ERROR 1: Please select a .txt file to upload.';
                event.preventDefault(); // Prevenir el envío del formulario si no hay archivo
            }
        });
    }

    if (downloadBtn) {
        downloadBtn.addEventListener('click', function (event) {
            fileError.textContent = ''; // Limpiar errores

            const hasResultsDisplayed = resultSection && resultSection.querySelector('table');
            if (!fileInput.files.length && !hasResultsDisplayed) {
                fileError.textContent = 'ERROR 2: Please upload a file and extract keyphrases first.';
            } else if (!hasResultsDisplayed) {
                fileError.textContent = 'ERROR 3: Please extract keyphrases first to see results.';
            } else {
                console.log("Download button clicked. Results are displayed. Attempting to navigate to /download_keyphrases");
                window.location.href = "/download_keyphrases";
            }
        });
    }

    if (resultSection && resultSection.querySelector('table')) {
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
});