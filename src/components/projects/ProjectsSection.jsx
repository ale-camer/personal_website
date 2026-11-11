import React, { useState, useEffect } from 'react';
import QuantLambdaSection from '../quantlambda/QuantLambdaSection';
import { tx, txList, useSiteLocale } from '../../i18n/localeService';

export const PLAYGROUND_PROJECTS = [
  {
    id: 'spark-encyclopedia',
    title: 'Spark Learning',
    oneLinerEs:
      'Guía visual e interactiva para entender cómo procesa datos a gran escala Apache Spark.',
    oneLinerEn:
      'Interactive visual guide to understand how Apache Spark processes large-scale distributed data.',
    objectiveEs:
      'Transforma conceptos complejos de procesamiento distribuido en un recorrido visual paso a paso, para explorar qué decisiones se toman en cada etapa y qué ocurre por dentro cuando un sistema escala.',
    objectiveEn:
      'Turns complex distributed computing concepts into a step-by-step visual walkthrough, allowing you to explore architectural decisions at every stage and see what happens under the hood as a cluster scales.',
    colorAccent: '#f43f5e',
    colorRgb: '244, 63, 94',
    appUrl: 'https://spark.alejandrocamerlengo.com',
    displayUrl: 'https://spark.alejandrocamerlengo.com',
    previewImg: '/images/projects/spark-preview.png',
    previewAlign: 'top',
    appLabelEs: 'Abrir Spark Learning ↗',
    appLabelEn: 'Open Spark Learning ↗',
    bulletsEs: [
      'Mapa de decisiones interactivo: Recorré las 7 etapas de un flujo de datos y descubrí cómo se conectan los problemas reales con sus soluciones.',
      'Qué pasa por dentro: Inspeccioná casos prácticos, cuellos de botella frecuentes y cómo destrabarlos.',
      'Enciclopedia integrada: Buscador rápido con 30 guías directas para consultar cualquier concepto al instante.'
    ],
    bulletsEn: [
      'Interactive decision map: Navigate the 7 stages of a data pipeline and discover how real-world bottlenecks connect to their engineering solutions.',
      'Under the hood: Inspect practical case studies, frequent shuffle/skew bottlenecks, and how to resolve them.',
      'Built-in encyclopedia: Instant search across 30 direct reference guides to look up any concept on the fly.'
    ]
  },
  {
    id: 'geospatial-world-map',
    title: 'World Map',
    oneLinerEs:
      'Marcá los países que visitaste, medí tu recorrido por continente y creá tu propio mapa.',
    oneLinerEn:
      'Mark the countries you have visited, track your progress by continent, and design your own custom map.',
    objectiveEs:
      'Una herramienta pensada para viajeros y curiosos de la geografía: seleccioná los países que conocés, visualizá tus estadísticas globales al instante y diseñá un mapa a tu medida para guardar o imprimir.',
    objectiveEn:
      'A tool designed for travelers and geography enthusiasts: select the countries you have visited, view your global statistics instantly, and style a custom map to save or print.',
    colorAccent: '#38bdf8',
    colorRgb: '56, 189, 248',
    appUrl: 'https://worldmap.alejandrocamerlengo.com',
    displayUrl: 'https://worldmap.alejandrocamerlengo.com',
    previewImg: '/images/projects/worldmap-preview.png',
    previewAlign: 'top',
    appLabelEs: 'Abrir World Map ↗',
    appLabelEn: 'Open World Map ↗',
    bulletsEs: [
      'Tu progreso alrededor del mundo: Estadísticas en vivo de cuántos países y qué porcentaje conocés de cada continente.',
      'Diseño a tu medida: Elegí entre distintos estilos visuales y colores antes de lanzar tu mapa en pantalla completa.',
      'Guardá y retomá cuando quieras: Descargá tu selección en un clic o volvé a cargarla sin necesidad de crearte una cuenta.'
    ],
    bulletsEn: [
      'Your progress around the world: Live statistics showing how many countries and what percentage of each continent you have explored.',
      'Custom visual styling: Choose across multiple cartographic themes and color palettes before launching your full-screen map.',
      'Save and resume anytime: Download your selection in one click or reload it later without needing an account.'
    ]
  },
  {
    id: 'world-bank-qol',
    title: 'Quality of Life Explorer',
    oneLinerEs:
      'Compará cómo evolucionaron el bienestar, la salud, la educación y los ingresos en 240 países.',
    oneLinerEn:
      'Compare how well-being, health, education, and income evolved across 240 countries.',
    objectiveEs:
      'Un observatorio interactivo para cruzar décadas de datos históricos y descubrir qué países avanzaron, cuáles se estancaron y cómo cambiaron las condiciones de vida alrededor del mundo.',
    objectiveEn:
      'An interactive observatory to cross-examine decades of historical data and discover which nations advanced, which stagnated, and how living standards shifted worldwide.',
    colorAccent: '#f59e0b',
    colorRgb: '245, 158, 11',
    appUrl: 'https://explorer.alejandrocamerlengo.com',
    displayUrl: 'https://explorer.alejandrocamerlengo.com',
    previewImg: '/images/projects/qol-preview.png',
    appLabelEs: 'Abrir Quality of Life Explorer ↗',
    appLabelEn: 'Open Quality of Life Explorer ↗',
    bulletsEs: [
      '44 indicadores de vida real: Explorá desde esperanza de vida, salud y educación hasta poder adquisitivo, energía y ambiente.',
      'Viaje en el tiempo: Filtrá cualquier ventana de años para ver cómo cambió el mapa mundial y el ranking global.',
      'Exploración sincronizada: Hacé clic en cualquier país del mapa o de la tabla comparativa para seguir su trayectoria.'
    ],
    bulletsEn: [
      '44 real-life indicators: Explore metrics ranging from life expectancy, health, and education to purchasing power, energy, and environment.',
      'Time travel: Filter any historical year window to see how the world map and global rankings evolved.',
      'Synchronized exploration: Click any country on the map or comparative table to trace its historical trajectory.'
    ]
  }
];

