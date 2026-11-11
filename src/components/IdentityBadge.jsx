import React, { useState, useEffect, useRef } from 'react';
import { tx, useSiteLocale } from '../i18n/localeService';

const SYSTEM_PROMPT_GUARDRAIL = `Sos el asistente personal integrado en la web de Alejandro Camerlengo.
REGLA ESTRICTA E INQUEBRANTABLE:
Solo podés responder preguntas sobre lo que hay en esta aplicación web y el CV de Alejandro, estructurados en 3 secciones principales:
1. Proyectos (#proyectos):
   - Proyecto Insignia: QuantLambda (quantlambda.dev), plataforma financiera cuantitativa, optimización de carteras, RAG vectorial y comité multi-agente en GCP.
   - Exploradores interactivos: Spark Learning (spark.alejandrocamerlengo.com), World Map Explorer (worldmap.alejandrocamerlengo.com) y Global Quality of Life Explorer (explorer.alejandrocamerlengo.com).
2. Análisis (#analisis):
   - Investigación propia: Macroeconomía, Gasto Público y Degradación del Mercado Laboral en Argentina (macro.alejandrocamerlengo.com), con series oficiales automatizadas y proyección SARIMAX.
3. Mi CV (#mi-cv):
   - Trayectoria 2011–2026: Negocios, Economía y Finanzas Cuantitativas (UNLZ, UBA Finanzas, UCEMA; Best Day, Portfolio Manager, Balanz), Ciencia de Datos (UBA Data Science; Lumen, AB InBev) e Ingeniería de Datos (Siemens Advanta y actualmente Data Engineer en Tongo, Suiza). Incluye descarga directa del CV en PDF.
Respondé en el idioma en que esté la consulta o el sitio, breve (2-3 oraciones).`;

/**
 * Renderiza texto con soporte limpio para **negritas** y `código` sin mostrar asteriscos crudos.
 */
function renderFormattedText(text) {
  if (!text) return null;
  const paragraphs = String(text).split('\n');
  return paragraphs.map((line, pIdx) => {
    const tokens = line.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
    return (
      <p key={pIdx} className="vchat-text">
        {tokens.map((tok, i) => {
          if (tok.startsWith('**') && tok.endsWith('**') && tok.length > 4) {
            return <strong key={i}>{tok.slice(2, -2)}</strong>;
          }
          if (tok.startsWith('`') && tok.endsWith('`') && tok.length > 2) {
            return (
              <code key={i} className="vchat-inline-code">
                {tok.slice(1, -1)}
              </code>
            );
          }
          return tok;
        })}
      </p>
    );
  });
}

