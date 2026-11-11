import React, { useState, useEffect, useRef } from 'react';
import { tx, txList, useSiteLocale } from '../../i18n/localeService';

export const WORK_ITEMS = [
  {
    id: 'tongo',
    role: 'Data Engineer',
    company: 'Tongo',
    scopeEs: 'Fintech Startup • Estados Unidos (Remoto - Contractor)',
    scopeEn: 'Fintech Startup • United States (Remote - Contractor)',
    start: 2025.92,
    end: 2026.85,
    periodEs: '12/2025 – Presente',
    periodEn: '12/2025 – Present',
    colorAccent: '#f43f5e',
    colorRgb: '244, 63, 94',
    bulletsEs: [
      'Flujos de Datos & Reverse ETL: Orquestación end-to-end entre S3, bases OLTP/OLAP y apps de negocio (HubSpot, Slack) vía scrapers, APIs, Airbyte y Fivetran, rediseñando claves primarias para eliminar duplicados y reducir el volumen sincronizado a <1%.',
      'Arquitectura Core & Optimización: Diseño de pipelines críticos en AWS EC2, dbt (Airflow y GitHub Actions) y Snowflake nativo, reemplazando vistas anidadas por procedimientos materializados para bajar la complejidad de exponencial a logarítmica y los tiempos de horas a segundos.',
      'BI-as-Code & Apps Operativas: Desarrollo de tableros con resúmenes contextuales de IA en Superset, aplicaciones interactivas en Streamlit y frameworks cuantitativos de reconciliación y benchmarking para toda la compañía.'
    ],
    bulletsEn: [
      'Data Flows & Reverse ETL: End-to-end orchestration across S3, OLTP/OLAP databases, and business apps (HubSpot, Slack) via scrapers, APIs, Airbyte, and Fivetran, redesigning primary keys to eliminate duplicates and cut synced volume to <1%.',
      'Core Architecture & Optimization: Engineered mission-critical pipelines in AWS EC2, dbt (Airflow & GitHub Actions), and native Snowflake, replacing nested views with materialized procedures to reduce complexity from exponential to logarithmic and runtime from hours to seconds.',
      'BI-as-Code & Operational Apps: Built AI-summarized dashboards in Superset, interactive Streamlit applications, and quantitative reconciliation and benchmarking frameworks across the company.'
    ]
  },
  {
    id: 'siemens',
    role: 'Data Engineer (Consulting)',
    company: 'Siemens Advanta',
    scopeEs: 'Consultoría Global • Palma de Mallorca, España (Remoto - Contractor)',
    scopeEn: 'Global Consulting • Palma de Mallorca, Spain (Remote - Contractor)',
    start: 2025.08,
    end: 2025.92,
    periodEs: '02/2025 – 11/2025',
    periodEn: '02/2025 – 11/2025',
    colorAccent: '#f43f5e',
    colorRgb: '244, 63, 94',
    bulletsEs: [
      'Ingeniería de Pipelines en Azure: Mantenimiento, optimización y depuración de flujos productivos distribuidos con Apache Spark (PySpark), Python y SQL sobre Azure Databricks, Data Factory (ADF) y Blob Storage.',
      'Procesamiento a Gran Escala: Orquestación de cargas incrementales y particionado sobre miles de millones de registros transaccionales y financieros bajo flujos CI/CD en Azure DevOps.',
      'Modelado Dimensional & BI: Diseño de arquitecturas Snowflake/Star Schema y desarrollo de más de 30 reportes financieros corporativos en Power BI (DAX avanzado y Power Query) para clientes Fortune 500.'
    ],
    bulletsEn: [
      'Azure Pipeline Engineering: Maintained, optimized, and debugged distributed production data flows using Apache Spark (PySpark), Python, and SQL on Azure Databricks, Data Factory (ADF), and Blob Storage.',
      'Large-Scale Processing: Orchestrated incremental loads and partitioning over billions of transactional and financial records under CI/CD workflows in Azure DevOps.',
      'Dimensional Modeling & BI: Designed Snowflake/Star Schema architectures and delivered 30+ corporate financial reports in Power BI (advanced DAX & Power Query) for Fortune 500 clients.'
    ]
  },
  {
    id: 'abinbev',
    role: 'Data Scientist (Fraud & Pricing)',
    company: 'AB InBev',
    scopeEs: 'Consumo Masivo Global • Bruselas, Bélgica (Remoto - Contractor)',
    scopeEn: 'Global FMCG • Brussels, Belgium (Remote - Contractor)',
    start: 2023.58,
    end: 2025.08,
    periodEs: '08/2023 – 01/2025',
    periodEn: '08/2023 – 01/2025',
    colorAccent: '#a855f7',
    colorRgb: '168, 85, 247',
    bulletsEs: [
      'Infraestructura de Datos de Fraude: Gobierno de más de 25 pipelines productivos en Spark/Python y SQL sobre Databricks y Snowflake para LATAM, reduciendo la latencia de horas a segundos para reporting ejecutivo del C-Suite.',
      'Detección de Anomalías (ML): Entrenamiento y despliegue de modelos no supervisados y supervisados de prevención de fraude (Python, Scikit-learn, Isolation Forest), mejorando la rentabilidad un 3% en mercados clave.',
      'Inferencia Causal & Pricing: Diseño y evaluación estadística de experimentos de elasticidad y optimización de precios (A/B Testing y RCTs), incrementando el volumen de ventas un 0.5% en mercados principales.'
    ],
    bulletsEn: [
      'Fraud Data Infrastructure: Governed 25+ production Spark/Python and SQL pipelines on Databricks and Snowflake across LATAM, cutting latency from hours to seconds for C-Suite executive reporting.',
      'Anomaly Detection (ML): Trained and deployed unsupervised and supervised fraud prevention models (Python, Scikit-learn, Isolation Forest), improving profitability by 3% in key markets.',
      'Causal Inference & Pricing: Designed and statistically evaluated price elasticity and optimization experiments (A/B Testing & RCTs), lifting sales volume by 0.5% in core markets.'
    ]
  },
  {
    id: 'lumen',
    role: 'Data Scientist (Corporate Finance)',
    company: 'Lumen Technologies',
    scopeEs: 'Telecomunicaciones • Buenos Aires, Argentina (Híbrido)',
    scopeEn: 'Telecommunications • Buenos Aires, Argentina (Hybrid)',
    start: 2021.83,
    end: 2023.58,
    periodEs: '11/2021 – 07/2023',
    periodEn: '11/2021 – 07/2023',
    colorAccent: '#a855f7',
    colorRgb: '168, 85, 247',
    bulletsEs: [
      'Automatización ETL & Reporting: Construcción de más de 10 pipelines ETL productivos (Python, SQL y Talend) que automatizaron el ecosistema de tableros en Power BI para más de 50 stakeholders financieros y de liderazgo.',
      'Forecasting & Riesgo Crediticio: Desarrollo de modelos predictivos de comportamiento de pago, riesgo de mora y proyección de flujo de caja (Random Forests y regresiones) para planificación financiera regional.',
      'People Analytics & NLP: Aplicación de procesamiento de lenguaje natural sobre encuestas de clima y salida (NLTK, spaCy) para detectar drivers de rotación y guiar políticas de retención en RR.HH.'
    ],
    bulletsEn: [
      'ETL & Reporting Automation: Built 10+ production ETL pipelines (Python, SQL, Talend) automating the Power BI dashboard ecosystem for 50+ finance and leadership stakeholders.',
      'Forecasting & Credit Risk: Developed predictive models for payment behavior, default risk, and cash-flow forecasting (Random Forests & regressions) for regional financial planning.',
      'People Analytics & NLP: Applied natural language processing on climate and exit surveys (NLTK, spaCy) to uncover turnover drivers and guide HR retention policies.'
    ]
  },
  {
    id: 'balanz',
    role: 'Quantitative Analyst (Algorithmic Trading)',
    company: 'Balanz Capital',
    scopeEs: 'Mercado de Capitales • Buenos Aires, Argentina (Híbrido)',
    scopeEn: 'Capital Markets • Buenos Aires, Argentina (Hybrid)',
    start: 2021.08,
    end: 2021.83,
    periodEs: '02/2021 – 10/2021',
    periodEn: '02/2021 – 10/2021',
    colorAccent: '#10b981',
    colorRgb: '16, 185, 129',
    bulletsEs: [
      'Estrategias de Trading Algorítmico: Investigación, desarrollo y backtesting de estrategias sistemáticas direccionales y de arbitraje con Python y redes neuronales recurrentes (LSTM) para activos de Argentina y EE.UU.',
      'Modelado de Derivados & Volatilidad: Construcción de herramientas de análisis cuantitativo para curvas de tasas, superficies y sonrisas de volatilidad implícita orientadas a la operatoria de la mesa.',
      'Visualización Cuantitativa Interactiva: Desarrollo de monitores dinámicos de mercado en Python (Plotly, Seaborn) para seguimiento de señales, ejecución y riesgo en tiempo real.'
    ],
    bulletsEn: [
      'Algorithmic Trading Strategies: Researched, developed, and backtested systematic directional and arbitrage strategies using Python and recurrent neural networks (LSTM) for Argentine and US assets.',
      'Derivatives & Volatility Modeling: Built quantitative analytics tools for yield curves, implied volatility surfaces, and option smiles tailored for trading desk execution.',
      'Interactive Quantitative Visualization: Created dynamic market monitors in Python (Plotly, Seaborn) for real-time signal, execution, and risk tracking.'
    ]
  },
  {
    id: 'portfolio-manager-indep',
    role: 'Portfolio Manager',
    company: 'Independent',
    scopeEs: 'Mercado de Capitales • Asset Management',
    scopeEn: 'Capital Markets • Asset Management',
    start: 2018.08,
    end: 2021.08,
    periodEs: '02/2018 – 01/2021',
    periodEn: '02/2018 – 01/2021',
    colorAccent: '#10b981',
    colorRgb: '16, 185, 129',
    bulletsEs: [
      'Profiling & Propuestas de Inversión: Perfilamiento integral de inversores evaluando aversión al riesgo, horizonte temporal y liquidez para estructurar propuestas a medida (Strategic & Tactical Asset Allocation).',
      'Rebalanceo & Control de Riesgo: Ejecución sistemática de rebalanceos en carteras multimoneda (renta fija, equity y derivados), optimizando el ratio retorno/riesgo y acotando el drawdown ante cambios de régimen.',
      'Reporting & Performance Attribution: Elaboración de reportes ejecutivos de rendimiento, atribución de resultados y seguimiento patrimonial periódico frente a benchmarks de referencia.'
    ],
    bulletsEn: [
      'Investor Profiling & Proposals: Comprehensive investor profiling assessing risk aversion, time horizon, and liquidity to structure tailored portfolios (Strategic & Tactical Asset Allocation).',
      'Rebalancing & Risk Control: Systematic rebalancing across multi-currency portfolios (fixed income, equities, and derivatives), optimizing risk-adjusted return and limiting drawdown across regime shifts.',
      'Reporting & Performance Attribution: Executive performance reporting, return attribution, and periodic wealth tracking against market benchmarks.'
    ]
  },
  {
    id: 'bestday',
    role: 'Semi Senior Treasury Analyst (South America)',
    company: 'Best Day Travel Group',
    scopeEs: 'Finanzas Corporativas • Sudamérica',
    scopeEn: 'Corporate Finance • South America',
    start: 2015.5,
    end: 2018.08,
    periodEs: '07/2015 – 01/2018',
    periodEn: '07/2015 – 01/2018',
    colorAccent: '#f59e0b',
    colorRgb: '245, 158, 11',
    bulletsEs: [
      'Treasury & Liquidity Management: Administración integral de liquidez y tesorería regional para Sudamérica, optimizando el flujo de caja operativo, el capital de trabajo y la posición financiera diaria.',
      'Corporate Finance & FX Reporting: Elaboración de reportes ejecutivos de finanzas corporativas, gestión de cuentas por cobrar y por pagar (AR/AP) y seguimiento de exposición cambiaria multimoneda.',
      'Automatización Contable (Excel VBA): Desarrollo de macros avanzadas en Microsoft Excel para automatizar cierres contables, conciliaciones bancarias masivas y controles operativos.'
    ],
    bulletsEn: [
      'Treasury & Liquidity Management: Regional liquidity and treasury management across South America, optimizing operating cash flow, working capital, and daily financial positions.',
      'Corporate Finance & FX Reporting: Executive corporate finance reporting, accounts receivable/payable (AR/AP) management, and multi-currency FX exposure tracking.',
      'Accounting Automation (Excel VBA): Built advanced Microsoft Excel macros to automate accounting closes, high-volume bank reconciliations, and operational controls.'
    ]
  }
];

