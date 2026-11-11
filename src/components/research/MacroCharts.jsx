import React, { useState } from 'react';
import { getMacroText } from './macroI18n';

function fmt(val, decimals = 1) {
  if (val === null || val === undefined || Number.isNaN(Number(val))) return 'N/D';
  return Number(val).toFixed(decimals);
}

function buildPath(points) {
  if (!points.length) return '';
  return points
    .map((p, i) => `${i === 0 ? 'M' : 'L'}${p[0].toFixed(1)},${p[1].toFixed(1)}`)
    .join(' ');
}

function buildArea(points, baselineY) {
  if (!points.length) return '';
  const firstX = points[0][0].toFixed(1);
  const lastX = points[points.length - 1][0].toFixed(1);
  return `${buildPath(points)} L${lastX},${baselineY.toFixed(1)} L${firstX},${baselineY.toFixed(1)} Z`;
}

/* ==========================================================================
   VISUAL 1: PBI REAL, GASTO PÚBLICO E INFLACIÓN (1980–2025)
   ========================================================================== */
export function MacroVisual1({ series, lang = 'ES', onExpand }) {
  const t = getMacroText(lang);
  const [hoverIdx, setHoverIdx] = useState(null);

  if (!series?.year?.length) return null;

  const years = series.year;
  const gdpIdx = series.gdp_index_1980;
  const pubExp = series.pub_exp_pct_gdp;
  const inflRaw = series.inflation_pct;
  const gdpGrowth = series.gdp_growth_pct;
  const n = years.length;

  const W = 940;
  const H = 500;
  const padL = 56;
  const padR = 54;
  const plotW = W - padL - padR;

  const topY0 = 62;
  const topY1 = 295;
  const topH = topY1 - topY0;
  const maxTopVal = 240;

  const botY0 = 345;
  const botY1 = 468;
  const botH = botY1 - botY0;
  const minG = -12;
  const maxG = 12;

  const xOf = (i) => padL + (i / (n - 1)) * plotW;
  const yTop = (v) => topY1 - (Math.min(maxTopVal, Math.max(0, Number(v) || 0)) / maxTopVal) * topH;
  const yBot = (v) => {
    const clamped = Math.max(minG, Math.min(maxG, Number(v) || 0));
    return botY1 - ((clamped - minG) / (maxG - minG)) * botH;
  };
  const zeroBotY = yBot(0);

  const gdpPts = years
    .map((_, i) => (gdpIdx[i] != null ? [xOf(i), yTop(gdpIdx[i])] : null))
    .filter(Boolean);
  const expPts = years
    .map((_, i) => (pubExp[i] != null ? [xOf(i), yTop(pubExp[i])] : null))
    .filter(Boolean);
  const infPts = years
    .map((_, i) =>
      inflRaw[i] != null ? [xOf(i), yTop(Math.min(100, Math.max(0, inflRaw[i])))] : null
    )
    .filter(Boolean);

  const idxOfYear = (yr) => Math.max(0, years.indexOf(yr));
  const x1990 = xOf(idxOfYear(1990));
  const x1991 = xOf(idxOfYear(1991));
  const x2001 = xOf(idxOfYear(2001));
  const x2011 = xOf(idxOfYear(2011));
  const xLast = xOf(n - 1);

  return (
    <figure className="mc-card">
      <div className="mc-header">
        <div className="mc-header-titles">
          <h3 className="mc-title">{t.v1Title}</h3>
          <p className="mc-subtitle">{t.v1Sub}</p>
        </div>
        {onExpand && (
          <button type="button" className="mc-expand-btn" onClick={onExpand}>
            {t.zoomBtn}
          </button>
        )}
      </div>

      {/* LEYENDA EXTERNA (CERO SOLAPAMIENTO) */}
      <div className="mc-legend-row">
        <span className="mc-legend-item">
          <i className="mc-dot" style={{ background: '#38bdf8' }} />
          {t.v1LegendGdp}
        </span>
        <span className="mc-legend-item">
          <i className="mc-dot" style={{ background: '#f59e0b' }} />
          {t.v1LegendExp}
        </span>
        <span className="mc-legend-item">
          <i className="mc-dot" style={{ background: '#f43f5e' }} />
          {t.v1LegendInf}
        </span>
      </div>

      <div className="mc-svg-wrap">
        <svg viewBox={`0 0 ${W} ${H}`} className="mc-svg">
          {/* FRANJAS DE RÉGIMEN EN BANDA SUPERIOR RESERVADA */}
          <g>
            <rect
              x={padL}
              y={8}
              width={x1990 - padL}
              height={42}
              rx={5}
              className="mc-regime-box mc-regime-red"
            />
            <text x={(padL + x1990) / 2} y={24} textAnchor="middle" className="mc-regime-title">
              {t.v1Regime1}
            </text>
            <text x={(padL + x1990) / 2} y={40} textAnchor="middle" className="mc-regime-sub">
              {t.v1Regime1Sub}
            </text>

            <rect
              x={x1991}
              y={8}
              width={x2001 - x1991}
              height={42}
              rx={5}
              className="mc-regime-box mc-regime-green"
            />
            <text x={(x1991 + x2001) / 2} y={24} textAnchor="middle" className="mc-regime-title">
              {t.v1Regime2}
            </text>
            <text x={(x1991 + x2001) / 2} y={40} textAnchor="middle" className="mc-regime-sub">
              {t.v1Regime2Sub}
            </text>

            <rect
              x={x2011}
              y={8}
              width={xLast - x2011}
              height={42}
              rx={5}
              className="mc-regime-box mc-regime-amber"
            />
            <text x={(x2011 + xLast) / 2} y={24} textAnchor="middle" className="mc-regime-title">
              {t.v1Regime3}
            </text>
            <text x={(x2011 + xLast) / 2} y={40} textAnchor="middle" className="mc-regime-sub">
              {t.v1Regime3Sub}
            </text>
          </g>

          {/* GRILLA PANEL SUPERIOR */}
          {[0, 50, 100, 150, 200].map((v) => {
            const y = yTop(v);
            return (
              <g key={v}>
                <line x1={padL} y1={y} x2={W - padR} y2={y} className="mc-grid-line" />
                <text x={padL - 8} y={y + 4} textAnchor="end" className="mc-axis-text">
                  {v}
                </text>
                {v <= 100 && (
                  <text x={W - padR + 8} y={y + 4} textAnchor="start" className="mc-axis-text">
                    {v}%
                  </text>
                )}
              </g>
            );
          })}

          {/* ÁREAS Y CURVAS PANEL SUPERIOR */}
          <path d={buildArea(infPts, topY1)} fill="rgba(244, 63, 94, 0.10)" />
          <path d={buildArea(expPts, topY1)} fill="rgba(245, 158, 11, 0.14)" />
          <path d={buildPath(infPts)} fill="none" stroke="#f43f5e" strokeWidth="2" strokeDasharray="4 3" />
          <path d={buildPath(expPts)} fill="none" stroke="#f59e0b" strokeWidth="2.5" />
          <path d={buildPath(gdpPts)} fill="none" stroke="#38bdf8" strokeWidth="3" />

          {/* SUBTÍTULO PANEL INFERIOR */}
          <text x={padL} y={330} className="mc-panel-label">
            {t.v1BarTitle}
          </text>

          {/* GRILLA PANEL INFERIOR */}
          {[-10, -5, 0, 5, 10].map((v) => {
            const y = yBot(v);
            return (
              <g key={v}>
                <line
                  x1={padL}
                  y1={y}
                  x2={W - padR}
                  y2={y}
                  className={v === 0 ? 'mc-zero-line' : 'mc-grid-line'}
                />
                <text x={padL - 8} y={y + 4} textAnchor="end" className="mc-axis-text">
                  {v}%
                </text>
              </g>
            );
          })}

          {/* BARRAS DE CRECIMIENTO ANUAL PBI */}
          {years.map((yr, i) => {
            const g = Number(gdpGrowth[i]) || 0;
            const x = xOf(i);
            const bw = Math.max(6, plotW / n - 4);
            const yVal = yBot(g);
            const top = Math.min(zeroBotY, yVal);
            const h = Math.max(1.5, Math.abs(yVal - zeroBotY));
            const isPos = g >= 0;

            return (
              <g key={yr}>
                <rect
                  x={x - bw / 2}
                  y={top}
                  width={bw}
                  height={h}
                  rx={1.5}
                  fill={isPos ? '#10b981' : '#f43f5e'}
                  opacity={hoverIdx === i ? 1 : 0.82}
                />
                {yr % 5 === 0 && (
                  <text x={x} y={H - 10} textAnchor="middle" className="mc-axis-text">
                    {yr}
                  </text>
                )}
                <rect
                  x={x - plotW / n / 2}
                  y={topY0}
                  width={plotW / n}
                  height={botY1 - topY0}
                  fill="transparent"
                  onMouseEnter={() => setHoverIdx(i)}
                  onMouseLeave={() => setHoverIdx(null)}
                />
              </g>
            );
          })}

          {/* CROSSHAIR INTERACTIVO */}
          {hoverIdx !== null && (
            <g pointerEvents="none">
              <line
                x1={xOf(hoverIdx)}
                y1={topY0}
                x2={xOf(hoverIdx)}
                y2={botY1}
                stroke="#f59e0b"
                strokeWidth="1"
                strokeDasharray="3 3"
              />
              {gdpIdx[hoverIdx] != null && (
                <circle cx={xOf(hoverIdx)} cy={yTop(gdpIdx[hoverIdx])} r={4.5} fill="#38bdf8" />
              )}
              {pubExp[hoverIdx] != null && (
                <circle cx={xOf(hoverIdx)} cy={yTop(pubExp[hoverIdx])} r={4.5} fill="#f59e0b" />
              )}
            </g>
          )}
        </svg>

        {hoverIdx !== null && (
          <div className="mc-tooltip">
            <strong>{years[hoverIdx]}</strong>
            <span>
              {t.v1LegendGdp}: <b>{fmt(gdpIdx[hoverIdx], 1)}</b> (
              {Number(gdpGrowth[hoverIdx]) >= 0 ? '+' : ''}
              {fmt(gdpGrowth[hoverIdx], 1)}%)
            </span>
            <span>
              {t.v1LegendExp}:{' '}
              <b>{pubExp[hoverIdx] != null ? `${fmt(pubExp[hoverIdx], 1)}%` : 'N/D'}</b>
            </span>
            <span>
              {t.v1LegendInf}: <b>{fmt(inflRaw[hoverIdx], 1)}%</b>
            </span>
          </div>
        )}
      </div>

      <figcaption className="mc-caption">{t.v1Caption}</figcaption>
    </figure>
  );
}

