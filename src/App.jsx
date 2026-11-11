import React, { useState, useEffect, useRef, Suspense, lazy } from 'react';
import IntangibleCanvasBackground from './components/IntangibleCanvasBackground';
import IdentityBadge from './components/IdentityBadge';
import TopNavBar, { getNavLabel } from './components/TopNavBar';
import HomeCenterShowcase from './components/HomeCenterShowcase';
import { LANGUAGES, FlagBadge } from './i18n/languages';
import { tx, useSiteLocale } from './i18n/localeService';

const SectionView = lazy(() => import('./components/SectionView'));
const LanguageModal = lazy(() => import('./components/LanguageModal'));

// id interno de sección -> slug visible en la URL
const SECTION_SLUGS = {
  playground: 'proyectos',
  research: 'analisis',
  timeline: 'mi-cv'
};

function readSectionFromHash() {
  if (window.location.hostname.toLowerCase().startsWith('macro.')) {
    return 'research';
  }
  const slug = window.location.hash.replace('#', '').split('/')[0].toLowerCase();
  if (slug === 'quantlambda' || slug === 'flagship') return 'playground';
  if (slug === 'recorrido' || slug === 'cv') return 'timeline';
  const match = Object.entries(SECTION_SLUGS).find(([, s]) => s === slug);
  return match ? match[0] : null;
}

function readInitialLang() {
  try {
    const saved = window.localStorage.getItem('ac_site_lang');
    if (saved && LANGUAGES.some((l) => l.code === saved)) {
      return saved;
    }
  } catch {
    // ignore storage errors
  }
  return 'ES';
}

