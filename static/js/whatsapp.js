//WhatsApp Functionalities

let LANGUAGES_DATA = [];
const DEFAULT_LANGUAGE = "english";
const JSONfilePath = 'static/json/stopwords.json';

fetch(JSONfilePath)
    .then(response => response.json())
    .then(data => {
        LANGUAGES_DATA = Object.keys(data).map(key => ({
            value: key,
            text: capitalizeFirstLetter(key)
        }));

        setupLanguageSelection('language', 'selected_language', LANGUAGES_DATA, DEFAULT_LANGUAGE);
    })
    .catch(error => {
        console.error('Error al cargar los idiomas:', error);
    });

function setupLanguageSelection(selectId, hiddenInputId, languages, defaultLang) {
    const selectElement = document.getElementById(selectId);
    const hiddenInputElement = document.getElementById(hiddenInputId);

    if (!selectElement || !hiddenInputElement) {
        console.error(`Error: Language select ('${selectId}') or hidden input ('${hiddenInputId}') element not found.`);
        return;
    }

    selectElement.innerHTML = '';

    languages.forEach(function (language) {
        const option = document.createElement('option');
        option.value = language.value;
        option.textContent = language.text;
        selectElement.appendChild(option);
    });

    if (languages.some(lang => lang.value === defaultLang)) {
        selectElement.value = defaultLang;
    } else if (languages.length > 0) {
        selectElement.value = languages[0].value;
    }
    hiddenInputElement.value = selectElement.value;

    selectElement.addEventListener('change', function () {
        hiddenInputElement.value = this.value;
    });
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function setupFormValidation(formSelector, fileInputId, fileErrorId) {
    const formElement = document.querySelector(formSelector);
    const fileInputElement = document.getElementById(fileInputId);
    const fileErrorElement = document.getElementById(fileErrorId);

    if (!formElement) {
        console.error(`Error: Form element with selector ('${formSelector}') not found.`);
        return;
    }
    if (!fileInputElement) {
        console.error(`Error: File input element with ID ('${fileInputId}') not found.`);
        return;
    }
    if (!fileErrorElement) {
        console.error(`Error: File error element with ID ('${fileErrorId}') not found.`);
        return;
    }

    formElement.addEventListener('submit', function (event) {
        event.preventDefault();

        fileErrorElement.textContent = '';
        let isValid = true;

        if (!fileInputElement.files || fileInputElement.files.length === 0) {
            fileErrorElement.textContent = 'Please select a file to upload.';
            isValid = false;
        }

        if (isValid) {
            this.submit();
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    setupFormValidation('form.project-form', 'file', 'fileError');
});