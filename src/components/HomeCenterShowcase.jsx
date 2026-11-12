import React, { useState, useEffect, useRef } from 'react';
import { tx, useSiteLocale } from '../i18n/localeService';

export const TERMINAL_BULLETS = [
  {
    id: 'proyectos',
    num: '01',
    codeEs: '[1] o proyectos',
    codeEn: '[1] or projects',
    descEs: 'Explorar QuantLambda (mi proyecto insignia) y 3 apps interactivas.',
    descEn: 'Explore QuantLambda (my flagship platform) and 3 interactive apps.',
    actionType: 'section',
    target: 'playground'
  },
  {
    id: 'analisis',
    num: '02',
    codeEs: '[2] o analisis',
    codeEn: '[2] or research',
    descEs: 'Leer investigaciones propias (Macroeconomía y Empleo en Argentina).',
    descEn: 'Read original empirical research (Macroeconomics & Employment in Argentina).',
    actionType: 'section',
    target: 'research'
  },
  {
    id: 'mi-cv',
    num: '03',
    codeEs: '[3] o mi-cv',
    codeEn: '[3] or my-cv',
    descEs: 'Ver mi experiencia laboral, posgrados (2011–2026) y descargar el CV en PDF.',
    descEn: 'View my work experience, graduate degrees (2011–2026), and download my PDF CV.',
    actionType: 'section',
    target: 'timeline'
  },
  {
    id: 'chat',
    num: '04',
    codeEs: '[c] o chat',
    codeEn: '[c] or chat',
    descEs: 'Abrir el asistente conversacional de arriba a la izquierda.',
    descEn: 'Open the conversational assistant at the top left.',
    actionType: 'chat'
  },
  {
    id: 'socials',
    num: '05',
    codeEs: 'gh · li · gm',
    codeEn: 'gh · li · gm',
    descEs: 'Ir directo a mi GitHub, LinkedIn o enviarme un Gmail.',
    descEn: 'Go directly to my GitHub, LinkedIn, or send me a Gmail.',
    actionType: 'socials'
  },
  {
    id: 'prefs',
    num: '06',
    codeEs: '[l] idioma · [t] tema',
    codeEn: '[l] language · [t] theme',
    descEs: 'Cambiar el idioma de la página o alternar modo oscuro / claro.',
    descEn: 'Change the interface language or toggle dark / light mode.',
    actionType: 'prefs'
  },
  {
    id: 'nav',
    num: '07',
    codeEs: '[↑/↓] + [Enter] · [Esc]',
    codeEn: '[↑/↓] + [Enter] · [Esc]',
    descEs: 'Moverte adentro de cada sección, abrir elementos y volver atrás.',
    descEn: 'Move inside each section, open items, and go back.',
    actionType: 'info'
  }
];

let hasPlayedInitialBoot = false;

function shouldPlayInitialBoot() {
  if (hasPlayedInitialBoot) return false;
  if (typeof window === 'undefined') return false;
  if (window.location.hash && window.location.hash.length > 1) {
    hasPlayedInitialBoot = true;
    return false;
  }
  try {
    if (window.sessionStorage.getItem('ac_boot_done') === '1') {
      hasPlayedInitialBoot = true;
      return false;
    }
  } catch {
    // Ignore storage restrictions
  }
  return true;
}