function OriginalSocialLinks({ lang }) {
  return (
    <div
      className="social-original-links"
      aria-label={tx('Redes y contacto directo', 'Social networks and direct contact', lang)}
    >
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

function LanguageTriggerButton({ lang, open, setOpen }) {
  const selected = LANGUAGES.find((l) => l.code === lang) || LANGUAGES[0];
  return (
    <div className="lang-dropdown-root">
      <button
        type="button"
        className={`lang-single-trigger ${open ? 'is-open' : ''}`}
        onClick={() => setOpen((o) => !o)}
        title={`${tx('Seleccionar idioma (56 idiomas • Tecla L)', 'Select language (56 languages • Key L)', lang)} — ${selected.nativeName}`}
      >
        <FlagBadge lang={selected} width={18} height={12} />
        <span className="lang-flag-code">{selected.code}</span>
        <span className="lang-chevron">▾</span>
      </button>
    </div>
  );
}

function ThemeToggleBtn({ colorMode, setColorMode, lang }) {
  return (
    <button
      type="button"
      className="utility-theme-btn"
      onClick={() => setColorMode((m) => (m === 'dark' ? 'light' : 'dark'))}
      title={tx(
        'Cambiar modo Claro / Oscuro (Tecla T)',
        'Toggle Light / Dark mode (Key T)',
        lang
      )}
    >
      {colorMode === 'dark' ? '☀️' : '🌙'}
    </button>
  );
}

function UtilitiesCluster({
  lang,
  langOpen,
  setLangOpen,
  colorMode,
  setColorMode
}) {
  return (
    <div className="utility-pill-group">
      <LanguageTriggerButton lang={lang} open={langOpen} setOpen={setLangOpen} />
      <span className="utility-divider" />
      <ThemeToggleBtn colorMode={colorMode} setColorMode={setColorMode} lang={lang} />
    </div>
  );
}

export default function App() {
  const [colorMode, setColorMode] = useState('dark');
  const [lang, setLang] = useState(readInitialLang);
  const [langOpen, setLangOpen] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);
  const [activeSection, setActiveSection] = useState(readSectionFromHash);
  const keyBufferRef = useRef({ char: '', time: 0 });

  useSiteLocale(lang);

  // Sincroniza la sección activa con la URL (#proyectos, #analisis, #mi-cv)
  useEffect(() => {
    const handleHashChange = () => setActiveSection(readSectionFromHash());
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  // Pre-calentamiento silencioso (idle) de los contenedores Cloud Run de subdominios para evitar cold-starts en mobile
  useEffect(() => {
    const timer = setTimeout(() => {
      const warmupTargets = [
        'https://worldmap.alejandrocamerlengo.com/api/countries',
        'https://explorer.alejandrocamerlengo.com/',
        'https://qol-api-service-450135571603.us-central1.run.app/api/v1/metadata',
        'https://spark.alejandrocamerlengo.com/'
      ];
      warmupTargets.forEach((url) => {
        fetch(url, { mode: 'no-cors', cache: 'no-store' }).catch(() => {});
      });
    }, 2200);
    return () => clearTimeout(timer);
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

  const toggleTheme = () => setColorMode((m) => (m === 'dark' ? 'light' : 'dark'));
  const toggleChat = () => setChatOpen((o) => !o);
  const toggleLang = () => setLangOpen((o) => !o);

  const openExternalChannel = (channel) => {
    if (channel === 'gh') {
      window.open('https://github.com/ale-camer/', '_blank', 'noopener,noreferrer');
    } else if (channel === 'li') {
      window.open(
        'https://www.linkedin.com/in/alejandro-camerlengo-1ab3981b/',
        '_blank',
        'noopener,noreferrer'
      );
    } else if (channel === 'gm') {
      window.location.href = 'mailto:alejandrocamerlengo@gmail.com';
    }
  };

  // Atajos globales de teclado cuando el usuario no está tipeando texto libre en un input
  useEffect(() => {
    const handleGlobalKey = (e) => {
      if (langOpen) return;
      const activeEl = document.activeElement;
      const tag = activeEl?.tagName?.toLowerCase();
      const isHomeCmdInput = activeEl?.classList?.contains('hc-term-b-input');
      const hasTypedText = isHomeCmdInput && activeEl.value.trim().length > 0;

      // Si está escribiendo en el chat u otro input (o ya tipeó letras en el prompt), no pisar
      if ((tag === 'input' || tag === 'textarea') && (!isHomeCmdInput || hasTypedText)) {
        return;
      }
      if (e.metaKey || e.ctrlKey || e.altKey) return;

      const k = e.key.toLowerCase();
      const now = Date.now();
      const prev = keyBufferRef.current;

      // Secuencias de 2 teclas rápidas: gh (GitHub), li (LinkedIn), gm (Gmail)
      if (now - prev.time < 650) {
        const pair = prev.char + k;
        if (pair === 'gh' || pair === 'li' || pair === 'gm') {
          e.preventDefault();
          keyBufferRef.current = { char: '', time: 0 };
          openExternalChannel(pair);
          return;
        }
      }

      if (k === 'g' || k === 'l') {
        keyBufferRef.current = { char: k, time: now };
        if (k === 'g') {
          e.preventDefault();
          return;
        }
      }

      if (k === '1') {
        e.preventDefault();
        selectSection('playground');
      } else if (k === '2') {
        e.preventDefault();
        selectSection('research');
      } else if (k === '3') {
        e.preventDefault();
        selectSection('timeline');
      } else if (k === 'c') {
        e.preventDefault();
        toggleChat();
      } else if (k === 't') {
        e.preventDefault();
        toggleTheme();
      } else if (k === 'l') {
        e.preventDefault();
        // Pequeña espera de 240ms por si la segunda tecla es "i" (li -> LinkedIn)
        setTimeout(() => {
          if (keyBufferRef.current.char === 'l') {
            keyBufferRef.current = { char: '', time: 0 };
            setLangOpen((o) => !o);
          }
        }, 240);
      }
    };

    window.addEventListener('keydown', handleGlobalKey);
    return () => window.removeEventListener('keydown', handleGlobalKey);
  }, [langOpen]);

  return (
    <div className={`canvas-shell mode-${colorMode}`}>
      {/* ELEMENTO 1: FONDO MULTICAPA DE RED */}
      <IntangibleCanvasBackground colorMode={colorMode} isPaused={Boolean(activeSection) || langOpen} />

      {/* CABECERA: IDENTIDAD (IZQUIERDA) + NAVEGACIÓN (DERECHA) */}
      <header className="l-pos-top-split">
        <IdentityBadge
          accentHex="#25D366"
          accentTextColor="#06140c"
          colorMode={colorMode}
          lang={lang}
          externalOpen={chatOpen}
          onDrawerChange={setChatOpen}
          onSelectSection={selectSection}
        />
        <TopNavBar
          activeId={activeSection}
          onSelect={selectSection}
          lang={lang}
          navStyle="capsule"
          navFont="orbitron"
          accentHex="#10b981"
        />
      </header>

      {/* TERMINAL CENTRAL DEL HOME */}
      {!activeSection && (
        <HomeCenterShowcase
          lang={lang}
          onSelectSection={selectSection}
          onToggleChat={toggleChat}
          onToggleTheme={toggleTheme}
          onToggleLang={toggleLang}
          onOpenExternal={openExternalChannel}
        />
      )}

      {/* SECCIÓN ACTIVA — PANEL CENTRAL */}
      {activeSection && (
        <Suspense fallback={null}>
          <SectionView
            sectionId={activeSection}
            label={getNavLabel(activeSection, lang)}
            colorMode={colorMode}
            lang={lang}
            onClose={() => selectSection(null)}
          />
        </Suspense>
      )}

      {/* MODAL CENTRADO DE SELECCIÓN DE IDIOMA (56 IDIOMAS CON BUSCADOR Y BANDERAS SVG) */}
      {langOpen && (
        <Suspense fallback={null}>
          <LanguageModal lang={lang} setLang={setLang} open={langOpen} setOpen={setLangOpen} />
        </Suspense>
      )}

      {/* REDES DE CONTACTO ABAJO A LA IZQUIERDA */}
      <div className="l-pos-bottom-left">
        <div className="utility-pill-group social-pill-group">
          <OriginalSocialLinks lang={lang} />
        </div>
      </div>

      {/* PREFERENCIAS ABAJO A LA DERECHA: IDIOMA + TEMA */}
      <div className="l-pos-bottom-right">
        <UtilitiesCluster
          lang={lang}
          langOpen={langOpen}
          setLangOpen={setLangOpen}
          colorMode={colorMode}
          setColorMode={setColorMode}
        />
      </div>
    </div>
  );
}
