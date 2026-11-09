import React, { useState, useEffect, useRef } from 'react';
import IntangibleCanvasBackground from './components/IntangibleCanvasBackground';
import IdentityBadge from './components/IdentityBadge';
import TopNavBar, { NAV_ITEMS } from './components/TopNavBar';
import SectionView from './components/SectionView';

const LANGUAGES = [
  { code: 'ES', flag: '/images/flags/es.svg', label: 'Español' },
  { code: 'EN', flag: '/images/flags/en.svg', label: 'English' },
  { code: 'PT', flag: '/images/flags/pt.svg', label: 'Português' },
  { code: 'DE', flag: '/images/flags/de.svg', label: 'Deutsch' },
  { code: 'FR', flag: '/images/flags/fr.svg', label: 'Français' },
  { code: 'IT', flag: '/images/flags/it.svg', label: 'Italiano' },
  { code: 'ZH', flag: '/images/flags/cn.svg', label: '中文' },
  { code: 'JA', flag: '/images/flags/jp.svg', label: '日本語' },
  { code: 'KO', flag: '/images/flags/kr.svg', label: '한국어' },
  { code: 'NL', flag: '/images/flags/nl.svg', label: 'Nederlands' },
  { code: 'RU', flag: '/images/flags/ru.svg', label: 'Русский' },
  { code: 'SV', flag: '/images/flags/se.svg', label: 'Svenska' },
  { code: 'DA', flag: '/images/flags/dk.svg', label: 'Dansk' },
  { code: 'FI', flag: '/images/flags/fi.svg', label: 'Suomi' },
  { code: 'EL', flag: '/images/flags/gr.svg', label: 'Ελληνικά' },
  { code: 'TR', flag: '/images/flags/tr.svg', label: 'Türkçe' },
  { code: 'AR', flag: '/images/flags/sa.svg', label: 'العربية' }
];

// id interno de sección -> slug visible en la URL
const SECTION_SLUGS = {
  flagship: 'quantlambda',
  research: 'analisis',
  playground: 'proyectos',
  timeline: 'recorrido'
};

function readSectionFromHash() {
  const slug = window.location.hash.replace('#', '').toLowerCase();
  const match = Object.entries(SECTION_SLUGS).find(([, s]) => s === slug);
  return match ? match[0] : null;
}

function OriginalSocialLinks() {
  return (
    <div className="social-original-links">
      <a
        href="https://github.com/ale-camer/personal_website"
        target="_blank"
        rel="noreferrer"
        className="social-orig-link"
        title="GitHub"
      >
        <img src="/images/gh.png" alt="GitHub" className="social-orig-img" />
      </a>
      <a
        href="https://www.linkedin.com/in/alejandro-camerlengo-1ab3981b/"
        target="_blank"
        rel="noreferrer"
        className="social-orig-link"
        title="LinkedIn"
      >
        <img src="/images/li.png" alt="LinkedIn" className="social-orig-img" />
      </a>
      <a
        href="mailto:alejandrocamerlengo@gmail.com"
        className="social-orig-link"
        title="Email"
      >
        <img src="/images/email.png" alt="Email" className="social-orig-img" />
      </a>
    </div>
  );
}