export default function HomeCenterShowcase({
  lang = 'ES',
  onSelectSection,
  onToggleChat,
  onToggleTheme,
  onToggleLang,
  onOpenExternal
}) {
  useSiteLocale(lang);
  const [isBooting, setIsBooting] = useState(() => shouldPlayInitialBoot());
  const [isCommandsOpen, setIsCommandsOpen] = useState(false);
  const [selectedIdx, setSelectedIdx] = useState(0);
  const [cmdInput, setCmdInput] = useState('');
  const [feedbackMsg, setFeedbackMsg] = useState(null);
  const inputRef = useRef(null);

  // Telón de apertura ágil "> Welcome" (~420ms solo en la primera visita limpia)
  useEffect(() => {
    if (!isBooting) return;
    const t = setTimeout(() => {
      hasPlayedInitialBoot = true;
      try {
        window.sessionStorage.setItem('ac_boot_done', '1');
      } catch {
        // Ignore storage restrictions
      }
      setIsBooting(false);
    }, 420);
    return () => clearTimeout(t);
  }, [isBooting]);

  useEffect(() => {
    if (!isBooting) {
      inputRef.current?.focus();
    }
  }, [isBooting]);

  const executeBulletAction = (item) => {
    if (!item) return;
    if (item.actionType === 'section') {
      onSelectSection(item.target);
    } else if (item.actionType === 'chat') {
      if (onToggleChat) onToggleChat();
    } else if (item.actionType === 'socials') {
      if (onOpenExternal) onOpenExternal('gh');
    } else if (item.actionType === 'prefs') {
      if (onToggleLang) onToggleLang();
    }
  };

  useEffect(() => {
    if (isBooting) {
      const skipKey = (e) => {
        if (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ') {
          hasPlayedInitialBoot = true;
          setIsBooting(false);
        }
      };
      window.addEventListener('keydown', skipKey);
      return () => window.removeEventListener('keydown', skipKey);
    }

    const handleKeyDown = (e) => {
      const activeEl = document.activeElement;
      const isCmdInput = activeEl === inputRef.current;
      const tag = activeEl?.tagName?.toLowerCase();

      if ((tag === 'input' || tag === 'textarea') && !isCmdInput) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;

      if (e.key === '?' && !cmdInput) {
        e.preventDefault();
        setIsCommandsOpen((prev) => !prev);
        return;
      }

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (!isCommandsOpen) {
          setIsCommandsOpen(true);
        } else {
          setSelectedIdx((prev) => (prev + 1) % TERMINAL_BULLETS.length);
        }
        return;
      }

      if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (!isCommandsOpen) {
          setIsCommandsOpen(true);
        } else {
          setSelectedIdx((prev) => (prev - 1 + TERMINAL_BULLETS.length) % TERMINAL_BULLETS.length);
        }
        return;
      }

      if (e.key === 'Escape') {
        if (cmdInput || feedbackMsg) {
          setCmdInput('');
          setFeedbackMsg(null);
        } else if (isCommandsOpen) {
          setIsCommandsOpen(false);
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isBooting, isCommandsOpen, cmdInput, feedbackMsg]);

  const handlePromptSubmit = (e) => {
    e.preventDefault();
    const raw = cmdInput.trim().toLowerCase().replace(/^\//, '');
    setFeedbackMsg(null);

    if (!raw) {
      if (isCommandsOpen) {
        executeBulletAction(TERMINAL_BULLETS[selectedIdx]);
      } else {
        setIsCommandsOpen(true);
      }
      return;
    }

    if (
      raw === '?' ||
      raw === 'h' ||
      raw === 'help' ||
      raw === 'ayuda' ||
      raw === 'comandos' ||
      raw === 'commands'
    ) {
      setCmdInput('');
      setIsCommandsOpen((prev) => !prev);
      return;
    }

    if (raw === '1' || raw.startsWith('proy') || raw.startsWith('proj') || raw.includes('quant')) {
      setCmdInput('');
      onSelectSection('playground');
      return;
    }
    if (raw === '2' || raw.startsWith('ana') || raw.startsWith('res') || raw.includes('macro')) {
      setCmdInput('');
      onSelectSection('research');
      return;
    }
    if (raw === '3' || raw.includes('cv') || raw.includes('rec') || raw === 'my-cv') {
      setCmdInput('');
      onSelectSection('timeline');
      return;
    }
    if (raw === 'c' || raw === 'chat') {
      setCmdInput('');
      if (onToggleChat) onToggleChat();
      return;
    }
    if (raw === 'gh' || raw === 'github') {
      setCmdInput('');
      if (onOpenExternal) onOpenExternal('gh');
      return;
    }
    if (raw === 'li' || raw === 'linkedin') {
      setCmdInput('');
      if (onOpenExternal) onOpenExternal('li');
      return;
    }
    if (raw === 'gm' || raw === 'gmail' || raw === 'mail' || raw === 'email') {
      setCmdInput('');
      if (onOpenExternal) onOpenExternal('gm');
      return;
    }
    if (raw === 'l' || raw === 'idioma' || raw === 'lang' || raw === 'language') {
      setCmdInput('');
      if (onToggleLang) onToggleLang();
      return;
    }
    if (raw === 't' || raw === 'tema' || raw === 'theme') {
      setCmdInput('');
      if (onToggleTheme) onToggleTheme();
      return;
    }
    if (raw === 'clear' || raw === 'cls') {
      setCmdInput('');
      setFeedbackMsg(null);
      return;
    }

    setFeedbackMsg(
      `${tx('Comando no reconocido:', 'Unrecognized command:', lang)} "${raw}". ${tx('Probá: 1, 2, 3, c, gh, li, gm, l o t.', 'Try: 1, 2, 3, c, gh, li, gm, l or t.', lang)}`
    );
    setCmdInput('');
  };

  return (
    <>
      {isBooting && (
        <div
          className="hc-boot-curtain"
          onClick={() => {
            hasPlayedInitialBoot = true;
            setIsBooting(false);
          }}
          title={tx('Hacé clic o presioná Esc para saltar', 'Click or press Esc to skip', lang)}
        >
          <div className="hc-boot-cli-only is-large">
            <span className="hc-cli-prompt">&gt;</span>
            <span className="hc-cli-typewriter chars-7">Welcome</span>
            <span className="hc-term-cursor" />
          </div>
        </div>
      )}

      <div className="hc-root">
        <div
          className="hc-stage"
          onClick={(e) => {
            if (e.target.tagName.toLowerCase() !== 'button') {
              inputRef.current?.focus();
            }
          }}
          role="region"
          aria-label={tx(
            'Terminal de bienvenida y navegación por teclado',
            'Welcome terminal and keyboard navigation',
            lang
          )}
        >
          <div className="hc-welcome-terminal term-type-03-claude">
            {/* 1. SALUDO + AGRADECIMIENTO + QUÉ TE PODÉS ENCONTRAR */}
            <div className="hc-wt-intro">
              <p className="hc-wt-greeting">
                <strong>
                  {tx('Hola, gracias por visitar mi página.', 'Hi, thanks for visiting my website.', lang)}
                </strong>{' '}
                {tx(
                  'Acá vas a encontrar las aplicaciones que construyo, mis análisis económicos con datos reales y mi recorrido profesional.',
                  'Here you will find the applications I build, my empirical economic analyses, and my professional background.',
                  lang
                )}
              </p>
              <p className="hc-wt-sub">
                {tx('Si querés, podés navegar todo el sitio', 'If you like, you can navigate the entire site', lang)}{' '}
                <strong>{tx('100% con tu teclado', '100% with your keyboard', lang)}</strong>{' '}
                {tx(
                  '(escribiendo el comando o tocando la tecla directa):',
                  '(by typing a command or pressing the direct key):',
                  lang
                )}
              </p>
            </div>

            {/* 2. DESPLEGABLE DE COMANDOS EN VIÑETAS CON GUÍA LATERAL AI CLI */}
            <div className={`hc-wt-commands-drawer ${isCommandsOpen ? 'is-open' : ''}`}>
              <button
                type="button"
                className={`hc-wt-cmd-toggle ${isCommandsOpen ? 'is-open' : ''}`}
                onClick={() => setIsCommandsOpen((prev) => !prev)}
                aria-expanded={isCommandsOpen}
              >
                <span className="hc-wt-toggle-left">
                  <span className="hc-wt-toggle-chevron" aria-hidden="true">
                    {isCommandsOpen ? '▾' : '▸'}
                  </span>
                  <span className="hc-wt-toggle-label">
                    {isCommandsOpen
                      ? tx('Ocultar comandos', 'Hide commands', lang)
                      : tx('Ver comandos disponibles', 'Show available commands', lang)}
                  </span>
                  {!isCommandsOpen && (
                    <span className="hc-wt-toggle-summary" aria-hidden="true">
                      1 · 2 · 3 · c · gh · li · gm · l · t
                    </span>
                  )}
                </span>
                <span className="hc-wt-toggle-kbd">[?]</span>
              </button>

              {isCommandsOpen && (
                <ul className="hc-wt-bullets">
                  {TERMINAL_BULLETS.map((b, idx) => {
                    const isSelected = selectedIdx === idx;
                    return (
                      <li
                        key={b.id}
                        className={`hc-wt-bullet-row ${isSelected ? 'is-active' : ''}`}
                        onMouseEnter={() => setSelectedIdx(idx)}
                      >
                        <span className="hc-wt-dot" aria-hidden="true">
                          {isSelected ? '❯' : '•'}
                        </span>

                        {b.id === 'socials' ? (
                          <div className="hc-wt-bullet-content">
                            <span className="hc-wt-code-group">
                              <button
                                type="button"
                                className="hc-wt-inline-cmd"
                                onClick={() => onOpenExternal && onOpenExternal('gh')}
                              >
                                gh
                              </button>
                              <i>·</i>
                              <button
                                type="button"
                                className="hc-wt-inline-cmd"
                                onClick={() => onOpenExternal && onOpenExternal('li')}
                              >
                                li
                              </button>
                              <i>·</i>
                              <button
                                type="button"
                                className="hc-wt-inline-cmd"
                                onClick={() => onOpenExternal && onOpenExternal('gm')}
                              >
                                gm
                              </button>
                            </span>
                            <span className="hc-wt-sep">—</span>
                            <span className="hc-wt-desc">
                              {tx('Ir directo a mi', 'Go directly to my', lang)}{' '}
                              <button
                                type="button"
                                className="hc-wt-text-link"
                                onClick={() => onOpenExternal && onOpenExternal('gh')}
                              >
                                GitHub
                              </button>
                              ,{' '}
                              <button
                                type="button"
                                className="hc-wt-text-link"
                                onClick={() => onOpenExternal && onOpenExternal('li')}
                              >
                                LinkedIn
                              </button>{' '}
                              {tx('o enviarme un', 'or send me a', lang)}{' '}
                              <button
                                type="button"
                                className="hc-wt-text-link"
                                onClick={() => onOpenExternal && onOpenExternal('gm')}
                              >
                                Gmail
                              </button>
                              .
                            </span>
                          </div>
                        ) : b.id === 'prefs' ? (
                          <div className="hc-wt-bullet-content">
                            <span className="hc-wt-code-group">
                              <button
                                type="button"
                                className="hc-wt-inline-cmd"
                                onClick={() => onToggleLang && onToggleLang()}
                              >
                                {tx('[l] idioma', '[l] language', lang)}
                              </button>
                              <i>·</i>
                              <button
                                type="button"
                                className="hc-wt-inline-cmd"
                                onClick={() => onToggleTheme && onToggleTheme()}
                              >
                                {tx('[t] tema', '[t] theme', lang)}
                              </button>
                            </span>
                            <span className="hc-wt-sep">—</span>
                            <span className="hc-wt-desc">{tx(b.descEs, b.descEn, lang)}</span>
                          </div>
                        ) : (
                          <button
                            type="button"
                            className="hc-wt-bullet-btn"
                            onClick={() => executeBulletAction(b)}
                          >
                            <span className="hc-wt-code">{tx(b.codeEs, b.codeEn, lang)}</span>
                            <span className="hc-wt-sep">—</span>
                            <span className="hc-wt-desc">{tx(b.descEs, b.descEn, lang)}</span>
                          </button>
                        )}
                      </li>
                    );
                  })}
                </ul>
              )}
            </div>

            {/* 3. BARRA DE ENTRADA AI CLI MODERNA ABAJO */}
            <form className="hc-b-form" onSubmit={handlePromptSubmit}>
              <span className="hc-p-claude">&gt;</span>
              <div className="hc-b-input-wrap">
                <input
                  ref={inputRef}
                  type="text"
                  value={cmdInput}
                  onChange={(e) => {
                    setCmdInput(e.target.value);
                    if (feedbackMsg) setFeedbackMsg(null);
                  }}
                  className="hc-term-b-input"
                  placeholder={tx(
                    'escribí un comando (1, 2, 3, c, gh, li, gm, l, t) o presioná la tecla directa...',
                    'type a command (1, 2, 3, c, gh, li, gm, l, t) or press the direct key...',
                    lang
                  )}
                  aria-label={tx('Comando de terminal', 'Terminal command', lang)}
                  autoComplete="off"
                  spellCheck="false"
                />
              </div>
              <span className="hc-prompt-enter-tag">↵ Enter</span>
            </form>

            {feedbackMsg && <div className="hc-wt-feedback">{feedbackMsg}</div>}
          </div>
        </div>
      </div>
    </>
  );
}