function getLocalScopedReplyObject(userText, lang = 'ES') {
  const q = userText.toLowerCase();

  // 1. Stack técnico / herramientas / tecnologías
  if (
    q.includes('stack') ||
    q.includes('tecnolog') ||
    q.includes('tech') ||
    q.includes('herramienta') ||
    q.includes('tools') ||
    q.includes('skills') ||
    q.includes('lenguaje') ||
    q.includes('python') ||
    q.includes('sql') ||
    q.includes('kafka') ||
    q.includes('airflow') ||
    q.includes('bigquery') ||
    q.includes('dbt') ||
    q.includes('terraform') ||
    q.includes('cloud') ||
    q.includes('gcp') ||
    q.includes('aws')
  ) {
    return {
      text: tx(
        'Su stack principal combina **Data Engineering & Streaming** (`Python`, `SQL`, `Apache Spark`, `Kafka`, `Airflow`, `dbt`, `Polars`), **Cloud & IaC** (`GCP BigQuery`, `Cloud Run`, `AWS`, `Docker`, `Terraform`) y **AI / Sistemas Cuantitativos** (`RAG híbrido`, `Qdrant`, `pgvector`, `LangGraph`, `SARIMAX`, `CVaR/HRP`, `FastAPI`).',
        'His core stack combines **Data Engineering & Streaming** (`Python`, `SQL`, `Apache Spark`, `Kafka`, `Airflow`, `dbt`, `Polars`), **Cloud & IaC** (`GCP BigQuery`, `Cloud Run`, `AWS`, `Docker`, `Terraform`), and **AI / Quantitative Systems** (`Hybrid RAG`, `Qdrant`, `pgvector`, `LangGraph`, `SARIMAX`, `CVaR/HRP`, `FastAPI`).',
        lang
      ),
      actions: [
        {
          type: 'section',
          target: 'playground',
          label: tx('Ver Proyectos →', 'View Projects →', lang)
        },
        {
          type: 'section',
          target: 'timeline',
          label: tx('Ver Mi CV →', 'View My CV →', lang)
        }
      ]
    };
  }

  // 2. Experiencia actual (Tongo / Siemens / AB InBev) o CV general
  if (
    q.includes('tongo') ||
    q.includes('siemens') ||
    q.includes('abinbev') ||
    q.includes('ab inbev') ||
    q.includes('lumen') ||
    q.includes('balanz') ||
    q.includes('trabajo') ||
    q.includes('empresa') ||
    q.includes('actual') ||
    q.includes('suiza') ||
    q.includes('switzerland') ||
    q.includes('recorrido') ||
    q.includes('trayectoria') ||
    q.includes('experiencia') ||
    q.includes('experience') ||
    q.includes('career') ||
    q.includes('background') ||
    q.includes('cv') ||
    q.includes('resume') ||
    q.includes('pdf')
  ) {
    return {
      text: tx(
        'Actualmente es **Data Engineer en Tongo** (Suiza), tras desempeñarse como Data Engineer Global en **Siemens Advanta**, Data Scientist Global en **AB InBev** y **Lumen**, y en Finanzas Cuantitativas en **Balanz Capital**. En **Mi CV** podés recorrer el grafo completo (2011–2026) o descargar el PDF directo.',
        'He is currently a **Data Engineer at Tongo** (Switzerland), following global roles as a Data Engineer at **Siemens Advanta**, Global Data Scientist at **AB InBev** and **Lumen**, and Quantitative Finance roles at **Balanz Capital**. In **My CV** you can explore the full 2011–2026 timeline or download the PDF.',
        lang
      ),
      actions: [
        {
          type: 'section',
          target: 'timeline',
          label: tx('Abrir Mi CV →', 'Open My CV →', lang)
        },
        {
          type: 'download',
          href: '/Alejandro_Camerlengo_Data_Engineer.pdf',
          label: tx('Descargar CV (PDF) ↓', 'Download CV (PDF) ↓', lang)
        }
      ]
    };
  }

  // 3. Educación / Posgrados / Finanzas / Universidades
  if (
    q.includes('educación') ||
    q.includes('educacion') ||
    q.includes('education') ||
    q.includes('estudio') ||
    q.includes('posgrado') ||
    q.includes('maestr') ||
    q.includes('master') ||
    q.includes('degree') ||
    q.includes('universidad') ||
    q.includes('uba') ||
    q.includes('ucema') ||
    q.includes('unlz') ||
    q.includes('finanzas') ||
    q.includes('finance')
  ) {
    return {
      text: tx(
        'Cuenta con **3 posgrados** sobre su Licenciatura en Administración (UNLZ): **Maestría en Finanzas** (UBA), **Posgrado en finanzas cuantitativas** (UCEMA) y **Especialización en Ciencia de Datos y Estadística** (UBA). Podés ver el detalle de materias y tesis haciendo clic en el eje derecho de **Mi CV**.',
        'He holds **3 graduate degrees** building on his B.Sc. in Business & Economics (UNLZ): **M.Sc. in Finance** (UBA), **Graduate Program in Quantitative Finance** (UCEMA), and **Postgraduate Specialization in Data Science & Statistics** (UBA). You can inspect every curriculum on the right axis of **My CV**.',
        lang
      ),
      actions: [
        {
          type: 'section',
          target: 'timeline',
          label: tx('Ver Formación en Mi CV →', 'View Education in My CV →', lang)
        }
      ]
    };
  }

  // 4. QuantLambda / Proyecto Insignia
  if (
    q.includes('quantlambda') ||
    q.includes('insignia') ||
    q.includes('flagship') ||
    q.includes('estrella') ||
    q.includes('quant') ||
    q.includes('mercado') ||
    q.includes('market') ||
    q.includes('cartera') ||
    q.includes('portfolio') ||
    q.includes('agente') ||
    q.includes('agent')
  ) {
    return {
      text: tx(
        '**QuantLambda** (`quantlambda.dev`) es su plataforma insignia en producción: integra **13 microservicios en GCP** (`P-01` a `P-11`), monitoreo de regímenes macro, optimización de carteras (`CVaR` / `HRP`), RAG híbrido sobre reportes de la SEC y un **comité de 6 agentes de IA** con veto de riesgo.',
        '**QuantLambda** (`quantlambda.dev`) is his flagship production platform: integrating **13 GCP microservices** (`P-01` to `P-11`), macro regime telemetry, portfolio optimization (`CVaR` / `HRP`), hybrid RAG over SEC filings, and a **6-agent AI investment committee** with deterministic risk veto.',
        lang
      ),
      actions: [
        {
          type: 'section',
          target: 'playground',
          label: tx('Ver en Proyectos →', 'View in Projects →', lang)
        },
        {
          type: 'external',
          href: 'https://quantlambda.dev',
          label: 'quantlambda.dev ↗'
        }
      ]
    };
  }

  // 5. Análisis Macroeconómico Argentina
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
    q.includes('argentina') ||
    q.includes('sarimax')
  ) {
    return {
      text: tx(
        'En **Análisis** (`#analisis`) encontrás el estudio *Macroeconomía, Gasto Público y Degradación del Empleo en Argentina (1980–Presente)*: concilia **7 fuentes oficiales** mediante un pipeline mensual automatizado, con **5 gráficos interactivos nativos** y proyecciones econométricas `SARIMAX`.',
        'In **Research** (`#analisis`) you can read *Macroeconomics, Public Spending & Labor Quality Degradation in Argentina (1980–Present)*: reconciling **7 official statistical sources** via an automated monthly pipeline, with **5 interactive native charts** and `SARIMAX` econometric forecasts.',
        lang
      ),
      actions: [
        {
          type: 'section',
          target: 'research',
          label: tx('Abrir Análisis Macro →', 'Open Macro Research →', lang)
        }
      ]
    };
  }

  // 6. Exploradores / Spark / World Map / Quality of Life
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
    q.includes('calidad de vida') ||
    q.includes('explorer')
  ) {
    return {
      text: tx(
        'En **Proyectos** (`#proyectos`), debajo de **QuantLambda**, tenés **3 aplicaciones interactivas** listas para usar en el navegador: **Spark Learning** (arquitectura de Apache Spark 3.5), **World Map Explorer** (cartografía interactiva) y **Quality of Life Explorer** (44 indicadores en 240 países).',
        'In **Projects** (`#proyectos`), right below **QuantLambda**, you have **3 interactive web applications**: **Spark Learning** (Apache Spark 3.5 decision graph), **World Map Explorer** (custom cartography), and **Quality of Life Explorer** (44 indicators across 240 countries).',
        lang
      ),
      actions: [
        {
          type: 'section',
          target: 'playground',
          label: tx('Explorar Proyectos →', 'Explore Projects →', lang)
        }
      ]
    };
  }

  // 7. Atajos de teclado y navegación
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
    return {
      text: tx(
        'Podés navegar todo el sitio **100% con el teclado**: `1` abre **Proyectos**, `2` **Análisis**, `3` **Mi CV** (adentro `d` descarga el PDF), `c` abre/cierra este chat, `gh`/`li`/`gm` abren GitHub, LinkedIn o Gmail, `l` abre los **56 idiomas** y `t` cambia entre Modo Oscuro y Claro.',
        'You can navigate the entire site **100% by keyboard**: `1` opens **Projects**, `2` **Research**, `3` **My CV** (inside, `d` downloads the PDF), `c` toggles this chat, `gh`/`li`/`gm` open GitHub, LinkedIn, or Gmail, `l` opens the **56-language modal**, and `t` switches Dark/Light mode.',
        lang
      ),
      actions: []
    };
  }

  // 8. Contacto directo
  if (
    q.includes('contacto') ||
    q.includes('contact') ||
    q.includes('mail') ||
    q.includes('email') ||
    q.includes('linkedin') ||
    q.includes('github') ||
    q.includes('hablar') ||
    q.includes('reach')
  ) {
    return {
      text: tx(
        'Podés contactar a Alejandro directamente por **LinkedIn**, **GitHub** o **Email** (`alejandrocamerlengo@gmail.com`) con los botones de acá abajo:',
        'You can reach Alejandro directly via **LinkedIn**, **GitHub**, or **Email** (`alejandrocamerlengo@gmail.com`) using the buttons below:',
        lang
      ),
      actions: [
        {
          type: 'external',
          href: 'https://www.linkedin.com/in/alejandro-camerlengo-1ab3981b/',
          label: 'LinkedIn ↗'
        },
        {
          type: 'external',
          href: 'https://github.com/ale-camer',
          label: 'GitHub ↗'
        },
        {
          type: 'external',
          href: 'mailto:alejandrocamerlengo@gmail.com',
          label: 'Email ↗'
        }
      ]
    };
  }

  // 9. Resumen general de la web / saludo
  return {
    text: tx(
      'Podés preguntarme sobre cualquiera de las 3 áreas de la web o tocar una opción directa:\n• **Proyectos:** `QuantLambda` + 3 apps interactivas (*Spark*, *World Map*, *QoL Explorer*).\n• **Análisis:** Estudio macroeconómico y laboral de Argentina.\n• **Mi CV:** Experiencia (Tongo, Siemens, AB InBev, Balanz), posgrados y **CV en PDF**.',
      'You can ask me about any of the 3 areas of the site or pick a direct shortcut:\n• **Projects:** `QuantLambda` + 3 interactive apps (*Spark*, *World Map*, *QoL Explorer*).\n• **Research:** Argentine macroeconomic & labor market study.\n• **My CV:** Experience (Tongo, Siemens, AB InBev, Balanz), graduate degrees, and **PDF CV**.',
      lang
    ),
    actions: [
      {
        type: 'section',
        target: 'playground',
        label: tx('1 · Proyectos →', '1 · Projects →', lang)
      },
      {
        type: 'section',
        target: 'research',
        label: tx('2 · Análisis →', '2 · Research →', lang)
      },
      {
        type: 'section',
        target: 'timeline',
        label: tx('3 · Mi CV →', '3 · My CV →', lang)
      }
    ]
  };
}