export const EDU_ITEMS = [
  {
    id: 'ucema',
    degree: 'Executive Program in Quantitative Finance',
    school: 'Universidad del CEMA (UCEMA)',
    scopeEs: 'Posgrado en Finanzas Cuantitativas (Programa QUANt)',
    scopeEn: 'Postgraduate Program in Quantitative Finance (QUANt)',
    start: 2022.17,
    end: 2022.95,
    periodEs: '03/2022 – 12/2022',
    periodEn: '03/2022 – 12/2022',
    colorAccent: '#10b981',
    colorRgb: '16, 185, 129',
    bulletsEs: [
      'Mercado de Capitales & Derivados: Teoría moderna de portafolios, optimización cuantitativa de carteras, instrumentos de Renta Fija, Equity y exóticos, pricing y cobertura de derivados financieros y trading algorítmico.',
      'Matemática, Estadística & Computación: Cálculo estocástico, ecuaciones diferenciales, álgebra lineal numérica y simulación de Montecarlo; econometría de series de tiempo y Machine Learning financiero en Python.',
      'Investigación Aplicada: Segmentación cuantitativa multivariada (K-Means) sobre factores fundamentales y técnicos y backtesting algorítmico sobre activos del S&P 500.'
    ],
    bulletsEn: [
      'Capital Markets & Derivatives: Modern portfolio theory, quantitative portfolio optimization, Fixed Income, Equity & exotic instruments, derivatives pricing & hedging, and algorithmic trading.',
      'Mathematics, Statistics & Computing: Stochastic calculus, differential equations, numerical linear algebra, and Monte Carlo simulation; time-series econometrics and financial Machine Learning in Python.',
      'Applied Research: Multivariate quantitative segmentation (K-Means) across fundamental and technical factors and algorithmic backtesting on S&P 500 equities.'
    ]
  },
  {
    id: 'uba-ds',
    degree: 'Master’s Degree in Data Science (MSc)',
    school: 'Universidad de Buenos Aires (UBA)',
    scopeEs: 'Maestría en Explotación de Datos y Descubrimiento del Conocimiento (FIUBA / FCEN)',
    scopeEn: 'MSc in Data Mining & Knowledge Discovery (FIUBA / FCEN)',
    start: 2020.17,
    end: 2021.95,
    periodEs: '03/2020 – 12/2021',
    periodEn: '03/2020 – 12/2021',
    colorAccent: '#a855f7',
    colorRgb: '168, 85, 247',
    bulletsEs: [
      'Ciclo Troncal: Aprendizaje Automático (Machine Learning), Análisis Inteligente de Datos, Data Mining, Enfoque Estadístico del Aprendizaje y Knowledge Discovery en Economía, Finanzas y Ciencia.',
      'Modelado Avanzado & Especialización: Redes Neuronales y Deep Learning, Data Mining en Series Temporales, Tópicos Avanzados de Text & Web Mining (NLP) y Metaheurísticas de optimización.',
      'Ingeniería & Arquitectura de Datos: Data Warehousing, Sistemas de Información Geográfica (GIS), Recuperación de Información, Visualización de la Información y Arquitecturas de Big Data.'
    ],
    bulletsEn: [
      'Core Curriculum: Machine Learning, Intelligent Data Analysis, Data Mining, Statistical Learning, and Knowledge Discovery across Economics, Finance, and Science.',
      'Advanced Modeling & Specialization: Neural Networks & Deep Learning, Time-Series Data Mining, Advanced Text & Web Mining (NLP), and Optimization Metaheuristics.',
      'Data Engineering & Architecture: Data Warehousing, Geographic Information Systems (GIS), Information Retrieval, Information Visualization, and Big Data Architectures.'
    ]
  },
  {
    id: 'uba-fin',
    degree: 'Master’s Degree in Finance (Corporate Finance)',
    school: 'Universidad de Buenos Aires (UBA)',
    scopeEs: 'Maestría en Finanzas — Orientación Finanzas Corporativas (FCE)',
    scopeEn: 'MSc in Finance — Corporate Finance Track (FCE)',
    start: 2017.67,
    end: 2019.75,
    periodEs: '09/2017 – 09/2019',
    periodEn: '09/2017 – 09/2019',
    colorAccent: '#10b981',
    colorRgb: '16, 185, 129',
    bulletsEs: [
      'Ciclo Común & Mercados: Análisis cuantitativo para decisiones financieras, Entorno macroeconómico y elaboración de escenarios, Diagnóstico financiero e Instrumentos de Renta Fija, Renta Variable y Derivados.',
      'Finanzas Corporativas & Valuación: Estructura y costo de capital (WACC), Valuación de empresas, Fusiones y Adquisiciones (M&A), Evaluación de proyectos de inversión y Gestión estratégica de tesorería.',
      'Riesgo & Gobierno Corporativo: Gestión integral de riesgos financieros y operativos del negocio, regulación de mercados, control de gestión estratégica y gobierno corporativo.'
    ],
    bulletsEn: [
      'Core & Markets: Quantitative analysis for financial decisions, Macroeconomic environment & scenario planning, Financial diagnosis, and Fixed Income, Equity & Derivatives instruments.',
      'Corporate Finance & Valuation: Capital structure & cost of capital (WACC), Corporate valuation, Mergers & Acquisitions (M&A), Investment project evaluation, and Strategic treasury management.',
      'Risk & Corporate Governance: Enterprise financial and operational risk management, market regulation, strategic management control, and corporate governance.'
    ]
  },
  {
    id: 'unlz',
    degree: 'Bachelor’s Degree in Business Administration (BSc)',
    school: 'Universidad Nacional de Lomas de Zamora (UNLZ)',
    scopeEs: 'Licenciatura en Administración (Facultad de Ciencias Económicas)',
    scopeEn: 'BSc in Business Administration (School of Economics)',
    start: 2011.0,
    end: 2017.58,
    periodEs: '01/2011 – 07/2017',
    periodEn: '01/2011 – 07/2017',
    colorAccent: '#f59e0b',
    colorRgb: '245, 158, 11',
    bulletsEs: [
      'Métodos Cuantitativos & Finanzas: Matemática I y II, Matemática Financiera, Estadística, Investigación Operativa, Administración Financiera y Seminario de Planeamiento y Evaluación de Proyectos.',
      'Economía & Coyuntura: Microeconomía, Macroeconomía, Finanzas Públicas, Historia Económica y análisis de Coyuntura Económica aplicada a la toma de decisiones empresariales.',
      'Contabilidad & Dirección Estratégica: Contabilidad Básica, Técnicas de Valuación, Sistemas de Costos, Costos para la Toma de Decisiones, Sistemas Administrativos, Planeamiento y Dirección General.'
    ],
    bulletsEn: [
      'Quantitative Methods & Finance: Mathematics I & II, Financial Mathematics, Statistics, Operations Research, Financial Management, and Project Planning & Evaluation.',
      'Economics & Macro Analysis: Microeconomics, Macroeconomics, Public Finance, Economic History, and Applied Macroeconomic Analysis for business decision-making.',
      'Accounting & Strategic Management: Financial Accounting, Valuation Techniques, Cost Systems, Decision-Making Costs, Administrative Systems, Planning, and General Management.'
    ]
  }
];