/* ==========================================================================
   VISUAL 2: EMPLEO PRIVADO VS. EMAE + PROYECCIÓN SARIMAX (2009–2026)
   ========================================================================== */
export function MacroVisual2({ series, forecasts, lang = 'ES', onExpand }) {
  const t = getMacroText(lang);
  const [hoverIdx, setHoverIdx] = useState(null);

  if (!series?.period?.length) return null;

  const periods = series.period;
  const jobsIdx = series.jobs_idx_2009;
  const emaeOrig = series.emae_orig_idx_2009;
  const emaeDes = series.emae_des_idx_2009;
  const emaeTc = series.emae_tc_idx_2009;
  const fcEmae = forecasts?.emae_des_idx_base2009 || [];
  const fcJobs = forecasts?.private_jobs_idx_base2009 || [];

  const nHist = periods.length;
  const nTotal = nHist + fcEmae.length;

  const W = 940;
  const H = 400;
  const padL = 54;
  const padR = 46;
  const topY = 66;
  const botY = 356;
  const plotW = W - padL - padR;
  const plotH = botY - topY;

  const minY = 85;
  const maxY = 145;

  const xOf = (i) => padL + (i / (nTotal - 1)) * plotW;
  const yOf = (v) =>
    botY - ((Math.max(minY, Math.min(maxY, Number(v) || 100)) - minY) / (maxY - minY)) * plotH;

  const origPts = periods.map((_, i) => [xOf(i), yOf(emaeOrig[i])]);
  const desPts = periods.map((_, i) => [xOf(i), yOf(emaeDes[i])]);
  const tcPts = periods.map((_, i) => [xOf(i), yOf(emaeTc[i])]);
  const jobPts = periods.map((_, i) => [xOf(i), yOf(jobsIdx[i])]);

  const fcEmaePts = [
    [xOf(nHist - 1), yOf(emaeDes[nHist - 1])],
    ...fcEmae.map((r, k) => [xOf(nHist + k), yOf(r.point_forecast)])
  ];
  const fcJobsPts = [
    [xOf(nHist - 1), yOf(jobsIdx[nHist - 1])],
    ...fcJobs.map((r, k) => [xOf(nHist + k), yOf(r.point_forecast)])
  ];

  const fcBandPolygon = fcEmae.length
    ? [
        [xOf(nHist - 1), yOf(emaeDes[nHist - 1])],
        ...fcEmae.map((r, k) => [xOf(nHist + k), yOf(r.ci95_high)]),
        ...fcEmae
          .slice()
          .reverse()
          .map((r, k) => [xOf(nHist + fcEmae.length - 1 - k), yOf(r.ci95_low)]),
        [xOf(nHist - 1), yOf(emaeDes[nHist - 1])]
      ]
        .map((p, idx) => `${idx === 0 ? 'M' : 'L'}${p[0].toFixed(1)},${p[1].toFixed(1)}`)
        .join(' ') + ' Z'
    : '';

  const idx2012 = Math.max(0, periods.findIndex((p) => p.startsWith('2012-01')));
  const x2012 = xOf(idx2012);

  return (
    <figure className="mc-card">
      <div className="mc-header">
        <div className="mc-header-titles">
          <h3 className="mc-title">{t.v2Title}</h3>
          <p className="mc-subtitle">{t.v2Sub}</p>
        </div>
        {onExpand && (
          <button type="button" className="mc-expand-btn" onClick={onExpand}>
            {t.zoomBtn}
          </button>
        )}
      </div>

      <div className="mc-legend-row">
        <span className="mc-legend-item">
          <i className="mc-dot" style={{ background: '#f59e0b' }} />
          {t.v2LegendJobs}
        </span>
        <span className="mc-legend-item">
          <i className="mc-dot" style={{ background: '#38bdf8' }} />
          {t.v2LegendEmaeTc}
        </span>
        <span className="mc-legend-item">
          <i className="mc-dot" style={{ background: '#10b981' }} />
          {t.v2LegendEmaeDes}
        </span>
        <span className="mc-legend-item">
          <i className="mc-dot" style={{ background: '#94a3b8' }} />
          {t.v2LegendEmaeOrig}
        </span>
        <span className="mc-legend-item">
          <i className="mc-dot" style={{ background: '#a855f7' }} />
          {t.v2LegendForecast}
        </span>
      </div>

      <div className="mc-svg-wrap">
        <svg viewBox={`0 0 ${W} ${H}`} className="mc-svg">
          {/* CAJAS DE RÉGIMEN EN BANDA SUPERIOR RESERVADA */}
          <rect
            x={padL}
            y={10}
            width={x2012 - padL - 6}
            height={42}
            rx={5}
            className="mc-regime-box mc-regime-green"
          />
          <text x={(padL + x2012) / 2} y={26} textAnchor="middle" className="mc-regime-title">
            {t.v2RegimeA}
          </text>
          <text x={(padL + x2012) / 2} y={42} textAnchor="middle" className="mc-regime-sub">
            {t.v2RegimeASub}
          </text>

          <rect
            x={x2012}
            y={10}
            width={W - padR - x2012}
            height={42}
            rx={5}
            className="mc-regime-box mc-regime-amber"
          />
          <text x={(x2012 + W - padR) / 2} y={26} textAnchor="middle" className="mc-regime-title">
            {t.v2RegimeB}
          </text>
          <text x={(x2012 + W - padR) / 2} y={42} textAnchor="middle" className="mc-regime-sub">
            {t.v2RegimeBSub}
          </text>

          {/* GRILLA Y EJE Y */}
          {[90, 100, 110, 120, 130, 140].map((v) => {
            const y = yOf(v);
            return (
              <g key={v}>
                <line
                  x1={padL}
                  y1={y}
                  x2={W - padR}
                  y2={y}
                  className={v === 100 ? 'mc-zero-line' : 'mc-grid-line'}
                />
                <text x={padL - 8} y={y + 4} textAnchor="end" className="mc-axis-text">
                  {v}
                </text>
              </g>
            );
          })}

          <line
            x1={x2012}
            y1={topY}
            x2={x2012}
            y2={botY}
            stroke="#f59e0b"
            strokeWidth="1.2"
            strokeDasharray="4 4"
            opacity="0.7"
          />

          {fcBandPolygon && <path d={fcBandPolygon} fill="rgba(168, 85, 247, 0.18)" />}
          <path d={buildPath(origPts)} fill="none" stroke="#94a3b8" strokeWidth="1.1" opacity="0.45" />
          <path d={buildPath(desPts)} fill="none" stroke="#10b981" strokeWidth="1.6" opacity="0.85" />
          <path d={buildPath(tcPts)} fill="none" stroke="#38bdf8" strokeWidth="2.6" />
          <path d={buildPath(jobPts)} fill="none" stroke="#f59e0b" strokeWidth="3" />

          <path d={buildPath(fcEmaePts)} fill="none" stroke="#a855f7" strokeWidth="2.2" strokeDasharray="4 3" />
          <path d={buildPath(fcJobsPts)} fill="none" stroke="#f59e0b" strokeWidth="2.2" strokeDasharray="4 3" />

          {periods.map((p, i) => {
            if (!p.endsWith('-01-01')) return null;
            const yr = parseInt(p.slice(0, 4), 10);
            if (yr % 2 !== 1 && yr !== 2026) return null;
            return (
              <text key={p} x={xOf(i)} y={H - 12} textAnchor="middle" className="mc-axis-text">
                {yr}
              </text>
            );
          })}

          {periods.map((p, i) => (
            <rect
              key={p}
              x={xOf(i) - plotW / nTotal / 2}
              y={topY}
              width={plotW / nTotal}
              height={plotH}
              fill="transparent"
              onMouseEnter={() => setHoverIdx(i)}
              onMouseLeave={() => setHoverIdx(null)}
            />
          ))}

          {hoverIdx !== null && (
            <g pointerEvents="none">
              <line
                x1={xOf(hoverIdx)}
                y1={topY}
                x2={xOf(hoverIdx)}
                y2={botY}
                stroke="#f59e0b"
                strokeWidth="1"
                strokeDasharray="3 3"
              />
              <circle cx={xOf(hoverIdx)} cy={yOf(jobsIdx[hoverIdx])} r={4.5} fill="#f59e0b" />
              <circle cx={xOf(hoverIdx)} cy={yOf(emaeTc[hoverIdx])} r={4.5} fill="#38bdf8" />
            </g>
          )}
        </svg>

        {hoverIdx !== null && (
          <div className="mc-tooltip">
            <strong>{periods[hoverIdx].slice(0, 7)}</strong>
            <span>
              {t.v2LegendJobs}: <b>{fmt(jobsIdx[hoverIdx], 1)}</b>
            </span>
            <span>
              {t.v2LegendEmaeTc}: <b>{fmt(emaeTc[hoverIdx], 1)}</b>
            </span>
            <span>
              {t.v2LegendEmaeDes}: <b>{fmt(emaeDes[hoverIdx], 1)}</b>
            </span>
          </div>
        )}
      </div>

      <figcaption className="mc-caption">{t.v2Caption}</figcaption>
    </figure>
  );
}