function LanguageDropdown({ lang, setLang, openDirection = 'up' }) {
  const [open, setOpen] = useState(false);
  const wrapRef = useRef(null);

  const selected = LANGUAGES.find((l) => l.code === lang) || LANGUAGES[0];
  const otherOptions = LANGUAGES.filter((l) => l.code !== selected.code);

  useEffect(() => {
    if (!open) return;
    const handleOutside = (e) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleOutside);
    return () => document.removeEventListener('mousedown', handleOutside);
  }, [open]);

  return (
    <div className="lang-dropdown-root" ref={wrapRef}>
      <button
        type="button"
        className={`lang-single-trigger ${open ? 'is-open' : ''}`}
        onClick={() => setOpen((o) => !o)}
        title={`Idioma actual: ${selected.label}`}
      >
        <img src={selected.flag} alt={selected.code} className="lang-flag-img" />
        <span className="lang-flag-code">{selected.code}</span>
        <span className="lang-chevron">▾</span>
      </button>

      {open && (
        <div className={`lang-options-menu dir-${openDirection}`}>
          {otherOptions.map((item) => (
            <button
              key={item.code}
              type="button"
              className="lang-option-item"
              onClick={() => {
                setLang(item.code);
                setOpen(false);
              }}
              title={item.label}
            >
              <img src={item.flag} alt={item.code} className="lang-flag-img" />
              <span className="lang-flag-code">{item.code}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

function ThemeToggleBtn({ colorMode, setColorMode }) {
  return (
    <button
      type="button"
      className="utility-theme-btn"
      onClick={() => setColorMode((m) => (m === 'dark' ? 'light' : 'dark'))}
      title="Cambiar modo Claro / Oscuro"
    >
      {colorMode === 'dark' ? '☀️' : '🌙'}
    </button>
  );
}

function UtilitiesCluster({ lang, setLang, colorMode, setColorMode, openDirection = 'up' }) {
  return (
    <div className="utility-pill-group">
      <OriginalSocialLinks />
      <span className="utility-divider" />
      <LanguageDropdown lang={lang} setLang={setLang} openDirection={openDirection} />
      <span className="utility-divider" />
      <ThemeToggleBtn colorMode={colorMode} setColorMode={setColorMode} />
    </div>
  );
}

export default function App() {
  const [colorMode, setColorMode] = useState('dark');
  const [lang, setLang] = useState('ES');
  const [activeSection, setActiveSection] = useState(readSectionFromHash);

  // Sincroniza la sección activa con la URL (#quantlambda, #analisis, ...)
  // para poder compartir links y usar el botón "atrás" del navegador.
  useEffect(() => {
    const handleHashChange = () => setActiveSection(readSectionFromHash());
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const selectSection = (id) => {
    const slug = id ? SECTION_SLUGS[id] : '';
    if (slug) {
      window.location.hash = slug;
    } else {
      history.pushState(null, '', window.location.pathname + window.location.search);
      setActiveSection(null);
    }
  };

  return (
    <div className={`canvas-shell mode-${colorMode}`}>
      {/* ELEMENTO 1: FONDO MULTICAPA DE RED */}
      <IntangibleCanvasBackground colorMode={colorMode} />

      {/* CABECERA: IDENTIDAD (IZQUIERDA) + NAVEGACIÓN (DERECHA) */}
      <header className="l-pos-top-split">
        <IdentityBadge
          accentHex="#25D366"
          accentTextColor="#06140c"
          colorMode={colorMode}
        />
        <TopNavBar
          activeId={activeSection}
          onSelect={selectSection}
          navStyle="capsule"
          navFont="orbitron"
          accentHex="#10b981"
        />
      </header>

      {/* PROPUESTA CENTRAL — PLACEHOLDER (texto definitivo pendiente, ver docs/MASTER_BLUEPRINT.md §4) */}
      {!activeSection && (
        <div className="hero-tagline-slot" aria-hidden="true">
          <p className="hero-tagline-placeholder">[ Propuesta central — texto pendiente ]</p>
        </div>
      )}

      {/* SECCIÓN ACTIVA — PANEL CENTRAL */}
      {activeSection && (
        <SectionView
          label={NAV_ITEMS.find((item) => item.id === activeSection)?.label}
          onClose={() => selectSection(null)}
        />
      )}

      {/* UTILIDADES INFERIORES: REDES + IDIOMA + TEMA */}
      <div className="l-pos-bottom-right">
        <UtilitiesCluster
          lang={lang}
          setLang={setLang}
          colorMode={colorMode}
          setColorMode={setColorMode}
          openDirection="up"
        />
      </div>
    </div>
  );
}
