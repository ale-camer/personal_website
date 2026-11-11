import React, { useState, useEffect, useRef } from 'react';
import { tx, useSiteLocale } from '../i18n/localeService';

const SYSTEM_PROMPT_GUARDRAIL = `Sos el asistente personal integrado en la web de Alejandro Camerlengo.
REGLA ESTRICTA E INQUEBRANTABLE:
Solo podés responder preguntas sobre lo que hay en esta aplicación web y el CV de Alejandro, estructurados en 3 secciones principales:
1. Proyectos (#proyectos):
   - Proyecto Insignia: QuantLambda (quantlambda.dev), plataforma financiera cuantitativa, optimización de carteras, RAG vectorial (pgvector) y comité multi-agente en GCP.
   - Exploradores interactivos: Spark Learning (spark.alejandrocamerlengo.com), World Map Explorer (worldmap.alejandrocamerlengo.com) y Global Quality of Life Explorer (explorer.alejandrocamerlengo.com).
2. Análisis (#analisis):
   - Investigación propia: Macroeconomía, Gasto Público y Degradación del Mercado Laboral en Argentina (macro.alejandrocamerlengo.com), con series oficiales automatizadas y proyección SARIMAX.
3. Mi CV (#mi-cv):
   - Trayectoria 2011–2026: Negocios, Economía y Finanzas Corporativas/Cuantitativas (UNLZ, UBA Finanzas, UCEMA; Best Day Travel Group, Portfolio Manager, Balanz Capital), Ciencia de Datos (UBA Data Science; Lumen Technologies, AB InBev Global) e Ingeniería de Datos (Siemens Advanta Global y actualmente Data Engineer en Tongo). Incluye descarga directa del CV en PDF.
4. Navegación 100% por teclado: desde el Home o cualquier vista con teclas 1 (Proyectos), 2 (Análisis), 3 (Mi CV), c (Chat), gh (GitHub), li (LinkedIn), gm (Gmail), l (Idioma) y t (Tema Claro/Oscuro).
Si el usuario pregunta CUALQUIER COSA fuera de estos temas, debés rechazarlo amablemente en 1 oración indicando que este chat solo responde sobre el contenido de la web de Alejandro. Respondé en el idioma en que esté la consulta o el sitio, breve (2-3 oraciones).`;

