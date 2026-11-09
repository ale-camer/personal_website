import React, { useState } from 'react';
import WebbDeepFieldCanvas from './WebbDeepFieldCanvas';

const KEY_BULLETS = [
  {
    title: 'Exploración de 213 activos globales',
    text: 'Tabla institucional, mapa orbital de anomalías (P-06) y mapa de calor en 10 clases de activos.',
    href: 'https://quantlambda.dev/?view=markets&mode=screener',
    linkLabel: 'Markets ↗'
  },
  {
    title: 'Herramientas ad-hoc por activo + IA',
    text: 'Superficies 3D y payoffs de opciones, curvas soberanas de 42 países, FX, futuros y RAG sobre reportes oficiales.',
    href: 'https://quantlambda.dev/?view=markets&mode=detail&asset=NVDA-OPT&section=analytics&lens=derivatives&sub=surface3d',
    linkLabel: 'Analytics & RAG ↗'
  },
  {
    title: 'Simulador de carteras y Comité Multi-Agente',
    text: 'Cartera de $100k con presets en 1 clic, VaR/CVaR, correlación, Brinson y deliberación auditable de 3 agentes.',
    href: 'https://quantlambda.dev/?view=portfolio',
    linkLabel: 'Portfolio ↗'
  },
  {
    title: 'Guía con videos animados, chat IA y 56 idiomas',
    text: 'Recorrido visual paso a paso, explicaciones en lenguaje simple junto al dato técnico y copiloto conversacional.',
    href: 'https://quantlambda.dev/?view=guide',
    linkLabel: 'Guía ↗'
  }
];

export default function QuantLambdaSection({ colorMode = 'dark' }) {
  const [sceneIdx, setSceneIdx] = useState(null);
  const isLight = colorMode === 'light';

  return (
    <div className="ql-showcase">
      {/* 1. CABECERA / PRESENTACIÓN A ANCHO COMPLETO */}
      <div className="ql-top-banner">
        <div className="ql-top-banner-main">
          <div className="ql-eyebrow-row">
            <span className="ql-live-dot" />
            <span className="ql-eyebrow-text">PROYECTO ESTRELLA • EN PRODUCCIÓN</span>
            <span className="ql-domain-pill">quantlambda.dev</span>
          </div>

          <h2 className="ql-title">QuantLambda</h2>

          <p className="ql-lead">
            Analizá activos globales en tiempo real, simulá el riesgo de tu cartera y explorá una
            arquitectura cuantitativa y agéntica de punta a punta.
          </p>
        </div>

        <div className="ql-cta-row">
          <a
            href="https://quantlambda.dev"
            target="_blank"
            rel="noreferrer"
            className="ql-btn-primary"
          >
            Abrir QuantLambda ↗
          </a>
          <a
            href="https://quantlambda.dev/?view=guide"
            target="_blank"
            rel="noreferrer"
            className="ql-btn-secondary"
          >
            Guía Interactiva con Videos ↗
          </a>
        </div>
      </div>

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
            title="Abrir quantlambda.dev en una pestaña nueva"
          >
            https://quantlambda.dev
          </a>
          <div className="ql-scene-switcher" title="Cambiar escena matemática del Home">
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
                Mercados
              </a>
              <a
                href="https://quantlambda.dev/?view=portfolio"
                target="_blank"
                rel="noreferrer"
              >
                Portafolio
              </a>
            </div>
            <span className="ql-mini-spacer" />
          </div>

          <WebbDeepFieldCanvas
            isPaused={false}
            lang="ES"
            lightMode={isLight}
            selectedScene={sceneIdx}
          />

          <div className="ql-mini-overlay-copy">
            <div className="ql-mini-headline">Donde se decodifican los mercados</div>
            <div className="ql-mini-brief">
              Analizá activos globales en tiempo real, simulá el riesgo de tu cartera y explorá
              una arquitectura cuantitativa y agéntica de punta a punta.
            </div>
          </div>

          <div className="ql-mini-footer">
            <div className="ql-mini-footer-left">
              <a
                href="https://quantlambda.dev/?view=observability"
                target="_blank"
                rel="noreferrer"
              >
                <i className="ql-mini-sys-dot" /> Sistema
              </a>
              <a href="https://quantlambda.dev/?view=guide" target="_blank" rel="noreferrer">
                Guía
              </a>
            </div>
            <div className="ql-mini-footer-right">
              <span>ES</span>
              <span>Paleta</span>
            </div>
          </div>
        </div>
      </div>

      {/* 3. CUATRO BULLETS CONCISOS */}
      <ul className="ql-bullets-list">
        {KEY_BULLETS.map((item) => (
          <li key={item.title} className="ql-bullet-item">
            <span className="ql-bullet-marker" aria-hidden="true" />
            <div className="ql-bullet-body">
              <strong>{item.title}:</strong> <span>{item.text}</span>
            </div>
            <a
              href={item.href}
              target="_blank"
              rel="noreferrer"
              className="ql-bullet-link"
            >
              {item.linkLabel}
            </a>
          </li>
        ))}
      </ul>

      {/* 4. FRANJA DE INGENIERÍA & FINOPS */}
      <footer className="ql-arch-strip">
        <div className="ql-arch-info">
          <span className="ql-arch-badge">INGENIERÍA E2E & FINOPS</span>
          <p className="ql-arch-text">
            <strong>11 pipelines en producción sobre GCP (P-01 a P-11)</strong> • Ingesta de mercado,
            detección de anomalías (Isolation Forest), RAG vectorial (pgvector), sentimiento FinBERT
            y comité multi-agente corriendo bajo arquitectura <em>Scale-to-Zero (~$0.95/mes)</em>.
          </p>
        </div>
        <a
          href="https://quantlambda.dev/?view=observability"
          target="_blank"
          rel="noreferrer"
          className="ql-arch-link"
        >
          Ver Telemetría y FinOps en vivo ↗
        </a>
      </footer>
    </div>
  );
}
