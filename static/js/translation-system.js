// translation-system.js - Sistema completo de traducción

class TranslationSystem {
    constructor() {
        this.currentLang = 'english';
        this.translations = {};
        this.originalTexts = {};
        this.languageMap = {
            "spanish": "es",
            "mandarin": "zh-CN",
            "french": "fr",
            "arabic": "ar",
            "portuguese": "pt",
            "russian": "ru",
            "japanese": "ja",
            "korean": "ko",
            "italian": "it",
            "greek": "el",
            "turkish": "tr",
            "dutch": "nl",
            "swedish": "sv",
            "finnish": "fi",
            "norwegian": "no",
            "danish": "da",
            "german": "de"
        };
        this.allowedTags = ['h1', 'h2', 'h3', 'h4', 'a', 'p', 'label', 'button', 'th', 'li', 'div'];
        this.init();
    }

    async init() {
        await this.loadStopwords();
        await this.loadTranslations();
        this.setupLanguageSelector();
        this.extractOriginalTexts();
        this.loadSavedLanguage();
    }

    async loadStopwords() {
        try {
            const response = await fetch('static/json/stopwords.json');
            const stopwords = await response.json();
            this.populateLanguageSelector(stopwords);
        } catch (error) {
            console.error('Error loading stopwords:', error);
        }
    }

    populateLanguageSelector(stopwords) {
        const select = document.getElementById('select-language');
        if (!select) return;

        // Agregar inglés como opción por defecto
        const englishOption = document.createElement('option');
        englishOption.value = 'english';
        englishOption.textContent = 'English';
        select.appendChild(englishOption);

        // Agregar otros idiomas
        Object.keys(stopwords).forEach(lang => {
            if (lang !== 'english') {
                const option = document.createElement('option');
                option.value = lang;
                option.textContent = lang.charAt(0).toUpperCase() + lang.slice(1);
                select.appendChild(option);
            }
        });
    }

    async loadTranslations() {
        // Cargar todas las traducciones disponibles
        for (const [langName, langCode] of Object.entries(this.languageMap)) {
            try {
                const response = await fetch(`static/json/texts_${langCode}.json`);
                if (response.ok) {
                    this.translations[langName] = await response.json();
                }
            } catch (error) {
                console.warn(`Could not load translations for ${langName}:`, error);
            }
        }

        // Cargar textos en inglés
        try {
            const response = await fetch('static/json/texts_en.json');
            if (response.ok) {
                this.translations['english'] = await response.json();
            }
        } catch (error) {
            console.warn('Could not load English texts:', error);
        }
    }

    extractOriginalTexts() {
        // Usar WeakMap para evitar memory leaks
        this.elementMap = new WeakMap();
        let globalIndex = 0;

        this.allowedTags.forEach(tag => {
            const elements = document.querySelectorAll(tag);
            elements.forEach((element, index) => {
                const text = this.getElementText(element);
                if (text && text.length > 1 && !text.includes('{')) {
                    globalIndex++;
                    const key = `element_${globalIndex}`;

                    this.originalTexts[key] = {
                        element: element,
                        text: text,
                        tag: tag,
                        tagIndex: index + 1
                    };

                    // Mapear elemento directamente para acceso rápido
                    this.elementMap.set(element, key);
                    element.setAttribute('data-translate-key', key);
                }
            });
        });
    }

    getElementText(element) {
        // Obtener solo el texto directo del elemento, sin hijos
        const childElements = element.children;
        if (childElements.length > 0) {
            return Array.from(element.childNodes)
                .filter(node => node.nodeType === Node.TEXT_NODE)
                .map(node => node.textContent.trim())
                .join(' ')
                .trim();
        } else {
            return element.textContent.trim();
        }
    }

    setupLanguageSelector() {
        const select = document.getElementById('select-language');
        if (!select) return;

        select.addEventListener('change', async (e) => {
            const selectedLang = e.target.value;
            await this.changeLanguage(selectedLang);
            this.saveLanguagePreference(selectedLang);
        });
    }

    async changeLanguage(targetLang) {
        if (targetLang === this.currentLang) return;

        // Si es inglés, restaurar textos originales
        if (targetLang === 'english') {
            this.restoreOriginalTexts();
        } else {
            // Aplicar traducciones
            await this.applyTranslations(targetLang);
        }

        this.currentLang = targetLang;

        // Actualizar dirección de texto para idiomas RTL
        this.updateTextDirection(targetLang);

        // Actualizar atributo lang del documento
        document.documentElement.lang = this.languageMap[targetLang] || 'en';
    }

    async applyTranslations(targetLang) {
        const translations = this.translations[targetLang];
        if (!translations) {
            console.warn(`No translations available for ${targetLang}`);
            return;
        }

        // Aplicar traducciones usando las claves de mapeo
        Object.entries(this.originalTexts).forEach(([key, data]) => {
            const translationKey = this.findTranslationKey(data.text, translations);
            if (translationKey && translations[translationKey]) {
                this.updateElementText(data.element, translations[translationKey]);
            }
        });
    }

    findTranslationKey(originalText, translations) {
        // Buscar la clave de traducción que corresponde al texto original
        const englishTranslations = this.translations['english'] || {};

        for (const [key, englishText] of Object.entries(englishTranslations)) {
            if (englishText.trim() === originalText.trim()) {
                return key;
            }
        }
        return null;
    }

    updateElementText(element, newText) {
        const childElements = element.children;
        if (childElements.length > 0) {
            // Si tiene elementos hijos, actualizar solo los nodos de texto
            Array.from(element.childNodes).forEach(node => {
                if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
                    node.textContent = newText;
                }
            });
        } else {
            // Si no tiene hijos, reemplazar todo el contenido
            element.textContent = newText;
        }
    }

    restoreOriginalTexts() {
        Object.values(this.originalTexts).forEach(data => {
            this.updateElementText(data.element, data.text);
        });
    }

    updateTextDirection(lang) {
        const rtlLanguages = ['arabic'];
        const isRTL = rtlLanguages.includes(lang);
        document.documentElement.dir = isRTL ? 'rtl' : 'ltr';
    }

    saveLanguagePreference(lang) {
        try {
            localStorage.setItem('preferred_language', lang);
        } catch (error) {
            console.warn('Could not save language preference:', error);
        }
    }

    loadSavedLanguage() {
        try {
            const savedLang = localStorage.getItem('preferred_language');
            if (savedLang && this.languageMap[savedLang]) {
                const select = document.getElementById('select-language');
                if (select) {
                    select.value = savedLang;
                    this.changeLanguage(savedLang);
                }
            }
        } catch (error) {
            console.warn('Could not load saved language:', error);
        }
    }
}

// Inicializar el sistema cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.translationSystem = new TranslationSystem();
});

// Función global para cambiar idioma programáticamente
window.changeLanguage = function (lang) {
    if (window.translationSystem) {
        window.translationSystem.changeLanguage(lang);
    }
};