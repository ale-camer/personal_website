import React, { useState, useEffect, useRef } from 'react';

const SYSTEM_PROMPT_GUARDRAIL = `Sos el asistente personal integrado en la web de Alejandro Camerlengo.
REGLA ESTRICTA E INQUEBRANTABLE:
Solo podés responder preguntas sobre lo que hay en esta aplicación web y el recorrido de Alejandro:
1. Recorrido multidisciplinario (2011–2026): Negocios, Economía y Finanzas Corporativas/Cuantitativas (UNLZ, UBA, UCEMA; Best Day, Balanz), Ciencia de Datos (Lumen LATAM, AB InBev Global) e Ingeniería de Datos e IA End-to-End (Siemens Advanta Global y actualmente en Tongo).
2. 01. Proyecto Estrella (QuantLambda - quantlambda.dev).
3. 02. Investigaciones (Macroeconomía Argentina y Calidad del Empleo).
4. 03. Playground (Apache Spark, Calidad de Vida Global, Bitcoin y Geoespacial).
Si el usuario pregunta CUALQUIER COSA fuera de estos temas, debés rechazarlo amablemente en 1 oración indicando que este chat solo responde sobre el contenido de la web de Alejandro. Respondé en español rioplatense, breve (2-3 oraciones).`;

function getLocalScopedResponse(userText) {
  const q = userText.toLowerCase();

  if (
    q.includes('web') ||
    q.includes('página') ||
    q.includes('pagina') ||
    q.includes('encontrar') ||
    q.includes('hay') ||
    q.includes('secciones') ||
    q.includes('contenido')
  ) {
    return 'En la web tenés 4 espacios: **QuantLambda** (plataforma financiera E2E con IA), **Análisis** (investigaciones propias como Macroeconomía y Empleo en Argentina), **Proyectos** (apps interactivas de Spark, Geo, BTC y Calidad de Vida) y **Recorrido** (línea de tiempo 2011–2026).';
  }

  if (
    q.includes('recorrido') ||
    q.includes('trayectoria') ||
    q.includes('experiencia') ||
    q.includes('quién') ||
    q.includes('quien') ||
    q.includes('cv') ||
    q.includes('tongo') ||
    q.includes('finanzas')
  ) {
    return 'Ale cruza varias disciplinas sin encasillarse en una sola etiqueta: arrancó en **Negocios y Finanzas Cuantitativas** (Best Day, Balanz; UBA/UCEMA), pasó a **Data Science** modelando problemas reales (Lumen, AB InBev) y evolucionó a **Data & AI Engineering End-to-End** (Siemens Advanta y hoy en **Tongo**).';
  }

  if (q.includes('quantlambda') || q.includes('estrella') || q.includes('quant') || q.includes('mercado')) {
    return '**QuantLambda** (`quantlambda.dev`) es su proyecto insignia: una arquitectura financiera end-to-end que combina pipelines de datos en la nube, análisis cuantitativo, RAG vectorial (`pgvector`) y agentes de IA para inteligencia de mercado.';
  }

  if (
    q.includes('playground') ||
    q.includes('jugar') ||
    q.includes('apps') ||
    q.includes('proyectos') ||
    q.includes('spark') ||
    q.includes('investigaciones') ||
    q.includes('análisis') ||
    q.includes('analisis') ||
    q.includes('macro')
  ) {
    return 'En **Análisis** podés leer ensayos ad-hoc como el estudio sobre *Macroeconomía y Calidad del Empleo en Argentina*. Y en **Proyectos** tenés 4 apps listas para probar: *Apache Spark Encyclopedia*, *Calidad de Vida Global*, *Bitcoin Dashboard* y *Proyectos Geoespaciales*.';
  }

  return '🔒 Este chat está acotado exclusivamente a lo que hay en la web (Recorrido 2011–2026, QuantLambda, Análisis y Proyectos). ¿Sobre cuál te gustaría saber?';
}

async function askScopedGeminiFlash(userText) {
  const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
  if (!apiKey) {
    await new Promise((r) => setTimeout(r, 380));
    return getLocalScopedResponse(userText);
  }

  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          systemInstruction: { parts: [{ text: SYSTEM_PROMPT_GUARDRAIL }] },
          contents: [{ role: 'user', parts: [{ text: userText }] }],
          generationConfig: { maxOutputTokens: 160, temperature: 0.25 }
        })
      }
    );
    if (!res.ok) return getLocalScopedResponse(userText);
    const data = await res.json();
    return data?.candidates?.[0]?.content?.parts?.[0]?.text || getLocalScopedResponse(userText);
  } catch {
    return getLocalScopedResponse(userText);
  }
}

export default function IdentityBadge({
  accentHex = '#25D366',
  accentTextColor = '#06140c',
  chatAttached = false,
  socialsInChat = false,
  colorMode = 'dark',
  drawerAlign = 'left',
  onDrawerChange
}) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [hasUnseen, setHasUnseen] = useState(true);
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'ale',
      text: '¡Buenas! Espero que te resulte interesante mi contenido y estemos en contacto. ¿Qué te gustaría saber al respecto?'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const drawerRef = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (onDrawerChange) onDrawerChange(drawerOpen);
  }, [drawerOpen, onDrawerChange]);

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

    const replyText = await askScopedGeminiFlash(trimmed);

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
            <span className="dot-hover-text">open chat</span>
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
            title="Cerrar chat"
            aria-label="Cerrar chat"
          >
            ✕
          </button>

          <div className="vdrawer-messages-list">
            {messages.map((m) => (
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
                <span>Contacto directo:</span>
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
                placeholder="Escribí tu mensaje..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                maxLength={180}
                autoFocus
              />
              <button
                type="submit"
                className="vdrawer-send-btn"
                disabled={!inputValue.trim() || isTyping}
                aria-label="Enviar mensaje"
                title="Enviar"
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