/* ==========================================================================
   VISUAL 3: CRECIMIENTO ACUMULADO POR MODALIDAD VS. DEMOGRAFÍA (2012–2026)
   ========================================================================== */
export function MacroVisual3({ series, lang = 'ES', onExpand }) {
  const t = getMacroText(lang);
  const [hoverIdx, setHoverIdx] = useState(null);

  if (!series?.period?.length) return null;

  const periods = series.period;
  const n = periods.length;

  const W = 940;
  const H = 410;
  const padL = 56;
  const padR = 72;
  const topY = 26;
  const botY = 364;
  const plotW = W - padL - padR;
  const plotH = botY - topY;

  const minY = -20;
  const maxY = 180;

  const xOf = (i) => padL + (i / (n - 1)) * plotW;
  const yOf = (v) =>
    botY - ((Math.max(minY, Math.min(maxY, Number(v) || 0)) - minY) / (maxY - minY)) * plotH;

  const lines = [
    { key: 'monotributo_social_pct', label: t.v3ModSoc, color: '#f43f5e', width: 2.8 },
    { key: 'monotributo_pct', label: t.v3ModMono, color: '#f59e0b', width: 2.4 },
    { key: 'empleo_publico_pct', label: t.v3ModPub, color: '#a855f7', width: 2.4 },
    { key: 'population_proj_pct', label: t.v3ModPop, color: 'var(--mc-pop-color)', width: 2.2, dash: '5 4' },
    { key: 'total_pct', label: t.v3ModTot, color: '#94a3b8', width: 1.8, dash: '2 3' },
    { key: 'empleo_privado_pct', label: t.v3ModPriv, color: '#38bdf8', width: 3.0 },
    { key: 'casas_particulares_pct', label: t.v3ModDom, color: '#10b981', width: 1.6 },
    { key: 'autonomos_pct', label: t.v3ModAut, color: '#06b6d4', width: 1.8 }
  ];

  const popPts = periods.map((_, i) => [xOf(i), yOf(series.population_proj_pct[i])]);
  const privPts = periods.map((_, i) => [xOf(i), yOf(series.empleo_privado_pct[i])]);
  const gapPolygon =
    [...popPts, ...privPts.slice().reverse()]
      .map((p, idx) => `${idx === 0 ? 'M' : 'L'}${p[0].toFixed(1)},${p[1].toFixed(1)}`)
      .join(' ') + ' Z';

  let peakIdx = 0;
  series.monotributo_social_pct.forEach((v, idx) => {
    if (v > series.monotributo_social_pct[peakIdx]) peakIdx = idx;
  });

  return (
    <figure className="mc-card">
      <div className="mc-header">
        <div className="mc-header-titles">
          <h3 className="mc-title">{t.v3Title}</h3>
          <p className="mc-subtitle">{t.v3Sub}</p>
        </div>
        {onExpand && (
          <button type="button" className="mc-expand-btn" onClick={onExpand}>
            {t.zoomBtn}
          </button>
        )}
      </div>

      <div className="mc-legend-row">
        {lines.map((l) => (
          <span key={l.key} className="mc-legend-item">
            <i className="mc-dot" style={{ background: l.color }} />
            {l.label}
          </span>
        ))}
      </div>

      <div className="mc-svg-wrap">
        <svg viewBox={`0 0 ${W} ${H}`} className="mc-svg">
          {[-20, 0, 25, 50, 100, 150].map((v) => {
            const y = yOf(v);
            return (
              <g key={v}>
                <line
                  x1={padL}
                  y1={y}
                  x2={W - padR}
                  y2={y}
                  className={v === 0 ? 'mc-zero-line' : 'mc-grid-line'}
                />
                <text x={padL - 8} y={y + 4} textAnchor="end" className="mc-axis-text">
                  {v > 0 ? `+${v}%` : `${v}%`}
                </text>
              </g>
            );
          })}

          <path d={gapPolygon} fill="rgba(56, 189, 248, 0.09)" />

          {lines.map((l) => {
            const pts = periods.map((_, i) => [xOf(i), yOf(series[l.key][i])]);
            const lastVal = series[l.key][n - 1];
            return (
              <g key={l.key}>
                <path
                  d={buildPath(pts)}
                  fill="none"
                  stroke={l.color}
                  strokeWidth={l.width}
                  strokeDasharray={l.dash}
                />
                <circle cx={xOf(n - 1)} cy={yOf(lastVal)} r={3} fill={l.color} />
              </g>
            );
          })}

          <g>
            <rect
              x={padL + 40}
              y={34}
              width={290}
              height={40}
              rx={6}
              className="mc-regime-box mc-regime-red"
            />
            <text x={padL + 185} y={50} textAnchor="middle" className="mc-regime-title">
              {t.v3CalloutTitle}
            </text>
            <text x={padL + 185} y={66} textAnchor="middle" className="mc-regime-sub">
              {t.v3CalloutSub}
            </text>
            <line
              x1={padL + 330}
              y1={52}
              x2={xOf(peakIdx) - 4}
              y2={yOf(series.monotributo_social_pct[peakIdx])}
              stroke="#f43f5e"
              strokeWidth="1.3"
              strokeDasharray="3 3"
            />
            <circle
              cx={xOf(peakIdx)}
              cy={yOf(series.monotributo_social_pct[peakIdx])}
              r={4.5}
              fill="#f43f5e"
            />
          </g>

          <text x={W - padR + 6} y={yOf(series.monotributo_pct[n - 1]) + 3} className="mc-end-label" fill="#f59e0b">
            +{fmt(series.monotributo_pct[n - 1], 1)}%
          </text>
          <text x={W - padR + 6} y={yOf(series.empleo_publico_pct[n - 1]) - 3} className="mc-end-label" fill="#a855f7">
            +{fmt(series.empleo_publico_pct[n - 1], 1)}%
          </text>
          <text x={W - padR + 6} y={yOf(series.population_proj_pct[n - 1]) + 3} className="mc-end-label" fill="#94a3b8">
            +{fmt(series.population_proj_pct[n - 1], 1)}%
          </text>
          <text x={W - padR + 6} y={yOf(series.empleo_privado_pct[n - 1]) + 2} className="mc-end-label" fill="#38bdf8">
            {fmt(series.empleo_privado_pct[n - 1], 1)}%
          </text>
          <text x={W - padR + 6} y={yOf(series.autonomos_pct[n - 1]) + 6} className="mc-end-label" fill="#06b6d4">
            {fmt(series.autonomos_pct[n - 1], 1)}%
          </text>

          {periods.map((p, i) => {
            if (!p.endsWith('-01-01')) return null;
            const yr = parseInt(p.slice(0, 4), 10);
            if (yr % 2 !== 0) return null;
            return (
              <text key={p} x={xOf(i)} y={H - 12} textAnchor="middle" className="mc-axis-text">
                {yr}
              </text>
            );
          })}

          {periods.map((p, i) => (
            <rect
              key={p}
              x={xOf(i) - plotW / n / 2}
              y={topY}
              width={plotW / n}
              height={plotH}
              fill="transparent"
              onMouseEnter={() => setHoverIdx(i)}
              onMouseLeave={() => setHoverIdx(null)}
            />
          ))}

          {hoverIdx !== null && (
            <line
              x1={xOf(hoverIdx)}
              y1={topY}
              x2={xOf(hoverIdx)}
              y2={botY}
              stroke="#38bdf8"
              strokeWidth="1"
              strokeDasharray="3 3"
              pointerEvents="none"
            />
          )}
        </svg>

        {hoverIdx !== null && (
          <div className="mc-tooltip">
            <strong>{periods[hoverIdx].slice(0, 7)} (2012 = 0%)</strong>
            <span>
              {t.v3ModSoc}: <b>+{fmt(series.monotributo_social_pct[hoverIdx], 1)}%</b>
            </span>
            <span>
              {t.v3ModMono}: <b>+{fmt(series.monotributo_pct[hoverIdx], 1)}%</b>
            </span>
            <span>
              {t.v3ModPub}: <b>+{fmt(series.empleo_publico_pct[hoverIdx], 1)}%</b>
            </span>
            <span>
              {t.v3ModPop}: <b>+{fmt(series.population_proj_pct[hoverIdx], 1)}%</b>
            </span>
            <span>
              {t.v3ModPriv}: <b>{fmt(series.empleo_privado_pct[hoverIdx], 1)}%</b>
            </span>
          </div>
        )}
      </div>

      <figcaption className="mc-caption">{t.v3Caption}</figcaption>
    </figure>
  );
}

