import React, { useState, useEffect, useRef } from 'react';
import { tx, useSiteLocale } from '../i18n/localeService';

const SYSTEM_PROMPT_GUARDRAIL = `Sos el asistente personal integrado en la web de Alejandro Camerlengo.
Podés saludar, conversar de forma amena, cálida y natural (en español rioplatense si te hablan en español, o en el idioma en que te escriban) y guiar al visitante por lo que hay en esta aplicación web:
1. Proyectos (#proyectos):
   - Proyecto Insignia: QuantLambda (quantlambda.dev), plataforma para seguir mercados globales en vivo, analizar activos y simular riesgo de carteras.
   - Otros desarrollos interactivos: Spark Learning (spark.alejandrocamerlengo.com), World Map (worldmap.alejandrocamerlengo.com) y Quality of Life Explorer (explorer.alejandrocamerlengo.com).
2. Análisis (#analisis):
   - Investigación propia: Macroeconomía, Gasto Público y Degradación del Mercado Laboral en Argentina (macro.alejandrocamerlengo.com), con datos oficiales automatizados y proyecciones SARIMAX.
3. Mi CV (#mi-cv):
   - Trayectoria 2011–2026: Negocios y Finanzas (UNLZ, UBA Finanzas, UCEMA; Best Day, Portfolio Manager, Balanz), Data Science (UBA Data Science; Lumen, AB InBev) y Data Engineering (Siemens Advanta y actualmente Data Engineer en Tongo). Incluye descarga directa del CV en PDF.
Respondé siempre con buena onda, conciso (2-4 oraciones) y sin compartir teléfono ni dirección personal.`;

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
  const q = userText.toLowerCase().trim();

  // 0. Saludos y charla casual ("hola", "buenas", "cómo estás", "qué tal", "hello", "hi", etc.)
  const isGreetingOnly =
    /^(hola|buenas|buen dia|buen día|buenas tardes|buenas noches|que tal|qué tal|como va|cómo va|como estas|cómo estás|como andas|cómo andás|todo bien|que onda|qué onda|hey|hi|hello|howdy|good morning|good afternoon|good evening|how are you|what's up|whats up|saludos)[!¡?¿.,\s]*$/i.test(
      q
    );

  if (isGreetingOnly) {
    return {
      text: tx(
        '¡Hola! 👋 ¿Cómo va? Qué bueno que pases por acá.\nEn la app tenés todo el trabajo de **Alejandro** organizado en 3 secciones para explorar a tu ritmo:\n• **Proyectos:** `QuantLambda` (su plataforma de mercados en vivo) + 3 apps interactivas (*Spark Learning*, *World Map* y *Quality of Life Explorer*).\n• **Análisis:** Su investigación sobre macroeconomía y empleo en Argentina.\n• **Mi CV:** Su recorrido profesional y académico (2011–2026) y el **CV en PDF**.\n¿Qué te gustaría ver primero?',
        'Hi there! 👋 How’s it going? Great to have you here.\nIn this app you have all of **Alejandro’s** work organized into 3 sections to explore at your own pace:\n• **Projects:** `QuantLambda` (his live market platform) + 3 interactive apps (*Spark Learning*, *World Map*, and *Quality of Life Explorer*).\n• **Research:** His macroeconomic and labor market study on Argentina.\n• **My CV:** His full career & academic timeline (2011–2026) plus the **PDF CV**.\nWhat would you like to check out first?',
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

  // 0b. Agradecimientos, elogios o cierre ameno ("gracias", "buenísimo", "genial", "chau", etc.)
  if (
    /^(gracias|muchas gracias|mil gracias|thanks|thank you|thx|genial|buenisimo|buenísimo|excelente|impecable|crack|muy bueno|cool|awesome|great|nice|ok|okey|dale|perfecto|de diez|chau|adios|adiós|nos vemos|bye|hasta luego)[!¡?¿.,\s]*$/i.test(
      q
    )
  ) {
    return {
      text: tx(
        '¡De nada, un placer! 🙌 Si tenés cualquier otra duda sobre los proyectos, el análisis macro o el recorrido de Alejandro, escribime acá mismo o usá los accesos directos:',
        'You’re very welcome! 🙌 If you have any other questions about the projects, macro research, or Alejandro’s background, just ask me here or use the quick links below:',
        lang
      ),
      actions: [
        {
          type: 'section',
          target: 'playground',
          label: tx('Ver Proyectos →', 'View Projects →', lang)
        },
        {
          type: 'download',
          href: '/Alejandro_Camerlengo_Data_Engineer.pdf',
          label: tx('Descargar CV (PDF) ↓', 'Download CV (PDF) ↓', lang)
        }
      ]
    };
  }

  // 0c. Quién sos / Quién es Alejandro / Contame de vos / Qué hay en la app
  if (
    q.includes('quien sos') ||
    q.includes('quién sos') ||
    q.includes('quien es') ||
    q.includes('quién es') ||
    q.includes('contame de vos') ||
    q.includes('contame sobre') ||
    q.includes('sobre alejandro') ||
    q.includes('who are you') ||
    q.includes('who is alejandro') ||
    q.includes('about you') ||
    q.includes('about alejandro') ||
    q.includes('que hay en la app') ||
    q.includes('qué hay en la app') ||
    q.includes('que hay en la web') ||
    q.includes('qué hay en la web') ||
    q.includes('que tenes') ||
    q.includes('qué tenés') ||
    q.includes('que puedo ver') ||
    q.includes('qué puedo ver')
  ) {
    return {
      text: tx(
        '¡Te cuento! Soy el asistente interactivo de la web de **Alejandro Camerlengo**.\nAlejandro es **Data Engineer** (con base en **Data Science** y **Finanzas Cuantitativas y Corporativas**). Acá en la app tenés:\n• **Proyectos:** `QuantLambda` (su proyecto insignia) + 3 exploradores interactivos.\n• **Análisis:** Su estudio econométrico sobre macroeconomía y empleo.\n• **Mi CV:** Su línea de tiempo interactiva (2011–2026) y el PDF descargable.',
        'Happy to share! I’m the interactive assistant for **Alejandro Camerlengo’s** website.\nAlejandro is a **Data Engineer** (with a strong background in **Data Science** and **Quantitative & Corporate Finance**). Here in the app you’ll find:\n• **Projects:** `QuantLambda` (his flagship platform) + 3 interactive explorers.\n• **Research:** His econometric study on macroeconomics and employment.\n• **My CV:** His interactive timeline (2011–2026) and downloadable PDF.',
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
    q.includes('snowflake') ||
    q.includes('databricks') ||
    q.includes('airflow') ||
    q.includes('bigquery') ||
    q.includes('dbt') ||
    q.includes('cloud') ||
    q.includes('gcp') ||
    q.includes('aws') ||
    q.includes('azure')
  ) {
    return {
      text: tx(
        'Su stack principal combina **Plataformas & Cloud** (`Snowflake`, `Databricks`, `Azure ADF/DevOps`, `AWS S3/EC2`, `GCP`), **Pipelines & Orquestación** (`Python`, `SQL`, `Apache Spark`, `dbt`, `Airflow`, `Airbyte`, `Fivetran`) e **IA & Analytics** (`Workflows Agénticos`, `LLMs`, `Detección de Anomalías`, `Inferencia Causal`, `Forecasting`, `Power BI`, `Superset`, `Streamlit`).',
        'His core stack combines **Platforms & Cloud** (`Snowflake`, `Databricks`, `Azure ADF/DevOps`, `AWS S3/EC2`, `GCP`), **Pipelines & Orchestration** (`Python`, `SQL`, `Apache Spark`, `dbt`, `Airflow`, `Airbyte`, `Fivetran`), and **AI & Analytics** (`Agentic Workflows`, `LLMs`, `Anomaly Detection`, `Causal Inference`, `Forecasting`, `Power BI`, `Superset`, `Streamlit`).',
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
    q.includes('best day') ||
    q.includes('trabajo') ||
    q.includes('empresa') ||
    q.includes('actual') ||
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
        'Actualmente trabaja como **Data Engineer en Tongo** (Fintech de EE.UU.), tras desempeñarse como Data Engineer en **Siemens Advanta**, Data Scientist en **AB InBev** y **Lumen Technologies**, Quantitative Analyst en **Balanz Capital**, **Portfolio Manager** y Treasury Analyst en **Best Day**. En **Mi CV** podés explorar cada etapa o bajar el PDF directo.',
        'He currently works as a **Data Engineer at Tongo** (U.S. Fintech), following roles as a Data Engineer at **Siemens Advanta**, Data Scientist at **AB InBev** and **Lumen Technologies**, Quantitative Analyst at **Balanz Capital**, **Portfolio Manager**, and Treasury Analyst at **Best Day**. In **My CV** you can inspect every stage or download the PDF.',
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
        'Su formación académica combina **3 posgrados** sobre su **Licenciatura en Administración** (UNLZ): **Maestría en Finanzas** (UBA), **Maestría en Ciencia de Datos** (UBA) y **Posgrado en Finanzas Cuantitativas** (UCEMA). Podés tocar cada título en la columna derecha de **Mi CV** para ver las materias clave.',
        'His academic background combines **3 postgraduate programs** on top of his **BSc in Business Administration** (UNLZ): **MSc in Finance** (UBA), **MSc in Data Science** (UBA), and **Executive Program in Quantitative Finance** (UCEMA). You can tap each degree on the right column of **My CV** to see its core subjects.',
        lang
      ),
      actions: [
        {
          type: 'section',
          target: 'timeline',
          label: tx('Ver Educación en Mi CV →', 'View Education in My CV →', lang)
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
        '**QuantLambda** (`quantlambda.dev`) es su proyecto insignia: una plataforma en vivo para explorar **213 activos globales**, analizar opciones y curvas de tasas en 3D, simular el riesgo de carteras ante crisis históricas y debatir tesis con un comité de agentes e inteligencia artificial.',
        '**QuantLambda** (`quantlambda.dev`) is his flagship project: a live platform to explore **213 global assets**, inspect 3D options & sovereign yield curves, stress-test portfolios against historical crises, and evaluate investment theses with an AI committee.',
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
        'En **Análisis** (`#analisis`) encontrás el estudio *Macroeconomía, Gasto Público y Degradación del Empleo en Argentina (1980–Presente)*: concilia **7 fuentes oficiales** mediante un pipeline automatizado, con **5 gráficos interactivos** y proyecciones econométricas `SARIMAX`.',
        'In **Research** (`#analisis`) you can read *Macroeconomics, Public Spending & Labor Quality Degradation in Argentina (1980–Present)*: reconciling **7 official sources** via an automated pipeline, with **5 interactive charts** and `SARIMAX` econometric forecasts.',
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
        'En **Proyectos** (`#proyectos`), además de **QuantLambda**, tenés **3 aplicaciones interactivas** para probar:\n• **Spark Learning:** guía visual paso a paso sobre Apache Spark.\n• **World Map:** marcá los países que visitaste y creá tu propio mapa.\n• **Quality of Life Explorer:** compará 44 indicadores históricos en 240 países.',
        'In **Projects** (`#proyectos`), alongside **QuantLambda**, you have **3 interactive apps** to try:\n• **Spark Learning:** step-by-step visual guide to Apache Spark.\n• **World Map:** mark the countries you visited and style your own map.\n• **Quality of Life Explorer:** compare 44 historical indicators across 240 countries.',
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
        'Podés usar la web con clic o **100% con el teclado**: `1` abre **Proyectos**, `2` **Análisis**, `3` **Mi CV** (adentro `d` descarga el PDF), `c` abre/cierra este chat, `gh`/`li`/`gm` abren GitHub, LinkedIn o Gmail, `l` abre los **56 idiomas** y `t` cambia el tema.',
        'You can use the site by click or **100% by keyboard**: `1` opens **Projects**, `2` **Research**, `3` **My CV** (inside, `d` downloads the PDF), `c` toggles this chat, `gh`/`li`/`gm` open GitHub, LinkedIn, or Gmail, `l` opens the **56 languages**, and `t` switches theme.',
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
        'Podés escribirle o seguir el trabajo de Alejandro directamente por **LinkedIn**, **GitHub** o **Email** desde estos accesos:',
        'You can reach out or follow Alejandro’s work directly on **LinkedIn**, **GitHub**, or **Email** via these links:',
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

  // 9. Respuesta conversacional amigable por defecto ("hola, en la app tenés...")
  return {
    text: tx(
      '¡Hola! Mirá, te cuento rápido qué tenés acá en la app para que explores lo que más te interese:\n• En **Proyectos** podés probar **QuantLambda** (mercados y carteras en vivo) y 3 apps interactivas (*Spark*, *World Map* y *Quality of Life*).\n• En **Análisis** tenés un estudio macroeconómico y laboral sobre Argentina.\n• En **Mi CV** podés recorrer toda la experiencia y formación de Alejandro (2011–2026) o bajarte su **CV en PDF**.',
      'Hi! Here is a quick tour of what you have in the app so you can jump straight into what interests you most:\n• In **Projects** you can try **QuantLambda** (live markets & portfolios) and 3 interactive apps (*Spark*, *World Map*, and *Quality of Life*).\n• In **Research** you have an econometric study on Argentine macroeconomics & labor.\n• In **My CV** you can explore Alejandro’s full experience & education (2011–2026) or download his **PDF CV**.',
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
      id: 'hello',
      label: tx('👋 ¿Qué hay en la app?', '👋 What’s in the app?', lang),
      query: tx('¡Hola! ¿Qué puedo ver en la app?', 'Hi! What can I see in the app?', lang)
    },
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
      '¡Hola! 👋 Bienvenido a la web de **Alejandro**. Podés saludarme, escribir cualquier duda o tocar uno de los temas de acá abajo para ir directo:',
      'Hi! 👋 Welcome to **Alejandro’s** website. Feel free to say hello, ask anything, or tap one of the topics below to jump right in:',
      lang
    ),
    actions: [
      {
        type: 'section',
        target: 'playground',
        label: tx('Ver Proyectos →', 'View Projects →', lang)
      },
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
