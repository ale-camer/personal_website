import React, { useState } from 'react';
import WebbDeepFieldCanvas from './WebbDeepFieldCanvas';
import { tx, useSiteLocale } from '../../i18n/localeService';

const KEY_BULLETS = [
  {
    titleEs: 'Exploración de 213 activos globales',
    titleEn: 'Exploration of 213 global assets',
    textEs:
      'Compará acciones, bonos, divisas, materias primas y cripto en tiempo real, detectá movimientos inusuales y leé el pulso del mercado de un vistazo.',
    textEn:
      'Compare equities, bonds, currencies, commodities, and crypto in real time, spot unusual moves, and read the market pulse at a glance.',
    href: 'https://quantlambda.dev/?view=markets&mode=screener',
    linkLabelEs: 'Mercados ↗',
    linkLabelEn: 'Markets ↗'
  },
  {
    titleEs: 'Lentes de análisis a medida por activo',
    titleEn: 'Tailored analytical lenses per asset',
    textEs:
      'Inspeccioná opciones y volatilidad en 3D, curvas de tasas de 42 países, futuros y resúmenes claros sobre balances y reportes oficiales.',
    textEn:
      'Inspect 3D options & volatility surfaces, sovereign yield curves across 42 countries, futures, and clear summaries of official filings.',
    href: 'https://quantlambda.dev/?view=markets&mode=detail&asset=NVDA-OPT&section=analytics&lens=derivatives&sub=surface3d',
    linkLabelEs: 'Análisis ↗',
    linkLabelEn: 'Analytics ↗'
  },
  {
    titleEs: 'Simulador de carteras y debate de inversión',
    titleEn: 'Portfolio simulator & investment committee',
    textEs:
      'Armá o elegí un portafolio en un clic, medí su riesgo real ante crisis históricas y escuchá distintas posturas antes de decidir.',
    textEn:
      'Build or pick a portfolio in one click, stress-test its risk against historical crises, and evaluate contrasting views before deciding.',
    href: 'https://quantlambda.dev/?view=portfolio',
    linkLabelEs: 'Portafolio ↗',
    linkLabelEn: 'Portfolio ↗'
  },
  {
    titleEs: 'Guía paso a paso y asistente integrado',
    titleEn: 'Step-by-step guide & built-in copilot',
    textEs:
      'Recorré la plataforma con videos cortos, explicaciones en lenguaje simple junto a cada métrica y un copiloto para despejar dudas al instante.',
    textEn:
      'Tour the platform with short walkthroughs, plain-language explanations next to every metric, and an interactive copilot.',
    href: 'https://quantlambda.dev/?view=guide',
    linkLabelEs: 'Guía ↗',
    linkLabelEn: 'Guide ↗'
  }
];

