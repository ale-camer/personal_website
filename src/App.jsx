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
  const slug = window.location.hash.replace('#', '').split('/')[0].toLowerCase();
  const match = Object.entries(SECTION_SLUGS).find(([, s]) => s === slug);
  return match ? match[0] : null;
}

function OriginalSocialLinks() {
  return (
    <div className="social-original-links" aria-label="Redes y contacto directo">
      {/* GitHub */}
      <a
        href="https://github.com/ale-camer/"
        target="_blank"
        rel="noreferrer"
        className="social-orig-link"
        title="GitHub (ale-camer)"
        aria-label="GitHub"
      >
        <svg className="social-brand-svg github-svg" viewBox="0 0 24 24" aria-hidden="true">
          <path
            fill="currentColor"
            d="M12 .5C5.65.5.5 5.65.5 12c0 5.09 3.29 9.4 7.86 10.92.58.1.79-.25.79-.56 0-.28-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.28-1.68-1.28-1.68-1.05-.71.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.76 2.7 1.25 3.36.96.1-.75.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.68 0-1.26.45-2.28 1.18-3.09-.12-.29-.51-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11.05 11.05 0 0 1 5.78 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.59.24 2.76.12 3.05.74.81 1.18 1.83 1.18 3.09 0 4.41-2.69 5.38-5.26 5.67.41.36.78 1.06.78 2.14 0 1.55-.01 2.79-.01 3.17 0 .31.21.67.8.56A11.51 11.51 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5Z"
          />
        </svg>
      </a>

      {/* LinkedIn */}
      <a
        href="https://www.linkedin.com/in/alejandro-camerlengo-1ab3981b/"
        target="_blank"
        rel="noreferrer"
        className="social-orig-link"
        title="LinkedIn"
        aria-label="LinkedIn"
      >
        <svg className="social-brand-svg" viewBox="0 0 24 24" aria-hidden="true">
          <rect width="24" height="24" rx="4.5" fill="#0A66C2" />
          <path
            fill="#FFFFFF"
            d="M7.12 9.5H4.18V19h2.94V9.5ZM5.65 8.22c.96 0 1.73-.78 1.73-1.74a1.73 1.73 0 1 0-3.46 0c0 .96.77 1.74 1.73 1.74ZM19.82 19h-2.93v-4.63c0-1.1-.02-2.52-1.54-2.52-1.54 0-1.77 1.2-1.77 2.44V19h-2.94V9.5h2.82v1.3h.04c.39-.75 1.35-1.54 2.78-1.54 2.98 0 3.54 1.96 3.54 4.51V19Z"
          />
        </svg>
      </a>

      {/* Gmail */}
      <a
        href="mailto:alejandrocamerlengo@gmail.com"
        className="social-orig-link"
        title="Email (Gmail)"
        aria-label="Email"
      >
        <svg className="social-brand-svg" viewBox="0 0 24 24" aria-hidden="true">
          <path
            fill="#4285F4"
            d="M2.5 6.75V18c0 .97.78 1.75 1.75 1.75H6V9.82L2.5 6.75Z"
          />
          <path
            fill="#34A853"
            d="M18 19.75h1.75c.97 0 1.75-.78 1.75-1.75V6.75L18 9.82v9.93Z"
          />
          <path
            fill="#FBBC05"
            d="M18 4.75v5.07l3.5-3.07V5.9c0-1.45-1.65-2.28-2.8-1.4L18 4.75Z"
          />
          <path
            fill="#EA4335"
            d="M6 9.82V4.75L12 9.2l6-4.45v5.07L12 14.27 6 9.82Z"
          />
          <path
            fill="#C5221F"
            d="M2.5 5.9v.85L6 9.82V4.75l-.7-.25C4.15 3.62 2.5 4.45 2.5 5.9Z"
          />
        </svg>
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
          sectionId={activeSection}
          label={NAV_ITEMS.find((item) => item.id === activeSection)?.label}
          colorMode={colorMode}
          onClose={() => selectSection(null)}
        />
      )}

      {/* REDES DE CONTACTO ABAJO A LA IZQUIERDA */}
      <div className="l-pos-bottom-left">
        <div className="utility-pill-group social-pill-group">
          <OriginalSocialLinks />
        </div>
      </div>

      {/* PREFERENCIAS ABAJO A LA DERECHA: IDIOMA + TEMA */}
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
