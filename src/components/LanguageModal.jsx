import React, { useState, useEffect, useRef, useMemo } from 'react';
import { LANGUAGES, FlagBadge } from '../i18n/languages';
import { tx, useSiteLocale } from '../i18n/localeService';

export default function LanguageModal({ lang = 'ES', setLang, open, setOpen }) {
  useSiteLocale(lang);
  const [searchQuery, setSearchQuery] = useState('');
  const [dropdownOpen, setDropdownOpen] = useState(true);
  const [kbIdx, setKbIdx] = useState(0);
  const searchInputRef = useRef(null);
  const activeOptionRef = useRef(null);

  const currentLang = useMemo(
    () => LANGUAGES.find((l) => l.code === lang) || LANGUAGES[0],
    [lang]
  );

  const filteredLanguages = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    return LANGUAGES.filter((item) => {
      if (!q) return true;
      return (
        item.nativeName.toLowerCase().includes(q) ||
        item.name.toLowerCase().includes(q) ||
        item.code.toLowerCase().includes(q) ||
        item.region.toLowerCase().includes(q)
      );
    });
  }, [searchQuery]);

  useEffect(() => {
    if (!open) return undefined;
    setSearchQuery('');
    setDropdownOpen(true);
    const currentIndex = LANGUAGES.findIndex((l) => l.code === lang);
    setKbIdx(currentIndex >= 0 ? currentIndex : 0);

    const timer = setTimeout(() => {
      searchInputRef.current?.focus();
    }, 35);

    const handleGlobalEsc = (e) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        e.stopPropagation();
        setOpen(false);
      }
    };

    window.addEventListener('keydown', handleGlobalEsc, true);
    return () => {
      clearTimeout(timer);
      window.removeEventListener('keydown', handleGlobalEsc, true);
    };
  }, [open, lang, setOpen]);

  useEffect(() => {
    if (open && activeOptionRef.current) {
      activeOptionRef.current.scrollIntoView({ block: 'nearest' });
    }
  }, [kbIdx, open]);

  const handleChooseLanguage = (langObj) => {
    if (!langObj) return;
    setLang(langObj.code);
    try {
      window.localStorage.setItem('ac_site_lang', langObj.code);
    } catch {
      // ignore storage errors
    }
    setOpen(false);
  };

  if (!open) return null;

  return (
    <div
      className="lmodal-backdrop"
      onMouseDown={(e) => {
        if (e.target === e.currentTarget) setOpen(false);
      }}
    >
      <div className="lmodal-card" role="dialog" aria-modal="true" aria-label="Language selector">
        {/* CABECERA DEL MODAL */}
        <div className="lmodal-header">
          <div className="lmodal-header-main">
            <div className="lmodal-title-row">
              <span className="lmodal-title">
                {tx('Seleccionar Idioma de Interfaz', 'Select Interface Language', lang)}
              </span>
              <span className="lmodal-count-pill">
                {LANGUAGES.length} {tx('IDIOMAS', 'LANGUAGES', lang)}
              </span>
            </div>
            <p className="lmodal-subtitle">
              {tx(
                'Escribí el idioma en su lengua original (ej. Español, English, Português, Français, Deutsch, 日本語) o seleccioná del listado.',
                'Type the language in its original script (e.g. Español, English, Deutsch, 日本語, العربية) or choose from the list below.',
                lang
              )}
            </p>
          </div>

          <button
            type="button"
            className="lmodal-close-btn"
            onClick={() => setOpen(false)}
            title={tx('Cerrar (Esc)', 'Close (Esc)', lang)}
            aria-label={tx('Cerrar', 'Close', lang)}
          >
            ✕
          </button>
        </div>

        {/* PÍLDORA DEL IDIOMA ACTIVO */}
        <div className="lmodal-active-banner">
          <div className="lmodal-active-left">
            <FlagBadge lang={currentLang} width={22} height={15} />
            <div className="lmodal-active-names">
              <strong>{currentLang.nativeName}</strong>{' '}
              <span>
                ({currentLang.name} • {currentLang.region})
              </span>
            </div>
          </div>
          <span className="lmodal-active-tag">
            {tx('ACTIVO', 'ACTIVE', lang)} • {currentLang.code}
          </span>
        </div>

        {/* BUSCADOR + LISTADO DESPLEGABLE DE 56 IDIOMAS */}
        <div className="lmodal-body">
          <div className="lmodal-search-box">
            <svg
              className="lmodal-search-icon"
              viewBox="0 0 24 24"
              width="15"
              height="15"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>

            <input
              ref={searchInputRef}
              type="text"
              className="lmodal-search-input"
              value={searchQuery}
              onFocus={() => setDropdownOpen(true)}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setDropdownOpen(true);
                setKbIdx(0);
              }}
              onKeyDown={(e) => {
                if (!filteredLanguages.length) return;
                if (e.key === 'ArrowDown') {
                  e.preventDefault();
                  setDropdownOpen(true);
                  setKbIdx((prev) => (prev + 1) % filteredLanguages.length);
                } else if (e.key === 'ArrowUp') {
                  e.preventDefault();
                  setDropdownOpen(true);
                  setKbIdx((prev) => (prev - 1 + filteredLanguages.length) % filteredLanguages.length);
                } else if (e.key === 'Enter') {
                  e.preventDefault();
                  const chosen = filteredLanguages[kbIdx] || filteredLanguages[0];
                  if (chosen) handleChooseLanguage(chosen);
                }
              }}
              placeholder={tx(
                'Escribir idioma en su lengua original (ej. Español, Français, Deutsch, 日本語)...',
                'Type language in original script (e.g. Español, Français, Deutsch, 日本語)...',
                lang
              )}
            />

            {searchQuery && (
              <button
                type="button"
                className="lmodal-clear-btn"
                onClick={() => {
                  setSearchQuery('');
                  setKbIdx(0);
                  searchInputRef.current?.focus();
                }}
                aria-label="Clear search"
              >
                ✕
              </button>
            )}

            <button
              type="button"
              className="lmodal-chevron-btn"
              onClick={() => setDropdownOpen((prev) => !prev)}
              aria-label="Toggle list"
            >
              {dropdownOpen ? '▴' : '▾'}
            </button>
          </div>

          {dropdownOpen && (
            <div className="lmodal-list" role="listbox">
              {filteredLanguages.length === 0 ? (
                <div className="lmodal-empty">
                  {tx('No se encontró ningún idioma para', 'No matching language found for', lang)} &ldquo;
                  {searchQuery}&rdquo;
                </div>
              ) : (
                filteredLanguages.map((item, idx) => {
                  const isSelected = currentLang.code === item.code;
                  const isKbFocused = idx === kbIdx;
                  return (
                    <button
                      key={item.code}
                      ref={isKbFocused ? activeOptionRef : null}
                      type="button"
                      role="option"
                      aria-selected={isSelected}
                      className={`lmodal-option ${isSelected ? 'is-selected' : ''} ${isKbFocused ? 'is-kb-focus' : ''}`}
                      onMouseEnter={() => setKbIdx(idx)}
                      onClick={() => handleChooseLanguage(item)}
                    >
                      <div className="lmodal-opt-left">
                        <FlagBadge lang={item} width={22} height={15} />
                        <div className="lmodal-opt-text">
                          <span className="lmodal-opt-native">{item.nativeName}</span>
                          <span className="lmodal-opt-meta">
                            {item.name} • {item.region}
                          </span>
                        </div>
                      </div>

                      <div className="lmodal-opt-right">
                        <span className={`lmodal-opt-code ${isSelected ? 'is-selected' : ''}`}>
                          {item.code}
                        </span>
                        {isSelected && <span className="lmodal-opt-check">✓</span>}
                      </div>
                    </button>
                  );
                })
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
