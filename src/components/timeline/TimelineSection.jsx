import React, { useState } from 'react';

export const WORK_ITEMS = [
  {
    id: 'tongo',
    role: 'Data Engineer',
    company: 'Tongo (Fintech Startup)',
    scope: 'Estados Unidos (Remoto)',
    start: 2025.8,
    end: 2026.8,
    period: '12/2025 – Presente',
    colorAccent: '#f43f5e',
    colorRgb: '244, 63, 94',
    bullets: [
      'Arquitectura y escalado de la plataforma de datos fintech usando Snowflake (SQL avanzado) y Airflow, integrando Fivetran, Airbyte y HubSpot.',
      'Implementación de automatizaciones impulsadas por IA (Make) y soluciones de BI en Superset como primer profesional de datos de la compañía.',
      'Optimización extrema del flujo hacia CRM y BI, reduciendo el volumen diario de registros procesados de cientos de miles a menos de 100 para la operativa diaria.'
    ]
  },
  {
    id: 'siemens',
    role: 'Data Engineer (Consulting)',
    company: 'Siemens Advanta',
    scope: 'España (Remoto)',
    start: 2024.9,
    end: 2025.8,
    period: '02/2025 – 11/2025',
    colorAccent: '#f43f5e',
    colorRgb: '244, 63, 94',
    bullets: [
      'Ingeniería de pipelines ETL en Databricks procesando miles de millones de registros en segundos con Apache Spark, Python y SQL, optimizando DAGs mediante particionado y estrategias incrementales.',
      'Construcción y mantenimiento de flujos productivos integrados con Azure Data Factory y Azure Blob Storage para automatizar procesos a gran escala entre entornos.',
      'Desarrollo de más de 30 reportes financieros en Power BI sobre modelos estrella (Star Schema) y medidas DAX para clientes Fortune 500 de consumo masivo.'
    ]
  },
  {
    id: 'abinbev',
    role: 'Data Scientist (Fraud & Pricing)',
    company: 'AB InBev',
    scope: 'Bruselas, Bélgica (Remoto)',
    start: 2023.2,
    end: 2024.9,
    period: '08/2023 – 01/2025',
    colorAccent: '#a855f7',
    colorRgb: '168, 85, 247',
    bullets: [
      'Responsable de la infraestructura de datos de fraude en LATAM, construyendo más de 25 pipelines productivos en Databricks y Snowflake para procesar millones de transacciones semanales y reducir tiempos de horas a segundos.',
      'Desarrollo de modelos de detección de fraude (Isolation Forest) que incrementaron la precisión y mejoraron la rentabilidad hasta un 3% en los mercados más críticos.',
      'Diseño y ejecución de experimentos de optimización de precios (A/B testing y RCTs), impulsando el volumen de ventas hasta un 0.5% en mercados principales, junto a dashboards ejecutivos para el C-suite.'
    ]
  },
  {
    id: 'lumen',
    role: 'Data Scientist (Corporate Finance)',
    company: 'Lumen Technologies',
    scope: 'Buenos Aires, Argentina (Híbrido)',
    start: 2021.8,
    end: 2023.2,
    period: '11/2021 – 07/2023',
    colorAccent: '#a855f7',
    colorRgb: '168, 85, 247',
    bullets: [
      'Construcción de más de 10 pipelines ETL con Talend, Python y SQL para alimentar y automatizar tableros en Power BI utilizados por más de 50 stakeholders de finanzas y liderazgo.',
      'Proyección de pagos y estimación de riesgo de default mediante Random Forests; modelado de flujo de caja con técnicas de regresión para planificación financiera.',
      'Aplicación de NLP sobre encuestas de salida con NLTK y spaCy para identificar causas de rotación, permitiendo a RR.HH. diseñar políticas de retención más allá de incentivos monetarios.'
    ]
  },
  {
    id: 'balanz',
    role: 'Quantitative Analyst (Algorithmic Trading)',
    company: 'Balanz Capital',
    scope: 'Buenos Aires, Argentina (Híbrido)',
    start: 2021.0,
    end: 2021.8,
    period: '02/2021 – 10/2021',
    colorAccent: '#10b981',
    colorRgb: '16, 185, 129',
    bullets: [
      'Desarrollo y backtesting de estrategias de trading algorítmico utilizando Python y redes neuronales LSTM para los mercados de Argentina y Estados Unidos.',
      'Construcción de visualizaciones cuantitativas avanzadas (superficies y sonrisas de volatilidad) con Plotly y Seaborn para la toma de decisiones de la mesa de trading.'
    ]
  },
  {
    id: 'portfolio-manager-indep',
    role: 'Independent Portfolio Manager',
    company: 'Independiente',
    scope: 'Mercado de Capitales • Asset Management',
    start: 2018.1,
    end: 2021.0,
    period: '2018 – 2021',
    colorAccent: '#10b981',
    colorRgb: '16, 185, 129',
    bullets: [
      'Gestión y administración independiente de carteras de inversión, asignación estratégica y táctica de activos en renta fija, renta variable y derivados.',
      'Diseño de estrategias cuantitativas de cobertura cambiaria y de tasas, control de drawdown y seguimiento sistemático de retornos ajustados por riesgo.'
    ]
  },
  {
    id: 'bestday',
    role: 'Semi Senior Treasury Analyst (South America)',
    company: 'Best Day Travel Group',
    scope: 'Sudamérica • Finanzas Corporativas',
    start: 2015.3,
    end: 2018.1,
    period: '2015 – 2018',
    colorAccent: '#f59e0b',
    colorRgb: '245, 158, 11',
    bullets: [
      'Gestión de tesorería regional, flujo de caja multimoneda y exposición cambiaria (FX) para las operaciones de Sudamérica.',
      'Automatización de conciliaciones bancarias, reportes de liquidez y planificación financiera operativa.'
    ]
  }
];

