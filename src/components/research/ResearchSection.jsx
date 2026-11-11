import React, { useState, useEffect } from 'react';
import {
  MacroVisual1,
  MacroVisual2,
  MacroVisual3,
  MacroVisual4Table,
  MacroVisual5
} from './MacroCharts';
import { getMacroText } from './macroI18n';
import { tx as txStr, useSiteLocale } from '../../i18n/localeService';

const GITHUB_RAW_BASE =
  'https://raw.githubusercontent.com/ale-camer/argentina-macro-pipeline/main/outputs';
const LOCAL_FALLBACK_BASE = '/data/macro';

export const RESEARCH_STUDIES = [
  {
    id: 'macro-argentina',
    colorAccent: '#f59e0b',
    colorRgb: '245, 158, 11'
  }
];

const OFFICIAL_SOURCES = [
  {
    id: 'wb_inflation',
    num: '01',
    nameEs: 'Banco Mundial — Inflación (Deflactor del PBI % anual)',
    nameEn: 'World Bank — Inflation (GDP Deflator annual %)',
    url: 'https://data.worldbank.org/indicator/NY.GDP.DEFL.KD.ZG?locations=AR'
  },
  {
    id: 'wb_gdp_growth',
    num: '02',
    nameEs: 'Banco Mundial — Crecimiento del PBI Real (% anual)',
    nameEn: 'World Bank — Real GDP Growth (annual %)',
    url: 'https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=AR'
  },
  {
    id: 'gasto_publico',
    num: '03',
    nameEs: 'Ministerio de Economía — Gasto Público Consolidado (% del PBI)',
    nameEn: 'Ministry of Economy — Consolidated Public Spending (% of GDP)',
    url: 'https://www.argentina.gob.ar/economia/politicaeconomica/macroeconomica/gastopublicoconsolidado'
  },
  {
    id: 'sipa_modalidades',
    num: '04',
    nameEs: 'SIPA / Secretaría de Trabajo — Situación y Evolución del Trabajo Registrado',
    nameEn: 'SIPA / Ministry of Labor — Registered Employment Evolution',
    url: 'https://www.argentina.gob.ar/trabajo/estadisticas'
  },
  {
    id: 'indec_salarios_vigente',
    num: '05',
    nameEs: 'INDEC — Índice de Salarios (empalme serie oct-2001 y base abr-2012=100)',
    nameEn: 'INDEC — Wage Index (linked Oct-2001 and Apr-2012=100 series)',
    url: 'https://www.indec.gob.ar/indec/web/Nivel4-Tema-4-31-61'
  },
  {
    id: 'indec_emae',
    num: '06',
    nameEs: 'INDEC — Estimador Mensual de Actividad Económica (EMAE base 2004=100)',
    nameEn: 'INDEC — Monthly Economic Activity Estimator (EMAE base 2004=100)',
    url: 'https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48'
  }
];

