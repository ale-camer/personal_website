document.addEventListener('DOMContentLoaded', function () {
    const languageSelector = document.getElementById('select-language');
    const langJsonBaseUrl = "/static/json/lang/";
    const availableLanguages = ['english', 'spanish', 'french', 'german', 'italian', 'portuguese', 'russian', 'japanese', 'korean', 'arabic', 'dutch', 'swedish', 'danish', 'finnish'];

    function getPageKey() {
        const pathname = window.location.pathname;
        if (pathname === '/' || pathname.endsWith('/index.html') || pathname.endsWith('/')) {
            return 'home';
        }
        const pageName = pathname.split('/').pop().replace('.html', '');
        return pageName === '' ? 'home' : pageName;
    }
    const pageKey = getPageKey();

    function getCurrentLang() {
        const urlLang = new URLSearchParams(window.location.search).get('lang');
        if (urlLang && availableLanguages.includes(urlLang)) {
            localStorage.setItem('preferredLang', urlLang);
            return urlLang;
        }
        const storedLang = localStorage.getItem('preferredLang');
        if (storedLang && availableLanguages.includes(storedLang)) {
            return storedLang;
        }
        const flaskLang = 'spanish';
        return availableLanguages.includes(flaskLang) ? flaskLang : 'spanish';
    }

    async function loadAndApplyTranslations(lang) {
        try {
            const response = await fetch(`${langJsonBaseUrl}${lang}.json`);
            const allTranslations = await response.json();

            if (allTranslations['projects-description']) {
                window.projectTranslations = allTranslations['projects-description'];
            }

            const commonTranslations = allTranslations['common'] || {};
            const pageTranslations = allTranslations[pageKey] || {};
            const finalTranslations = { ...commonTranslations, ...pageTranslations };
            applyPageTranslations(finalTranslations);
            return true;
        } catch (err) {
            return false;
        }
    }

    function updateUrlLangParam(lang) {
        const params = new URLSearchParams(window.location.search);
        params.set('lang', lang);
        const newUrl = `${window.location.pathname}?${params.toString()}`;
        history.replaceState(null, '', newUrl);
    }

    function applyPageTranslations(translationsSection) {
        const elementsToTranslate = document.querySelectorAll('[data-translate-key], [data-translate-key-title], [data-translate-key-placeholder]');
        let translatedCount = 0;
        elementsToTranslate.forEach((element, index) => {
            const textKey = element.getAttribute('data-translate-key');
            const titleKey = element.getAttribute('data-translate-key-title');
            const placeholderKey = element.getAttribute('data-translate-key-placeholder');

            if (textKey && translationsSection[textKey] !== undefined) {
                const translation = translationsSection[textKey];
                if (element.tagName === 'INPUT') {
                    if (element.type === 'submit' || element.type === 'button') {
                        element.value = translation;
                    } else {
                        element.value = translation;
                    }
                } else if (element.tagName === 'BUTTON') {
                    element.innerHTML = translation;
                } else {
                    element.innerHTML = translation;
                }
                translatedCount++;
            }

            if (titleKey && translationsSection[titleKey] !== undefined) {
                element.title = translationsSection[titleKey];
                translatedCount++;
            }

            if (placeholderKey && translationsSection[placeholderKey] !== undefined) {
                element.placeholder = translationsSection[placeholderKey];
                translatedCount++;
            }
        });

        let translatedByIdCount = 0;
        Object.keys(translationsSection).forEach(key => {
            const elementById = document.getElementById(key);
            if (elementById && !elementById.hasAttribute('data-translate-key')) {
                translatedByIdCount++;
                if (elementById.tagName === 'INPUT' && (elementById.type === 'submit' || elementById.type === 'button')) {
                    elementById.value = translationsSection[key];
                } else if (elementById.tagName === 'BUTTON') {
                    elementById.innerHTML = translationsSection[key];
                } else {
                    elementById.innerHTML = translationsSection[key];
                }
            }
        });
    }

    function populateLanguageSelector() {

        if (!languageSelector) return;

        languageSelector.innerHTML = '';
        function capitalize(str) {
            return str.charAt(0).toUpperCase() + str.slice(1);
        }

        const sortedLanguages = [...availableLanguages].sort();
        sortedLanguages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang;
            option.textContent = capitalize(lang);
            languageSelector.appendChild(option);
        });
    }

    async function initializeTranslations() {

        const currentLang = getCurrentLang();
        document.documentElement.lang = currentLang;

        if (languageSelector) {
            $('#select-language').val(currentLang);
            $('#select-language').selectpicker('render');
        }

        updateUrlLangParam(currentLang);
        await loadAndApplyTranslations(currentLang);
    }
    initializeTranslations();

    if (languageSelector) {

        $('#select-language').on('change', async function () {
            const newLang = this.value;
            console.log(`Language changed to: ${newLang}`);
            localStorage.setItem('preferredLang', newLang);
            updateUrlLangParam(newLang);
            const success = await loadAndApplyTranslations(newLang);
            if (success) {
                document.documentElement.lang = newLang;
                const modal = document.querySelector('.project-modal');
                if (modal && modal.style.display === 'block' && modal.dataset.currentProjectId) {
                    updateModalContent(modal.dataset.currentProjectId);
                }
            } else {
                console.error(`Error al cargar las traducciones para: ${newLang}`);
            }
        });
    }
});