export const EDU_ITEMS = [
  {
    id: 'ucema',
    degree: 'Executive Program in Quantitative Finance',
    school: 'Universidad del CEMA (UCEMA)',
    scope: 'Posgrado en Finanzas Cuantitativas',
    start: 2022.2,
    end: 2023.0,
    period: '2022',
    colorAccent: '#10b981',
    colorRgb: '16, 185, 129',
    bullets: [
      'Cálculo estocástico, valoración de derivados, estructura temporal de tasas de interés y modelos cuantitativos de riesgo.',
      'Investigación aplicada en segmentación cuantitativa (K-Means) y backtesting algorítmico sobre activos del S&P 500.'
    ]
  },
  {
    id: 'uba-ds',
    degree: 'Master’s Degree in Data Science (MSc)',
    school: 'Universidad de Buenos Aires (UBA)',
    scope: 'Maestría en Ciencia de Datos',
    start: 2020.2,
    end: 2022.1,
    period: '2020 – 2021',
    colorAccent: '#a855f7',
    colorRgb: '168, 85, 247',
    bullets: [
      'Aprendizaje estadístico, Machine Learning, procesamiento de lenguaje natural (NLP), series de tiempo y minería de grandes volúmenes de datos.',
      'Álgebra lineal computacional, optimización y arquitectura de modelos predictivos.'
    ]
  },
  {
    id: 'uba-fin',
    degree: 'Master’s Degree in Finance (Corporate Finance)',
    school: 'Universidad de Buenos Aires (UBA)',
    scope: 'Maestría en Finanzas Corporativas',
    start: 2018.2,
    end: 2020.1,
    period: '2018 – 2019',
    colorAccent: '#f59e0b',
    colorRgb: '245, 158, 11',
    bullets: [
      'Valuación de empresas, mercado de capitales, estructura de capital, fusiones y adquisiciones (M&A) y evaluación de proyectos de inversión.',
      'Modelado financiero avanzado, análisis de riesgo crediticio y gestión de portafolios corporativos.'
    ]
  },
  {
    id: 'unlz',
    degree: 'Bachelor’s Degree in Business Administration (BSc)',
    school: 'Universidad Nacional de Lomas de Zamora (UNLZ)',
    scope: 'Licenciatura en Administración',
    start: 2011.0,
    end: 2017.6,
    period: '2011 – 2017',
    colorAccent: '#f59e0b',
    colorRgb: '245, 158, 11',
    bullets: [
      'Formación de grado en administración, economía, estadística, matemática financiera, contabilidad gerencial y dirección estratégica.'
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

const WORK_CLEAN_PCTS = computeDeoverlappedPcts(WORK_ITEMS, 12.8, 6.0, 92.5);
const EDU_CLEAN_PCTS = computeDeoverlappedPcts(EDU_ITEMS, 17.5, 19.0, 82.0);

function buildDagConnectorPath(side, labelY, midPct) {
  const isLeft = side === 'left';
  const xStart = isLeft ? 0 : 100;
  const xEnd = isLeft ? 100 : 0;
  const c1 = isLeft ? 55 : 45;
  const c2 = isLeft ? 45 : 55;
  return `M ${xStart} ${labelY} C ${c1} ${labelY}, ${c2} ${midPct}, ${xEnd} ${midPct}`;
}

export default function TimelineSection() {
  const [selectedId, setSelectedId] = useState('tongo');

  const selectedItem = ALL_ITEMS.find((it) => it.id === selectedId) || ALL_ITEMS[0];
  const activeSpanTop = getTopPct(selectedItem.end);
  const activeSpanHeight = getHeightPct(selectedItem.start, selectedItem.end);

  return (
    <div className="tl-root">
      {/* CABECERA DE RECORRIDO */}
      <div className="tl-header-bar">
        <div className="tl-header-copy">
          <div className="tl-eyebrow">2011 – 2026 • TRAYECTORIA PROFESIONAL Y ACADÉMICA</div>
          <h2 className="tl-main-title">
            Negocios & Finanzas → Data Science → Data & AI Engineering
          </h2>
        </div>
      </div>

      {/* ESCENARIO DAG DE DOBLE EJE */}
      <div className="tl-stage-box scifi-dag">
        <span className="tl-hud-corner tl-corner-tl" aria-hidden="true" />
        <span className="tl-hud-corner tl-corner-tr" aria-hidden="true" />
        <span className="tl-hud-corner tl-corner-bl" aria-hidden="true" />
        <span className="tl-hud-corner tl-corner-br" aria-hidden="true" />

        <div className="tl-d1-col-headers">
          <span className="tl-col-pill">EXPERIENCIA LABORAL</span>
          <span className="tl-col-axis-label">2026 ↓ 2011</span>
          <span className="tl-col-pill">EDUCACIÓN</span>
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
                    onClick={() => setSelectedId(item.id)}
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
                        stroke="#ffffff"
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
                    onClick={() => setSelectedId(item.id)}
                  >
                    <div className="tl-node-main-row">
                      <div className="tl-node-titles">
                        <span className="tl-node-role">{item.role}</span>
                        <span className="tl-node-org">{item.company}</span>
                      </div>
                      <span className="tl-node-period-badge">{item.period}</span>
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
                    onClick={() => setSelectedId(item.id)}
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
                        stroke="#ffffff"
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
                    onClick={() => setSelectedId(item.id)}
                  >
                    <div className="tl-node-main-row">
                      <div className="tl-node-titles">
                        <span className="tl-node-role">{item.degree}</span>
                        <span className="tl-node-org">{item.school}</span>
                      </div>
                      <span className="tl-node-period-badge">{item.period}</span>
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
              • {selectedItem.subtitle} ({selectedItem.scope})
            </span>
          </div>
          <span className="tl-insp-period">{selectedItem.period}</span>
        </div>

        <ul className="pj-clean-bullets">
          {selectedItem.bullets.map((b) => (
            <li key={b}>{b}</li>
          ))}
        </ul>
      </footer>
    </div>
  );
}
