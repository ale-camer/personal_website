const LANGUAGES_DATA = [
    { value: "english", text: "English" },
    { value: "mandarin", text: "Mandarin" },
    { value: "spanish", text: "Spanish" },
    { value: "french", text: "French" },
    { value: "arabic", text: "Arabic" },
    { value: "bengali", text: "Bengali" },
    { value: "portuguese", text: "Portuguese" },
    { value: "russian", text: "Russian" },
    { value: "japanese", text: "Japanese" },
    { value: "punjabi", text: "Punjabi" },
    { value: "german", text: "German" },
    { value: "javanese", text: "Javanese" },
    { value: "korean", text: "Korean" },
    { value: "vietnamese", text: "Vietnamese" },
    { value: "telugu", text: "Telugu" }
];
const DEFAULT_LANGUAGE = "english";

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
    setupLanguageSelection('language', 'selected_language', LANGUAGES_DATA, DEFAULT_LANGUAGE);
    setupFormValidation('form.project-form', 'file', 'fileError');
});