async function askScopedAssistant(userText, lang) {
  const proxyEndpoint = import.meta.env.VITE_CHAT_API_URL;
  if (!proxyEndpoint) {
    await new Promise((r) => setTimeout(r, 240));
    return getLocalScopedReplyObject(userText, lang);
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
    if (!res.ok) return getLocalScopedReplyObject(userText, lang);
    const data = await res.json();
    const replyText = data?.reply || data?.text;
    if (replyText) {
      return { text: replyText, actions: [] };
    }
    return getLocalScopedReplyObject(userText, lang);
  } catch {
    return getLocalScopedReplyObject(userText, lang);
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
  onDrawerChange,
  onSelectSection
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

  const quickPrompts = [
    {
      id: 'quantlambda',
      label: tx('🚀 QuantLambda', '🚀 QuantLambda', lang),
      query: tx('Contame sobre QuantLambda', 'Tell me about QuantLambda', lang)
    },
    {
      id: 'exp',
      label: tx('💼 Experiencia y CV', '💼 Experience & CV', lang),
      query: tx('Resumen de experiencia laboral y CV', 'Work experience and CV summary', lang)
    },
    {
      id: 'stack',
      label: tx('🛠️ Stack técnico', '🛠️ Tech stack', lang),
      query: tx('¿Cuál es su stack técnico?', 'What is his technical stack?', lang)
    },
    {
      id: 'macro',
      label: tx('📊 Análisis Macro', '📊 Macro Research', lang),
      query: tx('¿De qué trata el análisis macroeconómico?', 'What is the macroeconomic research about?', lang)
    },
    {
      id: 'edu',
      label: tx('🎓 Posgrados', '🎓 Graduate degrees', lang),
      query: tx('¿Qué posgrados y estudios tiene?', 'What graduate degrees does he hold?', lang)
    },
    {
      id: 'contact',
      label: tx('📬 Contacto', '📬 Contact', lang),
      query: tx('¿Cómo lo puedo contactar?', 'How can I contact him?', lang)
    }
  ];

  const welcomeMessage = {
    id: 'welcome',
    sender: 'ale',
    text: tx(
      '¡Buenas! Soy el asistente interactivo de la web de **Alejandro**. Tocá cualquiera de los temas de abajo o escribí tu consulta:',
      'Hi! I am the interactive assistant for **Alejandro’s** website. Tap any topic below or type your question:',
      lang
    ),
    actions: [
      {
        type: 'download',
        href: '/Alejandro_Camerlengo_Data_Engineer.pdf',
        label: tx('Descargar CV (PDF) ↓', 'Download CV (PDF) ↓', lang)
      }
    ]
  };

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
      { id: `u_${Date.now()}`, sender: 'user', text: trimmed, actions: [] }
    ]);
    setInputValue('');
    setIsTyping(true);

    const replyObj = await askScopedAssistant(trimmed, lang);

    setIsTyping(false);
    setMessages((prev) => [
      ...prev,
      {
        id: `a_${Date.now()}`,
        sender: 'ale',
        text: replyObj.text,
        actions: replyObj.actions || []
      }
    ]);
  };

  const handleSubmitForm = (e) => {
    e.preventDefault();
    handleSendQuestion(inputValue);
  };

  const handleActionClick = (act) => {
    if (act.type === 'section' && onSelectSection) {
      onSelectSection(act.target);
      if (window.innerWidth < 640) {
        setDrawerOpen(false);
      }
    }
  };

  const allMessages = [welcomeMessage, ...messages];

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
          {/* Barra superior del chat estilo WhatsApp / HUD */}
          <div className="vdrawer-topbar">
            <div className="vdrawer-topbar-left">
              <img
                src="/images/profile.jpg"
                alt="Alejandro"
                className="vdrawer-mini-avatar"
              />
              <div className="vdrawer-topbar-meta">
                <span className="vdrawer-topbar-name">Alejandro Camerlengo</span>
                <span className="vdrawer-topbar-status">
                  <i className="vdrawer-status-dot" />
                  {tx('Asistente interactivo · En línea', 'Interactive assistant · Online', lang)}
                </span>
              </div>
            </div>

            <div className="vdrawer-topbar-actions">
              {messages.length > 0 && (
                <button
                  type="button"
                  className="vdrawer-reset-btn"
                  onClick={() => setMessages([])}
                  title={tx('Limpiar conversación', 'Clear conversation', lang)}
                >
                  ↺
                </button>
              )}
              <button
                type="button"
                className="vdrawer-close-btn"
                onClick={() => setDrawerOpen(false)}
                title={tx('Cerrar chat (Esc)', 'Close chat (Esc)', lang)}
                aria-label={tx('Cerrar chat', 'Close chat', lang)}
              >
                ✕
              </button>
            </div>
          </div>

          <div className="vdrawer-messages-list">
            {allMessages.map((m) => (
              <div
                key={m.id}
                className={`vchat-bubble-row ${m.sender === 'user' ? 'from-user' : 'from-ale'}`}
              >
                <div className="vchat-bubble">
                  <div className="vchat-rich-body">{renderFormattedText(m.text)}</div>

                  {m.actions && m.actions.length > 0 && (
                    <div className="vchat-actions-row">
                      {m.actions.map((act, idx) =>
                        act.type === 'section' ? (
                          <button
                            key={idx}
                            type="button"
                            className="vchat-action-pill"
                            onClick={() => handleActionClick(act)}
                          >
                            {act.label}
                          </button>
                        ) : (
                          <a
                            key={idx}
                            href={act.href}
                            target={act.type === 'external' ? '_blank' : undefined}
                            rel={act.type === 'external' ? 'noopener noreferrer' : undefined}
                            download={act.type === 'download' ? 'Alejandro_Camerlengo_CV.pdf' : undefined}
                            className="vchat-action-pill"
                          >
                            {act.label}
                          </a>
                        )
                      )}
                    </div>
                  )}
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
            {/* Píldoras de sugerencias rápidas */}
            <div className="vdrawer-quick-chips" aria-label={tx('Preguntas rápidas', 'Quick questions', lang)}>
              {quickPrompts.map((chip) => (
                <button
                  key={chip.id}
                  type="button"
                  className="vdrawer-chip-btn"
                  disabled={isTyping}
                  onClick={() => handleSendQuestion(chip.query)}
                >
                  {chip.label}
                </button>
              ))}
            </div>

            {socialsInChat && (
              <div className="vdrawer-integrated-socials">
                <span>{tx('Contacto directo:', 'Direct contact:', lang)}</span>
                <div className="vdrawer-social-links">
                  <a
                    href="https://github.com/ale-camer"
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
                placeholder={tx('Escribí tu pregunta o tocá un tema...', 'Type a question or tap a topic...', lang)}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                maxLength={180}
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