function renderBulletWithBoldLead(b) {
  const colonIdx = b.indexOf(':');
  if (colonIdx > 0 && colonIdx < 58) {
    const lead = b.slice(0, colonIdx + 1).trim();
    const rest = b.slice(colonIdx + 1).trim();
    return (
      <li key={b}>
        <strong className="tl-bullet-lead">{lead}</strong> {rest}
      </li>
    );
  }
  return <li key={b}>{b}</li>;
}

export default function ProjectsSection({ colorMode = 'dark', lang = 'ES' }) {
  useSiteLocale(lang);
  const [openId, setOpenId] = useState(null);
  // 0 = QuantLambda, 1..3 = los 3 proyectos exploratorios
  const [kbdIdx, setKbdIdx] = useState(0);

  const toggleProject = (id) => {
    setOpenId((prev) => (prev === id ? null : id));
  };

  useEffect(() => {
    const handleKey = (e) => {
      const tag = document.activeElement?.tagName?.toLowerCase();
      if (tag === 'input' || tag === 'textarea') return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;

      const total = PLAYGROUND_PROJECTS.length + 1;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setKbdIdx((i) => (i + 1) % total);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setKbdIdx((i) => (i - 1 + total) % total);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (kbdIdx === 0) {
          window.open('https://quantlambda.dev', '_blank', 'noopener,noreferrer');
        } else {
          const proj = PLAYGROUND_PROJECTS[kbdIdx - 1];
          if (proj) toggleProject(proj.id);
        }
      }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [kbdIdx]);

  return (
    <div className="pj-root">
      {/* 1. PROYECTO INSIGNIA DESTACADO ARRIBA: QUANTLAMBDA */}
      <div className={`pj-flagship-wrap ${kbdIdx === 0 ? 'is-kbd-active' : ''}`}>
        <QuantLambdaSection colorMode={colorMode} lang={lang} />
      </div>

      {/* 2. BLOQUE SECUNDARIO: PROYECTOS DE EXPLORACIÓN / PRÁCTICA */}
      <div className="pj-sandbox-block">
        <div className="pj-purpose-header">
          <h3 className="tl-main-title">
            {tx(
              'Otros desarrollos y exploraciones interactivas',
              'Other interactive builds & explorations',
              lang
            )}
          </h3>
          <p className="pj-purpose-lead">
            {tx(
              'Aplicaciones más acotadas y experimentales, creadas por curiosidad para explorar datos públicos, mapas y conceptos visuales jugando:',
              'Focused experimental applications built out of curiosity to explore public datasets, maps, and visual concepts hands-on:',
              lang
            )}
          </p>
        </div>

        {/* LISTA DESPLEGABLE ESTILO GIT LIMPIA */}
        <div className="pj-acc-list mode-git">
          {PLAYGROUND_PROJECTS.map((proj, idx) => {
            const isOpen = openId === proj.id;
            const isKbdFocused = kbdIdx === idx + 1;
            const oneLiner = tx(proj.oneLinerEs, proj.oneLinerEn, lang);
            const objective = tx(proj.objectiveEs, proj.objectiveEn, lang);
            const appLabel = tx(proj.appLabelEs, proj.appLabelEn, lang);
            const bullets = txList(proj.bulletsEs, proj.bulletsEn, lang);

            return (
              <div
                key={proj.id}
                className={`pj-acc-item mode-v2 ${isOpen ? 'is-open' : ''} ${isKbdFocused ? 'is-kbd-focus' : ''}`}
                style={{
                  '--item-accent': proj.colorAccent,
                  '--item-rgb': proj.colorRgb
                }}
              >
                {/* FILA CABECERA CLICKEABLE SIN RUIDO */}
                <button
                  type="button"
                  className="pj-acc-trigger"
                  onMouseEnter={() => setKbdIdx(idx + 1)}
                  onClick={() => toggleProject(proj.id)}
                  aria-expanded={isOpen}
                >
                  <div className="pj-acc-trigger-left">
                    <span className="pj-git-node-dot" aria-hidden="true" />
                    <div className="pj-acc-titles">
                      <div className="pj-acc-title-row">
                        <span className="pj-acc-title">{proj.title}</span>
                      </div>
                      <span className="pj-acc-oneliner">{oneLiner}</span>
                    </div>
                  </div>

                  <div className="pj-acc-trigger-right">
                    <span className={`pj-acc-chevron ${isOpen ? 'is-open' : ''}`} aria-hidden="true">
                      {isOpen ? '−' : '+'}
                    </span>
                  </div>
                </button>

                {/* PANEL DESPLEGABLE UNIFICADO */}
                {isOpen && (
                  <div className="pj-acc-body">
                    {/* 1. PÁRRAFO DE PROPÓSITO CON BORDE LATERAL (SIN ETIQUETA) */}
                    <div className="pj-objective-banner">
                      <p className="pj-objective-text">{objective}</p>
                    </div>

                    {/* 2. VENTANA CON IMAGEN INICIAL DE LA APP (ESTILO QUANTLAMBDA) */}
                    <div className="ql-preview-frame pj-preview-frame">
                      <div className="ql-browser-bar">
                        <div className="ql-browser-dots">
                          <span />
                          <span />
                          <span />
                        </div>
                        <a
                          href={proj.appUrl}
                          target="_blank"
                          rel="noreferrer"
                          className="ql-browser-url"
                          title={appLabel}
                        >
                          {proj.displayUrl}
                        </a>
                        <span className="pj-browser-spacer" />
                      </div>

                      <a
                        href={proj.appUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="pj-preview-stage"
                        title={appLabel}
                      >
                        <img
                          src={proj.previewImg}
                          alt={proj.title}
                          className={`pj-preview-img ${proj.previewAlign === 'top' ? 'align-top' : ''}`}
                          loading="lazy"
                        />
                      </a>
                    </div>

                    {/* 3. BULLETS UNIFICADOS + BOTÓN CTA ÚNICO */}
                    <div className="pj-body-main-row">
                      <ul className="pj-clean-bullets">
                        {bullets.map(renderBulletWithBoldLead)}
                      </ul>

                      <div className="pj-body-side-actions">
                        <a
                          href={proj.appUrl}
                          target="_blank"
                          rel="noreferrer"
                          className="pj-repo-cta"
                          style={{
                            '--insp-accent': proj.colorAccent,
                            '--insp-rgb': proj.colorRgb
                          }}
                        >
                          <span>{appLabel}</span>
                        </a>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