export default function ResearchSection({ lang = 'ES', onHudChange }) {
  useSiteLocale(lang);
  const [openId, setOpenId] = useState('macro-argentina');
  const [readingEssay, setReadingEssay] = useState(() => {
    const hash = window.location.hash.toLowerCase();
    const host = window.location.hostname.toLowerCase();
    return hash.includes('macro-argentina') || host.startsWith('macro.');
  });
  const [macroData, setMacroData] = useState(null);
  const [expandedChart, setExpandedChart] = useState(null);

  const tx = getMacroText(lang);

  const openFullEssay = () => {
    setReadingEssay(true);
    window.history.replaceState(null, '', '#analisis/macro-argentina');
  };

  // Navegación por teclado dentro de Análisis (Enter abre ensayo, Esc vuelve al resumen, ↑/↓ hace scroll)
  useEffect(() => {
    const handleKey = (e) => {
      const tag = document.activeElement?.tagName?.toLowerCase();
      if (tag === 'input' || tag === 'textarea') return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;

      if (!readingEssay && e.key === 'Enter') {
        e.preventDefault();
        openFullEssay();
      } else if (readingEssay && e.key === 'Escape') {
        e.preventDefault();
        e.stopPropagation();
        if (expandedChart !== null) {
          setExpandedChart(null);
        } else {
          setReadingEssay(false);
          window.history.replaceState(null, '', '#analisis');
        }
      } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        const scroller = document.querySelector('.sv-a-scroll');
        if (scroller) {
          e.preventDefault();
          scroller.scrollBy({ top: e.key === 'ArrowDown' ? 140 : -140, behavior: 'smooth' });
        }
      }
    };
    window.addEventListener('keydown', handleKey, true);
    return () => window.removeEventListener('keydown', handleKey, true);
  }, [readingEssay, expandedChart]);

  useEffect(() => {
    if (!onHudChange) return;
    if (readingEssay) {
      onHudChange({
        onBack: () => {
          setReadingEssay(false);
          window.history.replaceState(null, '', '#analisis');
        },
        backLabel: tx.backBtn,
        repoHref: 'https://github.com/ale-camer/argentina-macro-pipeline',
        repoLabel: tx.repoLink
      });
    } else {
      onHudChange(null);
    }
    return () => onHudChange(null);
  }, [readingEssay, tx.backBtn, tx.repoLink, onHudChange]);

  useEffect(() => {
    let active = true;

    async function loadPipelineData() {
      try {
        const dataRes = await fetch(`${GITHUB_RAW_BASE}/macro_argentina_latest.json`);
        if (!dataRes.ok) throw new Error('Fallback to local macro JSON');
        const d = await dataRes.json();
        if (active) setMacroData(d);
      } catch {
        try {
          const localData = await fetch(
            `${LOCAL_FALLBACK_BASE}/macro_argentina_latest.json`
          ).then((r) => r.json());
          if (active) setMacroData(localData);
        } catch {
          // Static defaults remain active if both fail
        }
      }
    }

    loadPipelineData();
    return () => {
      active = false;
    };
  }, []);

  const hm = macroData?.headline_metrics;
  const cutoffs = macroData?.sources_cutoff || {};
  const series = macroData?.series || {};
  const forecasts = macroData?.forecasts_6m_sarimax;

  if (readingEssay) {
    return (
      <div className="rs-root rs-essay-mode">
        {/* CABECERA DIRECTA DEL ESTUDIO */}
        <header className="rs-essay-hero">
          <h1 className="rs-essay-main-title">{tx.essayMainTitle}</h1>
          <p className="rs-essay-subtitle">{tx.essaySubtitle}</p>
        </header>

        {/* SECCIÓN 1: POLÍTICA ECONÓMICA Y CRECIMIENTO */}
        <article className="rs-essay-section">
          <div className="rs-essay-sec-header">
            <h2 className="rs-essay-sec-title">01. {tx.sec1Title}</h2>
          </div>

          <div className="rs-essay-prose">
            <p>{tx.sec1P1}</p>
            <p>{tx.sec1P2}</p>
            <p>{tx.sec1P3}</p>
          </div>

          <MacroVisual1
            series={series.visual_1_annual_macro}
            lang={lang}
            onExpand={() => setExpandedChart('v1')}
          />
        </article>

        {/* SECCIÓN 2: EMPLEO (CANTIDAD) */}
        <article className="rs-essay-section">
          <div className="rs-essay-sec-header">
            <h2 className="rs-essay-sec-title">02. {tx.sec2Title}</h2>
          </div>

          <div className="rs-essay-prose">
            <p>{tx.sec2P1}</p>
            <p>
              {tx.sec2P2(
                hm ? `${hm.correlation_jobs_emae_tc_pct}%` : '82.3%',
                hm ? hm.elasticity_employment_gdp_beta.toFixed(2) : '0.44'
              )}
            </p>
          </div>

          <MacroVisual2
            series={series.visual_2_monthly_activity_jobs}
            forecasts={forecasts}
            lang={lang}
            onExpand={() => setExpandedChart('v2')}
          />
        </article>

        {/* SECCIÓN 3: CALIDAD Y COMPOSICIÓN DEL EMPLEO */}
        <article className="rs-essay-section">
          <div className="rs-essay-sec-header">
            <h2 className="rs-essay-sec-title">03. {tx.sec3Title}</h2>
          </div>

          <div className="rs-essay-prose">
            <p>{tx.sec3P1}</p>
            <ul className="rs-essay-list">
              <li>{tx.sec3Li1(hm ? `${hm.demographic_gap_private_jobs_pp} pp` : '-22.5 pp')}</li>
              <li>{tx.sec3Li2}</li>
              <li>{tx.sec3Li3}</li>
            </ul>
            <p>{tx.sec3P2}</p>
          </div>

          <MacroVisual3
            series={series.visual_3_modalities_cumulative_pct}
            lang={lang}
            onExpand={() => setExpandedChart('v3')}
          />

          <MacroVisual4Table rows={series.visual_4_structural_shift_summary} lang={lang} />
        </article>

        {/* SECCIÓN 4: EMPLEO (PRECIO / SALARIO REAL) */}
        <article className="rs-essay-section">
          <div className="rs-essay-sec-header">
            <h2 className="rs-essay-sec-title">04. {tx.sec4Title}</h2>
          </div>

          <div className="rs-essay-prose">
            <p>{tx.sec4P1}</p>
            <p>{tx.sec4P2(hm ? hm.real_wage_index_2012_base100_latest : '75.39')}</p>
          </div>

          <MacroVisual5
            series={series.visual_5_real_wages_annual}
            lang={lang}
            onExpand={() => setExpandedChart('v5')}
          />
        </article>

        {/* SECCIÓN 5: PROYECCIÓN CUANTITATIVA SARIMAX (6 MESES) & FUENTES */}
        <article className="rs-essay-section rs-forecast-section">
          <div className="rs-essay-sec-header">
            <h2 className="rs-essay-sec-title">05. {tx.sec5Title}</h2>
          </div>

          {forecasts && (
            <div className="rs-forecast-grid">
              <div className="rs-forecast-card">
                <div className="rs-forecast-card-title">{tx.fcCard1}</div>
                <table className="rs-forecast-table">
                  <thead>
                    <tr>
                      <th>{tx.fcColPeriod}</th>
                      <th>{tx.fcColPoint}</th>
                      <th>{tx.fcColCi}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {forecasts.emae_des_idx_base2009?.map((row) => (
                      <tr key={row.period}>
                        <td>{row.period.slice(0, 7)}</td>
                        <td className="rs-fc-point">{row.point_forecast.toFixed(2)}</td>
                        <td className="rs-fc-ci">
                          [{row.ci95_low.toFixed(1)} – {row.ci95_high.toFixed(1)}]
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="rs-forecast-card">
                <div className="rs-forecast-card-title">{tx.fcCard2}</div>
                <table className="rs-forecast-table">
                  <thead>
                    <tr>
                      <th>{tx.fcColPeriod}</th>
                      <th>{tx.fcColPoint}</th>
                      <th>{tx.fcColCi}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {forecasts.private_jobs_idx_base2009?.map((row) => (
                      <tr key={row.period}>
                        <td>{row.period.slice(0, 7)}</td>
                        <td className="rs-fc-point">{row.point_forecast.toFixed(2)}</td>
                        <td className="rs-fc-ci">
                          [{row.ci95_low.toFixed(1)} – {row.ci95_high.toFixed(1)}]
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="rs-sources-box">
            <div className="rs-telemetry-title">{tx.sourcesTitle}</div>
            <div className="rs-sources-list">
              {OFFICIAL_SOURCES.map((s) => (
                <a
                  key={s.id}
                  href={s.url}
                  target="_blank"
                  rel="noreferrer"
                  className="rs-source-item"
                >
                  <span className="rs-source-num">{s.num}</span>
                  <span className="rs-source-name">{txStr(s.nameEs, s.nameEn, lang)}</span>
                  <span className="rs-source-cutoff">
                    {tx.cutoffLabel}: {cutoffs[s.id] || '2026'} ↗
                  </span>
                </a>
              ))}
            </div>
          </div>
        </article>

        {/* MODAL PANTALLA COMPLETA PARA GRÁFICOS NATIVOS */}
        {expandedChart && (
          <div className="rs-lightbox-backdrop" onClick={() => setExpandedChart(null)}>
            <div className="rs-lightbox-content" onClick={(e) => e.stopPropagation()}>
              <div className="rs-lightbox-header">
                <span>{tx.expandedHeader}</span>
                <button
                  type="button"
                  className="rs-lightbox-close"
                  onClick={() => setExpandedChart(null)}
                >
                  {tx.closeBtn}
                </button>
              </div>
              <div className="mc-expanded-body">
                {expandedChart === 'v1' && (
                  <MacroVisual1 series={series.visual_1_annual_macro} lang={lang} />
                )}
                {expandedChart === 'v2' && (
                  <MacroVisual2
                    series={series.visual_2_monthly_activity_jobs}
                    forecasts={forecasts}
                    lang={lang}
                  />
                )}
                {expandedChart === 'v3' && (
                  <MacroVisual3 series={series.visual_3_modalities_cumulative_pct} lang={lang} />
                )}
                {expandedChart === 'v5' && (
                  <MacroVisual5 series={series.visual_5_real_wages_annual} lang={lang} />
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  const toggleStudy = (id) => {
    setOpenId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="rs-root">
      {/* CABECERA CON EL PROPÓSITO DE ANÁLISIS / INVESTIGACIONES */}
      <div className="pj-purpose-header">
        <h2 className="tl-main-title">{tx.hubTitle}</h2>
        <p className="pj-purpose-lead">{tx.hubLead}</p>
      </div>

      {/* LISTA LIMPIA Y DIRECTA AL ENSAYO */}
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
              {/* FILA CABECERA CLICKEABLE SIN ETIQUETAS */}
              <button
                type="button"
                className="pj-acc-trigger"
                onClick={() => toggleStudy(study.id)}
                aria-expanded={isOpen}
              >
                <div className="pj-acc-trigger-left">
                  <span className="pj-git-node-dot" aria-hidden="true" />
                  <div className="pj-acc-titles">
                    <div className="pj-acc-title-row">
                      <span className="pj-acc-title">{tx.studyTitle}</span>
                    </div>
                    <span className="pj-acc-oneliner">{tx.studyOneLiner}</span>
                  </div>
                </div>

                <div className="pj-acc-trigger-right">
                  <span className={`pj-acc-chevron ${isOpen ? 'is-open' : ''}`} aria-hidden="true">
                    {isOpen ? '−' : '+'}
                  </span>
                </div>
              </button>

              {/* PANEL DESPLEGABLE LIMPIO: SOLO TESIS + BULLETS UNIFICADOS + BOTÓN */}
              {isOpen && (
                <div className="pj-acc-body">
                  <div className="pj-objective-banner">
                    <p className="pj-objective-text">{tx.thesisText}</p>
                  </div>

                  <div className="pj-body-main-row">
                    <ul className="pj-clean-bullets">
                      {tx.bullets.map((b) => {
                        const colonIdx = b.indexOf(':');
                        if (colonIdx > 0 && colonIdx < 60) {
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

                    <div className="pj-body-side-actions">
                      <button
                        type="button"
                        onClick={openFullEssay}
                        className="pj-repo-cta rs-open-essay-btn"
                        style={{
                          '--insp-accent': study.colorAccent,
                          '--insp-rgb': study.colorRgb
                        }}
                      >
                        <span>{tx.readCta}</span>
                      </button>
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
