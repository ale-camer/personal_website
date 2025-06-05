document.addEventListener('DOMContentLoaded', function () {
    const languageSelector = document.getElementById('select-language');
    const langJsonBaseUrl = "/static/json/lang/";

    // Lista de idiomas que realmente tenés - EDITÁ ESTA LISTA
    const availableLanguages = ['english', 'spanish', 'french', 'german', 'italian', 'portuguese', 'russian', 'japanese', 'korean', 'arabic', 'dutch', 'swedish', 'danish', 'finnish'];

    function getPageKey() {
        const pathname = window.location.pathname;

        // Si la ruta es la raíz (/) o termina en index.html, la clave de página es "home"
        if (pathname === '/' || pathname.endsWith('/index.html') || pathname.endsWith('/')) {
            return 'home';
        }

        // Para otras páginas, extrae el nombre del archivo sin .html
        const pageName = pathname.split('/').pop().replace('.html', '');

        // Si por alguna razón la página se llama 'index', también la tratamos como 'home'
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
        const flaskLang = 'spanish'; // Cambiá esto por tu idioma por defecto
        if (flaskLang === 'es') return 'spanish';
        if (flaskLang === 'en') return 'english';
        return availableLanguages.includes(flaskLang) ? flaskLang : 'spanish';
    }

    async function loadAndApplyTranslations(lang) {
        try {
            const response = await fetch(`${langJsonBaseUrl}${lang}.json`);
            if (!response.ok) {
                console.log(`Error loading ${lang}.json: ${response.status}`);
                return false;
            }

            const allTranslations = await response.json();
            console.log(`Loaded ${lang}.json, looking for page: ${pageKey}`);

            // 1. Obtener las traducciones comunes (siempre se aplican).
            const commonTranslations = allTranslations['common'] || {};

            // 2. Obtener las traducciones específicas de la página actual.
            const pageTranslations = allTranslations[pageKey] || {};

            if (Object.keys(pageTranslations).length === 0) {
                console.warn(`Section ${pageKey} not found or is empty in ${lang}.json`);
            }

            // 3. Fusionar las traducciones. Las específicas de la página sobreescriben a las comunes si hay conflicto.
            const finalTranslations = { ...commonTranslations, ...pageTranslations };

            console.log(`Applying merged translations...`);
            applyPageTranslations(finalTranslations);
            console.log('Translations applied successfully');
            return true;

        } catch (err) {
            console.log('Error in loadAndApplyTranslations:', err);
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
        console.log('Applying translations to section:', translationsSection);
        const elementsToTranslate = document.querySelectorAll('[data-translate-key], [data-translate-key-title], [data-translate-key-placeholder]');
        console.log(`Found ${elementsToTranslate.length} elements with translation attributes`);

        let translatedCount = 0;
        elementsToTranslate.forEach((element, index) => {
            const textKey = element.getAttribute('data-translate-key');
            const titleKey = element.getAttribute('data-translate-key-title');
            const placeholderKey = element.getAttribute('data-translate-key-placeholder');

            console.log(`Element ${index + 1}:`, {
                tagName: element.tagName,
                id: element.id || 'no-id',
                className: element.className || 'no-class',
                textKey: textKey,
                titleKey: titleKey,
                placeholderKey: placeholderKey,
                currentText: element.innerHTML || element.value || element.placeholder
            });

            if (textKey && translationsSection[textKey] !== undefined) {
                const translation = translationsSection[textKey];
                console.log(`Translating ${textKey} from "${element.innerHTML || element.value}" to: "${translation}"`);

                if (element.tagName === 'INPUT') {
                    if (element.type === 'submit' || element.type === 'button') {
                        element.value = translation;
                    } else {
                        element.value = translation; // Para otros tipos de input también
                    }
                } else if (element.tagName === 'BUTTON') {
                    element.innerHTML = translation;
                } else {
                    element.innerHTML = translation;
                }
                translatedCount++;
            } else if (textKey) {
                console.warn(`Translation key "${textKey}" not found in translations`);
            }

            if (titleKey && translationsSection[titleKey] !== undefined) {
                console.log(`Setting title for ${titleKey}: ${translationsSection[titleKey]}`);
                element.title = translationsSection[titleKey];
                translatedCount++;
            }

            if (placeholderKey && translationsSection[placeholderKey] !== undefined) {
                console.log(`Setting placeholder for ${placeholderKey}: ${translationsSection[placeholderKey]}`);
                element.placeholder = translationsSection[placeholderKey];
                translatedCount++;
            }
        });

        console.log(`Translated ${translatedCount} attributes using data-translate-key`);

        // También buscar por ID
        let translatedByIdCount = 0;
        Object.keys(translationsSection).forEach(key => {
            const elementById = document.getElementById(key);
            if (elementById && !elementById.hasAttribute('data-translate-key')) {
                console.log(`Translating element by ID ${key} from "${elementById.innerHTML || elementById.value}" to: "${translationsSection[key]}"`);
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
        console.log(`Translated ${translatedByIdCount} elements by ID`);

        // Verificación final - mostrar algunos elementos después de la traducción
        console.log('=== VERIFICATION ===');
        const sampleElements = document.querySelectorAll('[data-translate-key]');
        Array.from(sampleElements).slice(0, 5).forEach((el, i) => {
            console.log(`Sample element ${i + 1} after translation:`, {
                key: el.getAttribute('data-translate-key'),
                currentContent: el.innerHTML || el.value || el.placeholder,
                tagName: el.tagName
            });
        });
    }

    function populateLanguageSelector() {
        if (!languageSelector) return;

        languageSelector.innerHTML = '';

        function capitalize(str) {
            return str.charAt(0).toUpperCase() + str.slice(1);
        }

        // Ordena el array availableLanguages alfabéticamente.
        const sortedLanguages = [...availableLanguages].sort();

        sortedLanguages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang;
            option.textContent = capitalize(lang);
            languageSelector.appendChild(option);
        });
    }

    async function initializeTranslations() {
        populateLanguageSelector();

        const currentLang = getCurrentLang();
        document.documentElement.lang = currentLang;

        if (languageSelector) {
            languageSelector.value = currentLang;
        }

        updateUrlLangParam(currentLang);
        await loadAndApplyTranslations(currentLang);
    }

    initializeTranslations();

    if (languageSelector) {
        languageSelector.addEventListener('change', async function () {
            const newLang = this.value;
            console.log(`Changing language to: ${newLang}`);
            localStorage.setItem('preferredLang', newLang);
            document.documentElement.lang = newLang;
            updateUrlLangParam(newLang);
            // Recarga la página después de actualizar el idioma.
            window.location.reload();
        });
    }
});