const ALL_ITEMS = [
  ...WORK_ITEMS.map((w) => ({ ...w, kind: 'work', title: w.role, subtitle: w.company })),
  ...EDU_ITEMS.map((e) => ({ ...e, kind: 'edu', title: e.degree, subtitle: e.school }))
];

const YEARS_DESC = Array.from({ length: 16 }, (_, i) => 2026 - i); // 2026..2011

const MIN_YEAR = 2011.0;
const MAX_YEAR = 2026.8;
const TOTAL_SPAN = MAX_YEAR - MIN_YEAR;

function getTopPct(yearValue) {
  return ((MAX_YEAR - yearValue) / TOTAL_SPAN) * 100;
}

function getHeightPct(startYear, endYear) {
  return Math.max(4.8, ((endYear - startYear) / TOTAL_SPAN) * 100 - 0.8);
}

function getMidPct(startYear, endYear) {
  return getTopPct((startYear + endYear) * 0.5);
}

function computeDeoverlappedPcts(items, minGapPct = 12.6, topBound = 6, bottomBound = 92.5) {
  const positions = items.map((it) => getMidPct(it.start, it.end));
  for (let i = 0; i < positions.length; i++) {
    if (i === 0) {
      positions[i] = Math.max(topBound, positions[i]);
    } else {
      positions[i] = Math.max(positions[i], positions[i - 1] + minGapPct);
    }
  }
  if (positions[positions.length - 1] > bottomBound) {
    positions[positions.length - 1] = bottomBound;
    for (let i = positions.length - 2; i >= 0; i--) {
      positions[i] = Math.min(positions[i], positions[i + 1] - minGapPct);
    }
  }
  return positions;
}

