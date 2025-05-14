// const form = document.getElementById('inputForm');
// form.addEventListener('submit', function (event) {
//     event.preventDefault();

//     const fileInput = document.getElementById('file');
//     const fileError = document.getElementById('fileError');

//     fileError.textContent = '';
//     let isValid = true;

//     if (!fileInput.files.length) {
//         fileError.textContent = 'Please select a file.';
//         isValid = false;
//     }

//     if (isValid) {
//         this.submit();
//     }
// });

// const downloadBtn = document.getElementById('downloadBtn');
// const resultSection = document.getElementById('result-section');
// downloadBtn.addEventListener('click', function () {
//     const fileInput = document.getElementById('file');
//     const fileError = document.getElementById('fileError');
//     // console.log(resultSection.textContent);
//     console.log(resultSection.textContent.length);
//     console.log(!resultSection.textContent.length);
    

//     fileError.textContent = '';

//     if (!fileInput.files.length) {
//         fileError.textContent = 'Please select a file first.';
//     } else {
//         window.location.href = "{{ url_for('download_keyphrases') }}";
//     }
// });

// document.addEventListener("DOMContentLoaded", function () {
//     const resultSection = document.getElementById("result-section");
//     if (resultSection) {
//         resultSection.scrollIntoView({ behavior: "smooth" });
//     }
// });

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file');
    const fileError = document.getElementById('fileError');
    const downloadBtn = document.getElementById('downloadBtn');
    const submitBtn = document.getElementById('submitBtn');
    const resultSection = document.getElementById('result-section');

    // Para el botón de envío (Extract)
    if (submitBtn) {
        submitBtn.addEventListener('click', (event) => {
            fileError.textContent = '';
            if (!fileInput.files.length) {
                fileError.textContent = 'ERROR 1';
                event.preventDefault();
            }
        });
    }

    // Para el botón de descarga
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function () {
            fileError.textContent = '';

            if (!resultSection || resultSection.textContent.trim().length === 0) {
                // Si resultSection NO existe O si existe PERO su contenido (sin espacios en blanco) está vacío
                fileError.textContent = 'ERROR 2';
            } else {
                // Si hay archivo seleccionado Y resultSection existe y tiene contenido
                window.location.href = "{{ url_for('download_keyphrases') }}";
            }
        });
    }

    if (resultSection && resultSection.textContent.trim().length > 0) {
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
});