import React, { useState } from 'react';

export const RESEARCH_STUDIES = [
  {
    id: 'macro-argentina',
    num: '01',
    hash: 'f81a3d',
    branch: 'research/macro-empleo-arg',
    title: 'Macroeconomía, Gasto Público y Degradación del Empleo en Argentina',
    oneLiner:
      'Radiografía empírica en 4 ejes (1961–Presente): inflación, gasto público/PBI, estancamiento privado y caída del salario real.',
    domain: 'Macroeconomía & Mercado Laboral',
    colorAccent: '#f59e0b',
    colorRgb: '245, 158, 11',
    thesis:
      'El estancamiento del PBI desde 2011 y el salto del gasto público/PBI financiando déficits con emisión no solo erosionaron el salario real, sino que ocultaron el freno del empleo asalariado privado detrás de un crecimiento artificial de modalidades precarizadas (Monotributo Social +160%) y empleo público (+30%).',
    metrics: [
      { label: 'Monotributo Social (2012→2022)', value: '+160%', accent: '#f43f5e', note: 'Mayor expansión relativa del padrón' },
      { label: 'Empleo Público (2012→2022)', value: '+30%', accent: '#f59e0b', note: 'Crecimiento por encima de la población' },
      { label: 'Participación Privada Formal', value: '55.9% → 48.2%', accent: '#38bdf8', note: 'Pérdida de peso en el total registrado' },
      { label: 'Correlación PBI vs. Empleo Privado', value: 'r > 0.85', accent: '#10b981', note: 'Sin crecimiento del PBI no hay empleo privado' }
    ],
    barsTitle: 'VARIACIÓN ACUMULADA Y COMPOSICIÓN POR MODALIDAD LABORAL (SIPA / MTEySS)',
    bars: [
      { name: 'Monotributo Social (Subsidiado)', share2012: '1.5%', share2022: '3.4%', delta: '+160%', pctWidth: 100, color: '#f43f5e' },
      { name: 'Monotributo Estándar', share2012: '12.0%', share2022: '14.8%', delta: '+45%', pctWidth: 48, color: '#f59e0b' },
      { name: 'Empleo Sector Público', share2012: '23.3%', share2022: '26.1%', delta: '+30%', pctWidth: 36, color: '#a855f7' },
      { name: 'Asalariados Sector Privado', share2012: '55.9%', share2022: '48.2%', delta: '+1.8%', pctWidth: 10, color: '#10b981' },
      { name: 'Trabajadores Autónomos', share2012: '3.8%', share2022: '3.1%', delta: '-4.2%', pctWidth: 8, color: '#38bdf8' }
    ],
    bullets: [
      'Eje 1 (Políticas, Gasto e Inflación desde 1961): Tres regímenes macroeconómicos marcados por la duplicación del gasto público/PBI en los 2000s sin contraparte sostenible de producto.',
      'Eje 2 y 3 (Cantidad y Calidad del Empleo): El empleo privado registrado quedó virtualmente congelado desde 2012 mientras la población activa creció ~18%.',
      'Eje 4 (Precio / Salario Real desde 2001): Aceleración inflacionaria que licúa sistemáticamente el poder adquisitivo tanto del sector privado como del público.'
    ],
    tags: ['Macroeconomía Argentina', 'Series de Tiempo', 'SIPA / INDEC', 'Política Fiscal', 'Mercado Laboral']
  },
  {
    id: 'quant-sp500-clustering',
    num: '02',
    hash: '9c4e12',
    branch: 'research/sp500-kmeans-backtest',
    title: 'Segmentación Cuantitativa y Backtesting Algorítmico sobre el S&P 500',
    oneLiner:
      'Comparativa de clustering (K-Means, Equiprobable y Equidistante) por ratios de riesgo/retorno para rotación sistemática de carteras.',
    domain: 'Quant Finance • UCEMA',
    colorAccent: '#10b981',
    colorRgb: '16, 185, 129',
    thesis:
      'Desarrollado en el programa ejecutivo de Finanzas Cuantitativas (UCEMA): evaluar si la segmentación periódica de acciones del S&P 500 mediante K-Means y cuantiles estadísticos permite aislar clústeres con mejor relación retorno/varianza que el índice bajo una estrategia sistemática.',
    metrics: [
      { label: 'Universo Analizado', value: 'S&P 500', accent: '#10b981', note: 'Series históricas de precios ajustados' },
      { label: 'Métodos de Segmentación', value: '3 Motores', accent: '#38bdf8', note: 'K-Means, Equiprobable y Equidistante' },
      { label: 'Métricas de Selección', value: '6 Ratios', accent: '#a855f7', note: 'Return, Risk, Sharpe, Sortino, Calmar, IR' },
      { label: 'Mejor Consistencia', value: 'K-Means + IR', accent: '#f59e0b', note: 'Alto rendimiento con baja varianza transversal' }
    ],
    barsTitle: 'DESEMPEÑO RELATIVO Y ESTABILIDAD POR MÉTODO DE SEGMENTACIÓN Y MÉTRICA',
    bars: [
      { name: 'K-Means • Information Ratio & Risk', share2012: 'Baja Var.', share2022: 'Alta Consistencia', delta: 'Óptimo', pctWidth: 92, color: '#10b981' },
      { name: 'Equiprobable • Sortino & Calmar Ratio', share2012: 'Baja Var.', share2022: 'Buen Downside', delta: 'Sólido', pctWidth: 78, color: '#38bdf8' },
      { name: 'Equidistante • Concentración en Outliers', share2012: 'Alta Var.', share2022: 'Pocos Tickers', delta: 'Volátil', pctWidth: 46, color: '#f43f5e' }
    ],
    bullets: [
      'Las métricas de Riesgo e Information Ratio combinadas con K-Means mostraron el mayor rendimiento medio con la menor varianza entre regímenes.',
      'El método Equiprobable destacó al seleccionar por Sortino y Calmar Ratio (penalización de volatilidad negativa y máximo drawdown).',
      'La segmentación Equidistante exhibió retornos nominales extremos pero alta inestabilidad por concentrar la cartera en muy pocos activos.'
    ],
    tags: ['Quant Finance', 'S&P 500', 'K-Means Clustering', 'Sharpe / Sortino / Calmar', 'Backtesting', 'UCEMA']
  },
  {
    id: 'nlp-ds-labour-market',
    num: '03',
    hash: '3b70e9',
    branch: 'research/nlp-labour-clustering',
    title: 'Radiografía NLP y Clustering del Mercado Laboral en Data Science & Engineering',
    oneLiner:
      'Scraping, distribución de seniority/remoto y clustering K-Means + N-Grams sobre ofertas reales de Data Science y Data Engineering.',
    domain: 'NLP & People Analytics',
    colorAccent: '#a855f7',
    colorRgb: '168, 85, 247',
    thesis:
      'Más allá del discurso general sobre la demanda en ciencia de datos, el análisis NLP de avisos reales muestra un mercado fuertemente sesgado hacia perfiles Senior/Mid con trabajo remoto consolidado y dividido en 3 clústeres técnicos bien diferenciados.',
    metrics: [
      { label: 'Modalidad 100% Remota', value: '74%', accent: '#10b981', note: '+22% en esquema híbrido' },
      { label: 'Vacantes Entry-Level', value: 'Solo 2%', accent: '#f43f5e', note: 'Fuerte barrera de entrada sin experiencia' },
      { label: 'Clústeres Detectados (K-Means)', value: '3 Perfiles', accent: '#a855f7', note: 'Cloud/DE, Core ML+SQL y BI/Analytics' },
      { label: 'Requisito de Viaje', value: '20%', accent: '#38bdf8', note: 'Concentrado en consultoría y liderazgo' }
    ],
    barsTitle: 'DISTRIBUCIÓN ESTRUCTURAL DE LAS OFERTAS ANALIZADAS (NLP & CLUSTERING)',
    bars: [
      { name: 'Trabajo 100% Remoto', share2012: 'Modalidad', share2022: 'Predominante', delta: '74%', pctWidth: 74, color: '#10b981' },
      { name: 'Esquema Híbrido', share2012: 'Modalidad', share2022: 'Flexible', delta: '22%', pctWidth: 22, color: '#38bdf8' },
      { name: 'Posiciones Entry-Level / Junior', share2012: 'Seniority', share2022: 'Cuello de botella', delta: '2%', pctWidth: 6, color: '#f43f5e' }
    ],
    bullets: [
      'Taxonomía automática de títulos en 3 ejes: Rol (Engineer, Scientist, Analyst, Architect), Nivel (Senior, Lead, Manager) y Dominio.',
      'Extracción de unigramas y bigramas sobre descripciones completas para aislar las combinaciones de herramientas que co-ocurren en producción.',
      'Clustering K-Means que separa claramente el perfil Cloud/Data Engineering (Azure/Pipelines) del perfil de Modelado Estadístico + SQL.'
    ],
    tags: ['NLP', 'K-Means Clustering', 'Web Scraping', 'N-Grams / TF-IDF', 'Data Market Trends']
  }
];