function getLocalScopedResponse(userText, lang = 'ES') {
  const q = userText.toLowerCase();

  if (
    q.includes('web') ||
    q.includes('página') ||
    q.includes('pagina') ||
    q.includes('site') ||
    q.includes('page') ||
    q.includes('encontrar') ||
    q.includes('hay') ||
    q.includes('secciones') ||
    q.includes('sections') ||
    q.includes('contenido') ||
    q.includes('resumen') ||
    q.includes('summary')
  ) {
    return tx(
      'La web se organiza en 3 secciones: **Proyectos** (con **QuantLambda** como proyecto insignia arriba y 3 exploradores interactivos debajo), **Análisis** (ensayos propios con datos reales como Macroeconomía y Empleo en Argentina) y **Mi CV** (recorrido 2011–2026 + descarga en PDF). Además podés navegar todo 100% con teclado (`1`, `2`, `3`, `c`, `gh`, `li`, `gm`, `l`, `t`).',
      'The website is organized into 3 sections: **Projects** (with **QuantLambda** as the flagship platform at the top and 3 interactive explorers below), **Research** (empirical studies with primary data such as Macroeconomics & Employment in Argentina), and **My CV** (2011–2026 career timeline + PDF download). You can also navigate 100% by keyboard (`1`, `2`, `3`, `c`, `gh`, `li`, `gm`, `l`, `t`).',
      lang
    );
  }

  if (
    q.includes('teclado') ||
    q.includes('keyboard') ||
    q.includes('comando') ||
    q.includes('command') ||
    q.includes('atajo') ||
    q.includes('shortcut') ||
    q.includes('terminal') ||
    q.includes('navegar') ||
    q.includes('navigate')
  ) {
    return tx(
      'Podés moverte 100% con el teclado en toda la página: `1` abre **Proyectos**, `2` **Análisis**, `3` **Mi CV** (y adentro `D` descarga el PDF), `c` abre/cierra este chat, `gh`/`li`/`gm` van a GitHub, LinkedIn o Gmail, `l` cambia el idioma y `t` alterna entre Modo Oscuro y Claro.',
      'You can navigate the entire site 100% with your keyboard: `1` opens **Projects**, `2` **Research**, `3` **My CV** (and inside `D` downloads the PDF), `c` toggles this chat, `gh`/`li`/`gm` open GitHub, LinkedIn, or Gmail, `l` opens the 56-language selector, and `t` switches between Dark and Light mode.',
      lang
    );
  }

  if (
    q.includes('recorrido') ||
    q.includes('trayectoria') ||
    q.includes('experiencia') ||
    q.includes('experience') ||
    q.includes('career') ||
    q.includes('background') ||
    q.includes('quién') ||
    q.includes('quien') ||
    q.includes('who') ||
    q.includes('cv') ||
    q.includes('resume') ||
    q.includes('tongo') ||
    q.includes('siemens') ||
    q.includes('abinbev') ||
    q.includes('lumen') ||
    q.includes('balanz') ||
    q.includes('educación') ||
    q.includes('educacion') ||
    q.includes('education') ||
    q.includes('estudios') ||
    q.includes('pdf') ||
    q.includes('finanzas') ||
    q.includes('finance')
  ) {
    return tx(
      'En **Mi CV** (`#mi-cv`) ves su evolución de 2011 a 2026: arrancó en **Negocios y Finanzas Cuantitativas** (UNLZ, UBA Finanzas, UCEMA; Best Day, Portfolio Manager, Balanz), pasó a **Data Science** (UBA MSc Data Science; Lumen, AB InBev) y evolucionó a **Data Engineering** (Siemens Advanta y hoy en **Tongo**). Arriba a la derecha podés descargar el CV en PDF.',
      'In **My CV** (`#mi-cv`) you can explore his 2011–2026 progression: starting in **Business & Quantitative Finance** (UNLZ, UBA Finance, UCEMA; Best Day, Portfolio Manager, Balanz), moving into **Data Science** (UBA MSc Data Science; Lumen, AB InBev), and evolving into **Data Engineering** (Siemens Advanta and currently at **Tongo**). You can download the PDF CV at the top right.',
      lang
    );
  }

  if (
    q.includes('quantlambda') ||
    q.includes('insignia') ||
    q.includes('flagship') ||
    q.includes('estrella') ||
    q.includes('quant') ||
    q.includes('mercado') ||
    q.includes('market') ||
    q.includes('cartera') ||
    q.includes('portfolio')
  ) {
    return tx(
      '**QuantLambda** (`quantlambda.dev`) encabeza la pestaña **Proyectos** como su proyecto insignia: una plataforma financiera end-to-end que integra pipelines en GCP, análisis cuantitativo de carteras, búsqueda vectorial (`pgvector`) y un comité de agentes de IA.',
      '**QuantLambda** (`quantlambda.dev`) leads the **Projects** tab as his flagship platform: an end-to-end financial workstation combining GCP data pipelines, quantitative portfolio analytics, vector RAG (`pgvector`), and an AI agent committee.',
      lang
    );
  }

  if (
    q.includes('investigaciones') ||
    q.includes('análisis') ||
    q.includes('analisis') ||
    q.includes('research') ||
    q.includes('macro') ||
    q.includes('inflación') ||
    q.includes('inflacion') ||
    q.includes('inflation') ||
    q.includes('empleo') ||
    q.includes('employment') ||
    q.includes('argentina')
  ) {
    return tx(
      'En **Análisis** (`#analisis`) encontrás investigaciones propias con datos primarios, encabezadas por el estudio sobre *Macroeconomía, Gasto Público y Calidad del Empleo en Argentina*, con 5 visualizaciones interactivas actualizadas automáticamente y proyección econométrica SARIMAX.',
      'In **Research** (`#analisis`) you will find empirical studies built from primary sources, led by *Macroeconomics, Public Spending & Labor Quality Degradation in Argentina*, featuring 5 automatically updated interactive charts and SARIMAX econometric forecasts.',
      lang
    );
  }

  if (
    q.includes('playground') ||
    q.includes('jugar') ||
    q.includes('apps') ||
    q.includes('proyectos') ||
    q.includes('projects') ||
    q.includes('spark') ||
    q.includes('world') ||
    q.includes('mapa') ||
    q.includes('map') ||
    q.includes('quality') ||
    q.includes('calidad de vida')
  ) {
    return tx(
      'En **Proyectos** (`#proyectos`), además de **QuantLambda** arriba como proyecto principal, tenés 3 desarrollos interactivos desplegables para explorar en vivo: *Spark Learning*, *World Map Explorer* y *Global Quality of Life Explorer*.',
      'In **Projects** (`#proyectos`), right below **QuantLambda** as the flagship platform, you have 3 interactive exploratory apps ready to try live: *Spark Learning*, *World Map Explorer*, and *Global Quality of Life Explorer*.',
      lang
    );
  }

  if (
    q.includes('contacto') ||
    q.includes('contact') ||
    q.includes('mail') ||
    q.includes('email') ||
    q.includes('linkedin') ||
    q.includes('github')
  ) {
    return tx(
      'Podés contactarlo directo por **LinkedIn** (`li`), **GitHub** (`gh`) o **Email** (`gm` → `alejandrocamerlengo@gmail.com`) desde los íconos de abajo a la izquierda o escribiendo el comando en la terminal del Home.',
      'You can reach him directly via **LinkedIn** (`li`), **GitHub** (`gh`), or **Email** (`gm` → `alejandrocamerlengo@gmail.com`) using the bottom-left icons or by typing the command in the Home terminal.',
      lang
    );
  }

  return tx(
    '🔒 Este chat responde exclusivamente sobre lo que hay en la web (**Proyectos / QuantLambda**, **Análisis**, **Mi CV** y atajos de navegación). ¿Sobre cuál te gustaría consultar?',
    '🔒 This chat is strictly scoped to the content of this website (**Projects / QuantLambda**, **Research**, **My CV**, and keyboard shortcuts). Which one would you like to ask about?',
    lang
  );
}