const WORK_CLEAN_PCTS = computeDeoverlappedPcts(WORK_ITEMS, 13.4, 5.5, 93.0);
const EDU_CLEAN_PCTS = computeDeoverlappedPcts(EDU_ITEMS, 18.0, 20.0, 82.0);

function buildDagConnectorPath(side, labelY, midPct) {
  const isLeft = side === 'left';
  const xStart = isLeft ? 0 : 100;
  const xEnd = isLeft ? 100 : 0;
  const c1 = isLeft ? 55 : 45;
  const c2 = isLeft ? 45 : 55;
  return `M ${xStart} ${labelY} C ${c1} ${labelY}, ${c2} ${midPct}, ${xEnd} ${midPct}`;
}

export default function TimelineSection({ colorMode = 'dark', lang = 'ES' }) {
  useSiteLocale(lang);
  const [selectedId, setSelectedId] = useState('tongo');
  const inspectorRef = useRef(null);

  const handleSelectNode = (id) => {
    setSelectedId(id);
    if (typeof window !== 'undefined' && window.innerWidth <= 680) {
      setTimeout(() => {
        inspectorRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 60);
    }
  };

  const selectedItem = ALL_ITEMS.find((it) => it.id === selectedId) || ALL_ITEMS[0];
  const activeSpanTop = getTopPct(selectedItem.end);
  const activeSpanHeight = getHeightPct(selectedItem.start, selectedItem.end);

  // Navegación por teclado en el grafo DAG de Mi CV (↑/↓ dentro de la columna, ←/→ entre Experiencia y Educación, D para PDF)
  useEffect(() => {
    const handleKey = (e) => {
      const tag = document.activeElement?.tagName?.toLowerCase();
      if (tag === 'input' || tag === 'textarea') return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;

      const isWork = WORK_ITEMS.some((w) => w.id === selectedId);
      const currentList = isWork ? WORK_ITEMS : EDU_ITEMS;
      const idx = currentList.findIndex((it) => it.id === selectedId);

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        const nextIdx = (idx + 1) % currentList.length;
        setSelectedId(currentList[nextIdx].id);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        const prevIdx = (idx - 1 + currentList.length) % currentList.length;
        setSelectedId(currentList[prevIdx].id);
      } else if (e.key === 'ArrowRight' && isWork) {
        e.preventDefault();
        setSelectedId(EDU_ITEMS[0].id);
      } else if (e.key === 'ArrowLeft' && !isWork) {
        e.preventDefault();
        setSelectedId(WORK_ITEMS[0].id);
      } else if (e.key.toLowerCase() === 'd') {
        e.preventDefault();
        const link = document.createElement('a');
        link.href = '/Alejandro_Camerlengo_Data_Engineer.pdf';
        link.download = 'Alejandro_Camerlengo_CV.pdf';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [selectedId]);

  const selectedScope = tx(selectedItem.scopeEs, selectedItem.scopeEn, lang);
  const selectedPeriod = tx(selectedItem.periodEs, selectedItem.periodEn, lang);
  const selectedBullets = txList(selectedItem.bulletsEs, selectedItem.bulletsEn, lang);

  return (
    <div className="tl-root">
      {/* CABECERA UNIFICADA DE MI CV */}
      <div className="pj-purpose-header">
        <h2 className="tl-main-title">
          {tx(
            'Negocios & Finanzas → Data Science → Data Engineering',
            'Business & Finance → Data Science → Data Engineering',
            lang
          )}
        </h2>
        <p className="pj-purpose-lead">
          {tx(
            'Línea de tiempo proporcional (2011–2026): hacé clic en cualquier etapa laboral o académica para ver en detalle su alcance y responsabilidades.',
            'Proportional timeline (2011–2026): click any work or academic stage to inspect its scope and key deliverables in detail.',
            lang
          )}
        </p>
      </div>

      {/* ESCENARIO DAG DE DOBLE EJE */}
      <div className="tl-stage-box scifi-dag">
        <span className="tl-hud-corner tl-corner-tl" aria-hidden="true" />
        <span className="tl-hud-corner tl-corner-tr" aria-hidden="true" />
        <span className="tl-hud-corner tl-corner-bl" aria-hidden="true" />
        <span className="tl-hud-corner tl-corner-br" aria-hidden="true" />

        <div className="tl-d1-col-headers">
          <span className="tl-col-pill">{tx('EXPERIENCIA', 'EXPERIENCE', lang)}</span>
          <span aria-hidden="true" />
          <span className="tl-col-pill">{tx('EDUCACIÓN', 'EDUCATION', lang)}</span>
        </div>

        <div className="tl-dual-canvas">
          {/* COLUMNA IZQUIERDA: EXPERIENCIA LABORAL */}
          <div className="tl-side tl-side-work">
            {WORK_ITEMS.map((item, idx) => {
              const isSelected = selectedId === item.id;
              const topPct = getTopPct(item.end);
              const heightPct = getHeightPct(item.start, item.end);
              const midPct = getMidPct(item.start, item.end);
              const labelY = WORK_CLEAN_PCTS[idx];
              const pathD = buildDagConnectorPath('left', labelY, midPct);

              return (
                <React.Fragment key={item.id}>
                  <span
                    className={`tl-duration-rail rail-left mode-dag ${isSelected ? 'is-selected' : ''}`}
                    style={{
                      top: `${topPct}%`,
                      height: `${heightPct}%`,
                      '--item-accent': item.colorAccent,
                      '--item-rgb': item.colorRgb
                    }}
                    onClick={() => handleSelectNode(item.id)}
                  />

                  <svg
                    className={`tl-leader-svg side-left mode-dag ${isSelected ? 'is-selected' : ''}`}
                    viewBox="0 0 100 100"
                    preserveAspectRatio="none"
                    aria-hidden="true"
                  >
                    <path
                      d={pathD}
                      className="tl-trace-base"
                      stroke={item.colorAccent}
                      strokeWidth={isSelected ? '2.2' : '1.15'}
                      strokeOpacity={isSelected ? '0.95' : '0.35'}
                      fill="none"
                      vectorEffect="non-scaling-stroke"
                    />
                    {isSelected && (
                      <path
                        d={pathD}
                        className="tl-trace-pulse"
                        stroke={colorMode === 'light' ? item.colorAccent : '#ffffff'}
                        strokeWidth="2"
                        fill="none"
                        vectorEffect="non-scaling-stroke"
                      />
                    )}
                  </svg>

                  <button
                    type="button"
                    className={`tl-scifi-node mode-dag side-work ${isSelected ? 'is-selected' : ''}`}
                    style={{
                      top: `${labelY}%`,
                      '--item-accent': item.colorAccent,
                      '--item-rgb': item.colorRgb
                    }}
                    onClick={() => handleSelectNode(item.id)}
                  >
                    <div className="tl-node-main-row">
                      <div className="tl-node-titles">
                        <span className="tl-node-role">{item.role}</span>
                        <span className="tl-node-org">{item.company}</span>
                      </div>
                      <span className="tl-node-period-badge">
                        {tx(item.periodEs, item.periodEn, lang)}
                      </span>
                    </div>

                    <span className="tl-port-dot port-right" aria-hidden="true" />
                  </button>
                </React.Fragment>
              );
            })}
          </div>

          {/* EJE CENTRAL DE AÑOS (2026 → 2011) */}
          <div className="tl-center-axis">
            <div
              className="tl-axis-active-glow"
              style={{
                top: `${activeSpanTop}%`,
                height: `${activeSpanHeight}%`,
                '--item-accent': selectedItem.colorAccent
              }}
            />

            {YEARS_DESC.map((yr) => {
              const inActiveRange =
                yr >= Math.floor(selectedItem.start) && yr <= Math.ceil(selectedItem.end);
              return (
                <div
                  key={yr}
                  className={`tl-year-node ${inActiveRange ? 'in-range' : ''}`}
                  style={{
                    top: `${getTopPct(yr)}%`,
                    '--item-accent': selectedItem.colorAccent
                  }}
                >
                  <span>{yr}</span>
                </div>
              );
            })}
          </div>

          {/* COLUMNA DERECHA: EDUCACIÓN */}
          <div className="tl-side tl-side-edu">
            {EDU_ITEMS.map((item, idx) => {
              const isSelected = selectedId === item.id;
              const topPct = getTopPct(item.end);
              const heightPct = getHeightPct(item.start, item.end);
              const midPct = getMidPct(item.start, item.end);
              const labelY = EDU_CLEAN_PCTS[idx];
              const pathD = buildDagConnectorPath('right', labelY, midPct);

              return (
                <React.Fragment key={item.id}>
                  <span
                    className={`tl-duration-rail rail-right mode-dag ${isSelected ? 'is-selected' : ''}`}
                    style={{
                      top: `${topPct}%`,
                      height: `${heightPct}%`,
                      '--item-accent': item.colorAccent,
                      '--item-rgb': item.colorRgb
                    }}
                    onClick={() => handleSelectNode(item.id)}
                  />

                  <svg
                    className={`tl-leader-svg side-right mode-dag ${isSelected ? 'is-selected' : ''}`}
                    viewBox="0 0 100 100"
                    preserveAspectRatio="none"
                    aria-hidden="true"
                  >
                    <path
                      d={pathD}
                      className="tl-trace-base"
                      stroke={item.colorAccent}
                      strokeWidth={isSelected ? '2.2' : '1.15'}
                      strokeOpacity={isSelected ? '0.95' : '0.35'}
                      fill="none"
                      vectorEffect="non-scaling-stroke"
                    />
                    {isSelected && (
                      <path
                        d={pathD}
                        className="tl-trace-pulse"
                        stroke={colorMode === 'light' ? item.colorAccent : '#ffffff'}
                        strokeWidth="2"
                        fill="none"
                        vectorEffect="non-scaling-stroke"
                      />
                    )}
                  </svg>

                  <button
                    type="button"
                    className={`tl-scifi-node mode-dag side-edu ${isSelected ? 'is-selected' : ''}`}
                    style={{
                      top: `${labelY}%`,
                      '--item-accent': item.colorAccent,
                      '--item-rgb': item.colorRgb
                    }}
                    onClick={() => handleSelectNode(item.id)}
                  >
                    <div className="tl-node-main-row">
                      <div className="tl-node-titles">
                        <span className="tl-node-role">{item.degree}</span>
                        <span className="tl-node-org">{item.school}</span>
                      </div>
                      <span className="tl-node-period-badge">
                        {tx(item.periodEs, item.periodEn, lang)}
                      </span>
                    </div>

                    <span className="tl-port-dot port-left" aria-hidden="true" />
                  </button>
                </React.Fragment>
              );
            })}
          </div>
        </div>
      </div>

      {/* CAJA EXPLICATORIA ABAJO (CON EL CONTENIDO DEL CV SIN TAGS) */}
      <footer
        ref={inspectorRef}
        className="tl-bottom-inspector"
        style={{
          '--insp-accent': selectedItem.colorAccent,
          '--insp-rgb': selectedItem.colorRgb
        }}
      >
        <div className="tl-bottom-insp-top">
          <div className="tl-bottom-insp-title-wrap">
            <h3 className="tl-bottom-insp-title">{selectedItem.title}</h3>
            <span className="tl-bottom-insp-org">
              • {selectedItem.subtitle} ({selectedScope})
            </span>
          </div>
          <span className="tl-insp-period">{selectedPeriod}</span>
        </div>

        <ul className="pj-clean-bullets">
          {selectedBullets.map((b) => {
            const colonIdx = b.indexOf(':');
            if (colonIdx > 0 && colonIdx < 54) {
              const lead = b.slice(0, colonIdx + 1).trim();
              const rest = b.slice(colonIdx + 1).trim();
              return (
                <li key={b}>
                  <strong className="tl-bullet-lead">{lead}</strong> {rest}
                </li>
              );
            }
            return <li key={b}>{b}</li>;
          })}
        </ul>
      </footer>
    </div>
  );
}