export default function ResearchSection() {
  const [openId, setOpenId] = useState('macro-argentina');

  const toggleStudy = (id) => {
    setOpenId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="rs-root">
      {/* CABECERA CON EL PROPÓSITO DE ANÁLISIS / INVESTIGACIONES */}
      <div className="pj-purpose-header">
        <div className="tl-eyebrow">SYS.RESEARCH // ANÁLISIS AD-HOC CON DATOS Y TESIS PROPIA</div>
        <h2 className="tl-main-title">
          Investigaciones cuantitativas y económicas construidas desde datos primarios
        </h2>
        <p className="pj-purpose-lead">
          Estudios realizados a pulmón cruzando series oficiales, mercados financieros y lenguaje
          natural para responder preguntas concretas con <strong>criterio de dominio</strong>. Hacé
          click en cada investigación para desplegar su tesis, métricas clave y hallazgos.
        </p>
      </div>

      {/* LISTA EXPANDIBLE ESTILO GIT MINIMAL */}
      <div className="pj-acc-list mode-git">
        {RESEARCH_STUDIES.map((study) => {
          const isOpen = openId === study.id;

          return (
            <div
              key={study.id}
              className={`pj-acc-item mode-v2 ${isOpen ? 'is-open' : ''}`}
              style={{
                '--item-accent': study.colorAccent,
                '--item-rgb': study.colorRgb
              }}
            >
              {/* FILA CABECERA CLICKEABLE */}
              <button
                type="button"
                className="pj-acc-trigger"
                onClick={() => toggleStudy(study.id)}
                aria-expanded={isOpen}
              >
                <div className="pj-acc-trigger-left">
                  <span className="pj-git-node-dot" aria-hidden="true" />
                  <span className="pj-acc-code">study {study.hash}</span>
                  <div className="pj-acc-titles">
                    <div className="pj-acc-title-row">
                      <span className="pj-acc-title">{study.title}</span>
                      <span className="pj-git-branch-pill">{study.branch}</span>
                    </div>
                    <span className="pj-acc-oneliner">{study.oneLiner}</span>
                  </div>
                </div>

                <div className="pj-acc-trigger-right">
                  <div className="pj-acc-preview-tags">
                    {study.tags.slice(0, 3).map((t) => (
                      <span key={t} className="tl-tag-pill">
                        {t}
                      </span>
                    ))}
                  </div>

                  <span className={`pj-acc-chevron ${isOpen ? 'is-open' : ''}`} aria-hidden="true">
                    {isOpen ? '−' : '+'}
                  </span>
                </div>
              </button>

              {/* PANEL DESPLEGABLE DEL ESTUDIO */}
              {isOpen && (
                <div className="pj-acc-body">
                  {/* TESIS CENTRAL DEL ESTUDIO */}
                  <div className="pj-objective-banner">
                    <span className="pj-objective-tag">TESIS CENTRAL & HALLAZGO ESTRUCTURAL</span>
                    <p className="pj-objective-text">{study.thesis}</p>
                  </div>

                  {/* 4 KPIs / MÉTRICAS RÁPIDAS */}
                  <div className="rs-metrics-grid">
                    {study.metrics.map((m) => (
                      <div key={m.label} className="rs-metric-card">
                        <span className="rs-metric-value" style={{ color: m.accent }}>
                          {m.value}
                        </span>
                        <span className="rs-metric-label">{m.label}</span>
                        <span className="rs-metric-note">{m.note}</span>
                      </div>
                    ))}
                  </div>

                  {/* VISUALIZACIÓN COMPACTA DE BARRAS TELEMÉTRICAS */}
                  <div className="rs-telemetry-box">
                    <div className="rs-telemetry-title">{study.barsTitle}</div>
                    <div className="rs-bars-list">
                      {study.bars.map((b) => (
                        <div key={b.name} className="rs-bar-row">
                          <div className="rs-bar-meta">
                            <span className="rs-bar-name">{b.name}</span>
                            <span className="rs-bar-shares">
                              {b.share2012} → {b.share2022}
                            </span>
                            <span className="rs-bar-delta" style={{ color: b.color }}>
                              {b.delta}
                            </span>
                          </div>
                          <div className="rs-bar-track">
                            <div
                              className="rs-bar-fill"
                              style={{
                                width: `${b.pctWidth}%`,
                                background: b.color
                              }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* 3 CONCLUSIONES PUNTUALES + TAGS */}
                  <div className="pj-body-main-row">
                    <ul className="pj-clean-bullets">
                      {study.bullets.map((b) => (
                        <li key={b}>{b}</li>
                      ))}
                    </ul>

                    <div className="pj-body-side-actions">
                      <div className="pj-all-tags">
                        {study.tags.map((t) => (
                          <span key={t} className="tl-tag-pill">
                            {t}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