export default function QuantLambdaSection({
  colorMode = 'dark',
  lang = 'ES',
  hideTopBanner = false
}) {
  useSiteLocale(lang);
  const [sceneIdx, setSceneIdx] = useState(null);
  const isLight = colorMode === 'light';

  return (
    <div className="ql-showcase">
      {/* 1. CABECERA UNIFICADA: PROYECTO INSIGNIA (opcional cuando se usa dentro del acordeón compacto Opción C) */}
      {!hideTopBanner && (
        <div className="ql-top-banner">
          <div className="ql-top-banner-main">
            <h2 className="tl-main-title">QuantLambda</h2>
            <p className="pj-purpose-lead">
              <strong>{tx('Mi proyecto insignia:', 'My flagship project:', lang)}</strong>{' '}
              {tx(
                'una plataforma para seguir mercados globales en vivo, analizar cada activo a fondo y poner a prueba carteras de inversión.',
                'a live platform to track global markets, analyze individual assets in depth, and stress-test investment portfolios.',
                lang
              )}
            </p>
          </div>

          <div className="ql-cta-row">
            <a
              href="https://quantlambda.dev"
              target="_blank"
              rel="noreferrer"
              className="pj-repo-cta"
              style={{
                '--insp-accent': '#10b981',
                '--insp-rgb': '16, 185, 129'
              }}
            >
              <span>{tx('Abrir QuantLambda ↗', 'Open QuantLambda ↗', lang)}</span>
            </a>
            <a
              href="https://quantlambda.dev/?view=guide"
              target="_blank"
              rel="noreferrer"
              className="ql-btn-secondary"
            >
              {tx('Guía Interactiva ↗', 'Interactive Guide ↗', lang)}
            </a>
          </div>
        </div>
      )}

      {/* 2. VENTANA DEL HOME ANIMADO A ANCHO COMPLETO */}
      <div className="ql-preview-frame">
        <div className="ql-browser-bar">
          <div className="ql-browser-dots">
            <span />
            <span />
            <span />
          </div>
          <a
            href="https://quantlambda.dev"
            target="_blank"
            rel="noreferrer"
            className="ql-browser-url"
            title={tx('Abrir quantlambda.dev en una pestaña nueva', 'Open quantlambda.dev in a new tab', lang)}
          >
            https://quantlambda.dev
          </a>
          <div
            className="ql-scene-switcher"
            title={tx('Cambiar escena matemática del Home', 'Switch Home mathematical scene', lang)}
          >
            {[0, 1, 2, 3].map((idx) => (
              <button
                key={idx}
                type="button"
                className={`ql-scene-dot-btn ${sceneIdx === idx ? 'is-active' : ''}`}
                onClick={() => setSceneIdx(sceneIdx === idx ? null : idx)}
              >
                {idx + 1}
              </button>
            ))}
          </div>
        </div>

        <div className={`ql-mini-stage ${isLight ? 'is-light' : 'is-dark'}`}>
          <div className="ql-mini-header">
            <span className="ql-mini-lambda">λ</span>
            <div className="ql-mini-nav">
              <a
                href="https://quantlambda.dev/?view=markets&mode=screener"
                target="_blank"
                rel="noreferrer"
              >
                {tx('Mercados', 'Markets', lang)}
              </a>
              <a
                href="https://quantlambda.dev/?view=portfolio"
                target="_blank"
                rel="noreferrer"
              >
                {tx('Portafolio', 'Portfolio', lang)}
              </a>
            </div>
            <span className="ql-mini-spacer" />
          </div>

          <WebbDeepFieldCanvas
            isPaused={false}
            lang={lang === 'ES' ? 'ES' : 'EN'}
            lightMode={isLight}
            selectedScene={sceneIdx}
          />

          <div className="ql-mini-overlay-copy">
            <div className="ql-mini-headline">
              {tx('Donde se decodifican los mercados', 'Where markets get decoded', lang)}
            </div>
            <div className="ql-mini-brief">
              {tx(
                'Seguí activos globales en tiempo real, simulá el riesgo de tu cartera y explorá cada instrumento con herramientas visuales claras.',
                'Track global assets in real time, simulate your portfolio risk, and explore every instrument with clear visual tools.',
                lang
              )}
            </div>
          </div>

          <div className="ql-mini-footer">
            <div className="ql-mini-footer-left">
              <a
                href="https://quantlambda.dev/?view=observability"
                target="_blank"
                rel="noreferrer"
              >
                <i className="ql-mini-sys-dot" /> {tx('Sistema', 'System', lang)}
              </a>
              <a href="https://quantlambda.dev/?view=guide" target="_blank" rel="noreferrer">
                {tx('Guía', 'Guide', lang)}
              </a>
            </div>
            <div className="ql-mini-footer-right">
              <span>{lang}</span>
              <span>{tx('Paleta', 'Palette', lang)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* 3. CUATRO BULLETS ORIENTADOS AL USUARIO */}
      <ul className="ql-bullets-list">
        {KEY_BULLETS.map((item) => (
          <li key={item.titleEn} className="ql-bullet-item">
            <span className="ql-bullet-marker" aria-hidden="true" />
            <div className="ql-bullet-body">
              <strong>{tx(item.titleEs, item.titleEn, lang)}:</strong>{' '}
              <span>{tx(item.textEs, item.textEn, lang)}</span>
            </div>
            <a
              href={item.href}
              target="_blank"
              rel="noreferrer"
              className="ql-bullet-link"
            >
              {tx(item.linkLabelEs, item.linkLabelEn, lang)}
            </a>
          </li>
        ))}
      </ul>

      {/* 4. PUENTE SOBRIO PARA QUIEN QUIERA INDAGAR EN EL CÓMO SE HIZO */}
      <footer className="ql-arch-strip">
        <div className="ql-arch-info">
          <p className="ql-arch-text">
            <strong>
              {tx('¿Querés indagar en cómo está construido?', 'Want to inspect how it is built under the hood?', lang)}
            </strong>{' '}
            {tx(
              'Consultá en vivo la arquitectura completa de datos, el estado de los procesos y los costos operativos de la plataforma.',
              'Explore the live data architecture, pipeline health telemetry, and FinOps operating costs of the platform.',
              lang
            )}
          </p>
        </div>
        <div className="ql-arch-actions">
          <a
            href="https://quantlambda.dev/?view=observability"
            target="_blank"
            rel="noreferrer"
            className="ql-arch-link"
          >
            {tx('Ver arquitectura y sistema en vivo ↗', 'View live architecture & system ↗', lang)}
          </a>
        </div>
      </footer>
    </div>
  );
}