/* ==========================================================================
   VISUAL 4: TABLA Y BARRAS DE COMPOSICIÓN DEL TRABAJO REGISTRADO
   ========================================================================== */
export function MacroVisual4Table({ rows, lang = 'ES' }) {
  const t = getMacroText(lang);
  if (!rows?.length) return null;

  const MOD_NAMES_I18N = {
    'Empleo privado': t.v3ModPriv.replace(/\s*\(.*\)/, ''),
    'Empleo público': t.v3ModPub,
    Monotributo: t.v3ModMono,
    'Empleo en casas particulares': t.v3ModDom,
    Autónomos: t.v3ModAut.replace(/\s*\(.*\)/, ''),
    'Monotributo Social': t.v3ModSoc
  };

  return (
    <figure className="mc-card">
      <div className="mc-header">
        <div className="mc-header-titles">
          <h3 className="mc-title">{t.v4Title}</h3>
          <p className="mc-subtitle">{t.v4Sub}</p>
        </div>
      </div>

      <div className="mc-table-wrap">
        <table className="mc-shift-table">
          <thead>
            <tr>
              <th>{t.v4ColMod}</th>
              <th>{t.v4Col2012}</th>
              <th>{t.v4Col2022}</th>
              <th>{t.v4ColLatest}</th>
              <th>{t.v4ColDelta}</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => {
              const isNeg = r.net_shift_pp < 0;
              const label = lang === 'ES' ? r.modality : MOD_NAMES_I18N[r.modality] || r.modality;
              return (
                <tr key={r.modality}>
                  <td className="mc-td-mod">{label}</td>
                  <td>{fmt(r.share_2012_01_pct, 2)}%</td>
                  <td>{fmt(r.share_2022_03_pct, 2)}%</td>
                  <td className="mc-td-bold">{fmt(r.share_latest_pct, 2)}%</td>
                  <td>
                    <span className={`mc-delta-pill ${isNeg ? 'is-neg' : 'is-pos'}`}>
                      {isNeg ? '' : '+'}
                      {fmt(r.net_shift_pp, 2)} pp
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <figcaption className="mc-caption">{t.v4Caption}</figcaption>
    </figure>
  );
}

/* ==========================================================================
   VISUAL 5: SALARIO REAL VS. PBI REAL (2005–2025)
   ========================================================================== */
export function MacroVisual5({ series, lang = 'ES', onExpand }) {
  const t = getMacroText(lang);
  const [hoverIdx, setHoverIdx] = useState(null);

  if (!series?.year?.length) return null;

  const years = series.year;
  const wageIdx = series.sal_real_idx_2012;
  const gdpIdx = series.gdp_real_idx_2012;
  const wageYoy = series.real_sal_yoy_pct;
  const gdpYoy = series.gdp_yoy_pct;
  const n = years.length;

  const W = 940;
  const H = 460;
  const padL = 56;
  const padR = 44;
  const plotW = W - padL - padR;

  const topY0 = 48;
  const topY1 = 258;
  const topH = topY1 - topY0;
  const minIdx = 65;
  const maxIdx = 112;

  const botY0 = 305;
  const botY1 = 425;
  const botH = botY1 - botY0;
  const minYoy = -14;
  const maxYoy = 14;

  const xOf = (i) => padL + (i / (n - 1)) * plotW;
  const yTop = (v) =>
    topY1 - ((Math.max(minIdx, Math.min(maxIdx, Number(v) || 100)) - minIdx) / (maxIdx - minIdx)) * topH;
  const yBot = (v) =>
    botY1 - ((Math.max(minYoy, Math.min(maxYoy, Number(v) || 0)) - minYoy) / (maxYoy - minYoy)) * botH;
  const zeroBotY = yBot(0);

  const wagePts = years.map((_, i) => [xOf(i), yTop(wageIdx[i])]);
  const gdpPts = years.map((_, i) => [xOf(i), yTop(gdpIdx[i])]);

  const idx2012 = Math.max(0, years.indexOf(2012));
  const gapPts = [...gdpPts.slice(idx2012), ...wagePts.slice(idx2012).reverse()];
  const gapPath =
    gapPts.map((p, idx) => `${idx === 0 ? 'M' : 'L'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ') + ' Z';

  return (
    <figure className="mc-card">
      <div className="mc-header">
        <div className="mc-header-titles">
          <h3 className="mc-title">{t.v5Title}</h3>
          <p className="mc-subtitle">{t.v5Sub}</p>
        </div>
        {onExpand && (
          <button type="button" className="mc-expand-btn" onClick={onExpand}>
            {t.zoomBtn}
          </button>
        )}
      </div>

      <div className="mc-legend-row">
        <span className="mc-legend-item">
          <i className="mc-dot" style={{ background: '#f43f5e' }} />
          {t.v5LegendWage}
        </span>
        <span className="mc-legend-item">
          <i className="mc-dot" style={{ background: '#38bdf8' }} />
          {t.v5LegendGdp}
        </span>
      </div>

      <div className="mc-svg-wrap">
        <svg viewBox={`0 0 ${W} ${H}`} className="mc-svg">
          <rect
            x={xOf(idx2012)}
            y={8}
            width={W - padR - xOf(idx2012)}
            height={30}
            rx={5}
            className="mc-regime-box mc-regime-red"
          />
          <text
            x={(xOf(idx2012) + W - padR) / 2}
            y={27}
            textAnchor="middle"
            className="mc-regime-title"
          >
            {t.v5Callout}
          </text>

          {[70, 80, 90, 100, 110].map((v) => {
            const y = yTop(v);
            return (
              <g key={v}>
                <line
                  x1={padL}
                  y1={y}
                  x2={W - padR}
                  y2={y}
                  className={v === 100 ? 'mc-zero-line' : 'mc-grid-line'}
                />
                <text x={padL - 8} y={y + 4} textAnchor="end" className="mc-axis-text">
                  {v}
                </text>
              </g>
            );
          })}

          <path d={gapPath} fill="rgba(244, 63, 94, 0.12)" />
          <path d={buildPath(gdpPts)} fill="none" stroke="#38bdf8" strokeWidth="2.6" />
          <path d={buildPath(wagePts)} fill="none" stroke="#f43f5e" strokeWidth="3" />

          {years.map((yr, i) => (
            <g key={`dots-${yr}`}>
              <circle cx={xOf(i)} cy={yTop(gdpIdx[i])} r={3} fill="#38bdf8" />
              <circle cx={xOf(i)} cy={yTop(wageIdx[i])} r={3.5} fill="#f43f5e" />
            </g>
          ))}

          <text x={padL} y={292} className="mc-panel-label">
            {t.v5BarTitle}
          </text>

          {[-10, 0, 10].map((v) => {
            const y = yBot(v);
            return (
              <g key={v}>
                <line
                  x1={padL}
                  y1={y}
                  x2={W - padR}
                  y2={y}
                  className={v === 0 ? 'mc-zero-line' : 'mc-grid-line'}
                />
                <text x={padL - 8} y={y + 4} textAnchor="end" className="mc-axis-text">
                  {v}%
                </text>
              </g>
            );
          })}

          {years.map((yr, i) => {
            const x = xOf(i);
            const bw = 9;
            const yW = yBot(wageYoy[i]);
            const yG = yBot(gdpYoy[i]);

            return (
              <g key={yr}>
                <rect
                  x={x - bw - 1}
                  y={Math.min(zeroBotY, yW)}
                  width={bw}
                  height={Math.max(1.5, Math.abs(yW - zeroBotY))}
                  rx={1.5}
                  fill="#f43f5e"
                  opacity={hoverIdx === i ? 1 : 0.85}
                />
                <rect
                  x={x + 1}
                  y={Math.min(zeroBotY, yG)}
                  width={bw}
                  height={Math.max(1.5, Math.abs(yG - zeroBotY))}
                  rx={1.5}
                  fill="#38bdf8"
                  opacity={hoverIdx === i ? 1 : 0.85}
                />
                <text x={x} y={H - 10} textAnchor="middle" className="mc-axis-text">
                  {yr}
                </text>
                <rect
                  x={x - plotW / n / 2}
                  y={topY0}
                  width={plotW / n}
                  height={botY1 - topY0}
                  fill="transparent"
                  onMouseEnter={() => setHoverIdx(i)}
                  onMouseLeave={() => setHoverIdx(null)}
                />
              </g>
            );
          })}
        </svg>

        {hoverIdx !== null && (
          <div className="mc-tooltip">
            <strong>{years[hoverIdx]} (2012 = 100)</strong>
            <span>
              {t.v5LegendWage}: <b>{fmt(wageIdx[hoverIdx], 1)}</b> (
              {Number(wageYoy[hoverIdx]) >= 0 ? '+' : ''}
              {fmt(wageYoy[hoverIdx], 1)}% YoY)
            </span>
            <span>
              {t.v5LegendGdp}: <b>{fmt(gdpIdx[hoverIdx], 1)}</b> (
              {Number(gdpYoy[hoverIdx]) >= 0 ? '+' : ''}
              {fmt(gdpYoy[hoverIdx], 1)}% YoY)
            </span>
          </div>
        )}
      </div>

      <figcaption className="mc-caption">{t.v5Caption}</figcaption>
    </figure>
  );
}