/**
 * Resguardo de API Key: nunca se expone ninguna clave privada en el bundle del navegador.
 * Si se configura VITE_CHAT_API_URL (endpoint proxy serverless/Cloud Run propio), consulta al backend;
 * de lo contrario responde de forma determinística e instantánea con el motor local acotado.
 */
async function askScopedAssistant(userText, lang) {
  const proxyEndpoint = import.meta.env.VITE_CHAT_API_URL;
  if (!proxyEndpoint) {
    await new Promise((r) => setTimeout(r, 320));
    return getLocalScopedResponse(userText, lang);
  }

  try {
    const res = await fetch(proxyEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: userText,
        lang,
        systemInstruction: SYSTEM_PROMPT_GUARDRAIL
      })
    });
    if (!res.ok) return getLocalScopedResponse(userText, lang);
    const data = await res.json();
    return data?.reply || data?.text || getLocalScopedResponse(userText, lang);
  } catch {
    return getLocalScopedResponse(userText, lang);
  }
}

export default function IdentityBadge({
  accentHex = '#25D366',
  accentTextColor = '#06140c',
  chatAttached = false,
  socialsInChat = false,
  colorMode = 'dark',
  lang = 'ES',
  drawerAlign = 'left',
  externalOpen,
  onDrawerChange
}) {
  useSiteLocale(lang);
  const [internalOpen, setInternalOpen] = useState(false);
  const drawerOpen = externalOpen !== undefined ? externalOpen : internalOpen;

  const setDrawerOpen = (val) => {
    const next = typeof val === 'function' ? val(drawerOpen) : val;
    setInternalOpen(next);
    if (onDrawerChange) onDrawerChange(next);
  };

  const [hasUnseen, setHasUnseen] = useState(true);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const drawerRef = useRef(null);
  const messagesEndRef = useRef(null);

  const welcomeMessage = tx(
    '¡Buenas! Espero que te resulte interesante mi contenido y estemos en contacto. ¿Qué te gustaría saber al respecto?',
    'Hi there! I hope you find my work interesting and that we stay in touch. What would you like to know about it?',
    lang
  );

  useEffect(() => {
    if (!drawerOpen) return;
    setHasUnseen(false);
    const handleKey = (e) => {
      if (e.key === 'Escape') {
        e.stopPropagation();
        setDrawerOpen(false);
      }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [drawerOpen]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  useEffect(() => {
    if (!drawerOpen) return;

    const handleMouseDownOutside = (e) => {
      if (drawerRef.current && !drawerRef.current.contains(e.target)) {
        setDrawerOpen(false);
      }
    };

    document.addEventListener('mousedown', handleMouseDownOutside);
    return () => {
      document.removeEventListener('mousedown', handleMouseDownOutside);
    };
  }, [drawerOpen]);

  const handleOpenChat = () => {
    if (!drawerOpen) {
      setDrawerOpen(true);
      setHasUnseen(false);
    }
  };

  const handleSendQuestion = async (questionText) => {
    const trimmed = questionText.trim();
    if (!trimmed || isTyping) return;

    setMessages((prev) => [
      ...prev,
      { id: `u_${Date.now()}`, sender: 'user', text: trimmed }
    ]);
    setInputValue('');
    setIsTyping(true);

    const replyText = await askScopedAssistant(trimmed, lang);

    setIsTyping(false);
    setMessages((prev) => [
      ...prev,
      { id: `a_${Date.now()}`, sender: 'ale', text: replyText }
    ]);
  };

  const handleSubmitForm = (e) => {
    e.preventDefault();
    handleSendQuestion(inputValue);
  };

  const allMessages = [{ id: 'welcome', sender: 'ale', text: welcomeMessage }, ...messages];

  return (
    <div
      className={`chat-identity-root mode-${colorMode}`}
      style={{
        '--chat-online': accentHex,
        '--chat-online-text': accentTextColor
      }}
    >
      <div
        className={`chat-header-trigger ${drawerOpen ? 'is-open' : ''}`}
        onClick={handleOpenChat}
      >
        <div className="chat-avatar-box">
          <svg className="chat-status-ring" viewBox="0 0 56 56">
            {[0, 1, 2, 3].map((idx) => {
              const totalCirc = 157.08;
              const segLen = 33.5;
              const gapLen = totalCirc - segLen;
              const rot = -90 + idx * 90 + 4;
              return (
                <circle
                  key={idx}
                  cx="28"
                  cy="28"
                  r="25"
                  fill="none"
                  stroke={accentHex}
                  strokeWidth="2.3"
                  strokeLinecap="round"
                  strokeDasharray={`${segLen} ${gapLen}`}
                  transform={`rotate(${rot} 28 28)`}
                  className="status-ring-seg"
                />
              );
            })}
          </svg>

          <img
            src="/images/profile.jpg"
            alt="Alejandro Camerlengo"
            className="chat-avatar-photo"
          />

          <span
            className={`unseen-status-dot ${hasUnseen ? 'is-unseen' : 'is-seen'} expand-on-hover`}
          >
            <span className="dot-hover-text">{tx('abrir chat', 'open chat', lang)}</span>
          </span>
        </div>

        <div className="name-and-callouts-wrap">
          <div className="name-line-row">
            <span className="name-m3-orbitron">Alejandro Camerlengo</span>
          </div>
        </div>
      </div>

      {drawerOpen && (
        <aside
          ref={drawerRef}
          className={`vertical-chat-drawer align-${drawerAlign} ${chatAttached ? 'attached-to-island' : ''}`}
        >
          <button
            className="vdrawer-floating-close"
            onClick={() => setDrawerOpen(false)}
            title={tx('Cerrar chat', 'Close chat', lang)}
            aria-label={tx('Cerrar chat', 'Close chat', lang)}
          >
            ✕
          </button>

          <div className="vdrawer-messages-list">
            {allMessages.map((m) => (
              <div
                key={m.id}
                className={`vchat-bubble-row ${m.sender === 'user' ? 'from-user' : 'from-ale'}`}
              >
                <div className="vchat-bubble">
                  <p className="vchat-text">{m.text}</p>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="vchat-bubble-row from-ale">
                <div className="vchat-bubble typing-bubble">
                  <span className="typing-dots">
                    <i />
                    <i />
                    <i />
                  </span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="vdrawer-bottom-area">
            {socialsInChat && (
              <div className="vdrawer-integrated-socials">
                <span>{tx('Contacto directo:', 'Direct contact:', lang)}</span>
                <div className="vdrawer-social-links">
                  <a
                    href="https://github.com/ale-camer/personal_website"
                    target="_blank"
                    rel="noreferrer"
                  >
                    GitHub ↗
                  </a>
                  <a
                    href="https://www.linkedin.com/in/alejandro-camerlengo-1ab3981b/"
                    target="_blank"
                    rel="noreferrer"
                  >
                    LinkedIn ↗
                  </a>
                  <a href="mailto:alejandrocamerlengo@gmail.com">Email ↗</a>
                </div>
              </div>
            )}

            <form className="vdrawer-input-form" onSubmit={handleSubmitForm}>
              <input
                type="text"
                className="vdrawer-input"
                placeholder={tx('Escribí tu mensaje...', 'Type your message...', lang)}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                maxLength={180}
                autoFocus
              />
              <button
                type="submit"
                className="vdrawer-send-btn"
                disabled={!inputValue.trim() || isTyping}
                aria-label={tx('Enviar mensaje', 'Send message', lang)}
                title={tx('Enviar', 'Send', lang)}
              >
                <svg
                  viewBox="0 0 24 24"
                  width="16"
                  height="16"
                  fill="currentColor"
                  style={{ marginLeft: '2px' }}
                >
                  <path d="M1.101 21.757L23.8 12.028 1.101 2.3l.011 7.912 13.623 1.816-13.623 1.817-.011 7.912z" />
                </svg>
              </button>
            </form>
          </div>
        </aside>
      )}
    </div>
  );
}
