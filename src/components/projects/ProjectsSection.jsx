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

export default function ProjectsSection({
  colorMode = 'dark',
  lang = 'ES',
  onHudChange
}) {
  useSiteLocale(lang);
  // Opción C: 4 filas ejecutivas compactas por defecto; clic o Enter despliega bajo demanda
  const [openId, setOpenId] = useState(null);
  // 0 = QuantLambda, 1..3 = los 3 proyectos exploratorios
  const [kbdIdx, setKbdIdx] = useState(0);
  const [explorerHref, setExplorerHref] = useState('https://explorer.alejandrocamerlengo.com');

  const toggleProject = (id) => {
    setOpenId((prev) => (prev === id ? null : id));
  };

  useEffect(() => {
    if (!onHudChange) return;
    if (openId) {
      onHudChange({
        onCollapseAll: () => setOpenId(null),
        collapseLabel: tx('Contraer todos ▴', 'Collapse all ▴', lang)
      });
    } else {
      onHudChange(null);
    }
    return () => onHudChange(null);
  }, [openId, lang, onHudChange]);

  // Pre-calienta los servicios al abrir la sección Proyectos y verifica resolución DNS de explorer
  useEffect(() => {
    const urls = [
      'https://worldmap.alejandrocamerlengo.com/api/countries',
      'https://qol-frontend-450135571603.us-central1.run.app/',
      'https://qol-api-service-450135571603.us-central1.run.app/api/v1/metadata/indicators',
      'https://spark.alejandrocamerlengo.com/'
    ];
    urls.forEach((u) => {
      fetch(u, { mode: 'no-cors', cache: 'no-store' }).catch(() => {});
    });

    fetch('https://explorer.alejandrocamerlengo.com/', { mode: 'no-cors', cache: 'no-store' }).catch(
      () => {
        setExplorerHref('https://qol-frontend-450135571603.us-central1.run.app');
      }
    );
  }, []);

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
          toggleProject('quantlambda');
        } else {
          const proj = PLAYGROUND_PROJECTS[kbdIdx - 1];
          if (proj) toggleProject(proj.id);
        }
      }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [kbdIdx]);

  const isQlOpen = openId === 'quantlambda';

  return (
    <div className="pj-root pj-mode-compact-c">
      {/* SUBTÍTULO GUÍA EJECUTIVO */}
      <div className="pj-compact-intro">
        <p className="pj-purpose-lead">
          {tx(
            'Tocá cualquier proyecto para desplegar su vista previa interactiva y detalles acá mismo, o abrí cada aplicación en vivo:',
            'Tap any project to expand its interactive preview and details right here, or launch each live application directly:',
            lang
          )}
        </p>
      </div>

      {/* 1. FILA EJECUTIVA INSIGNIA: QUANTLAMBDA (COLAPSABLE BAJO DEMANDA) */}
      <div
        className={`pj-acc-item mode-v2 pj-flagship-acc ${isQlOpen ? 'is-open' : ''} ${kbdIdx === 0 ? 'is-kbd-focus' : ''}`}
        style={{
          '--item-accent': '#10b981',
          '--item-rgb': '16, 185, 129'
        }}
      >
        <div
          role="button"
          tabIndex={0}
          className="pj-acc-trigger pj-flagship-trigger"
          onMouseEnter={() => setKbdIdx(0)}
          onClick={() => toggleProject('quantlambda')}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              toggleProject('quantlambda');
            }
          }}
          aria-expanded={isQlOpen}
        >
          <div className="pj-acc-trigger-left">
            <div className="pj-acc-titles">
              <div className="pj-acc-title-row">
                <span className="pj-flagship-badge">
                  <i className="pj-flagship-dot" aria-hidden="true" />
                  {tx('PROYECTO INSIGNIA', 'FLAGSHIP PROJECT', lang)}
                </span>
                <span className="pj-acc-title">QuantLambda</span>
                <span className="pj-domain-tag">quantlambda.dev</span>
              </div>
              <span className="pj-acc-oneliner">
                {tx(
                  'Plataforma en vivo para seguir 213 activos globales, analizar opciones y tasas en 3D y simular el riesgo de carteras.',
                  'Live platform to track 213 global assets, inspect 3D options & yield curves, and stress-test portfolio risk.',
                  lang
                )}
              </span>
            </div>
          </div>

          <div className="pj-acc-trigger-right">
            <a
              href="https://quantlambda.dev"
              target="_blank"
              rel="noreferrer"
              className="pj-quick-launch-pill is-flagship"
              onClick={(e) => e.stopPropagation()}
            >
              {tx('Abrir App ↗', 'Open App ↗', lang)}
            </a>
            <span className={`pj-row-chevron ${isQlOpen ? 'is-open' : ''}`} aria-hidden="true">
              {isQlOpen ? '▴' : '▾'}
            </span>
          </div>
        </div>

        {isQlOpen && (
          <div className="pj-acc-body pj-flagship-body">
            <QuantLambdaSection
              colorMode={colorMode}
              lang={lang}
              hideTopBanner={true}
            />
          </div>
        )}
      </div>

      {/* 2. LAS 3 APLICACIONES INTERACTIVAS COMPACTAS */}
      <div className="pj-acc-list mode-compact-list">
        {PLAYGROUND_PROJECTS.map((proj, idx) => {
          const isOpen = openId === proj.id;
          const isKbdFocused = kbdIdx === idx + 1;
          const oneLiner = tx(proj.oneLinerEs, proj.oneLinerEn, lang);
          const objective = tx(proj.objectiveEs, proj.objectiveEn, lang);
          const appLabel = tx(proj.appLabelEs, proj.appLabelEn, lang);
          const bullets = txList(proj.bulletsEs, proj.bulletsEn, lang);
          const resolvedUrl = proj.id === 'world-bank-qol' ? explorerHref : proj.appUrl;
          const cleanDomain = proj.displayUrl.replace(/^https?:\/\//, '');

          return (
            <div
              key={proj.id}
              className={`pj-acc-item mode-v2 ${isOpen ? 'is-open' : ''} ${isKbdFocused ? 'is-kbd-focus' : ''}`}
              style={{
                '--item-accent': proj.colorAccent,
                '--item-rgb': proj.colorRgb
              }}
            >
              <div
                role="button"
                tabIndex={0}
                className="pj-acc-trigger"
                onMouseEnter={() => setKbdIdx(idx + 1)}
                onClick={() => toggleProject(proj.id)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleProject(proj.id);
                  }
                }}
                aria-expanded={isOpen}
              >
                <div className="pj-acc-trigger-left">
                  <span className="pj-git-node-dot" aria-hidden="true" />
                  <div className="pj-acc-titles">
                    <div className="pj-acc-title-row">
                      <span className="pj-acc-title">{proj.title}</span>
                      <span className="pj-domain-tag">{cleanDomain}</span>
                    </div>
                    <span className="pj-acc-oneliner">{oneLiner}</span>
                  </div>
                </div>

                <div className="pj-acc-trigger-right">
                  <a
                    href={resolvedUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="pj-quick-launch-pill"
                    onClick={(e) => e.stopPropagation()}
                  >
                    {tx('Abrir ↗', 'Open ↗', lang)}
                  </a>
                  <span className={`pj-row-chevron ${isOpen ? 'is-open' : ''}`} aria-hidden="true">
                    {isOpen ? '▴' : '▾'}
                  </span>
                </div>
              </div>

              {isOpen && (
                <div className="pj-acc-body">
                  <div className="pj-objective-banner">
                    <p className="pj-objective-text">{objective}</p>
                  </div>

                  <div className="ql-preview-frame pj-preview-frame">
                    <div className="ql-browser-bar">
                      <div className="ql-browser-dots">
                        <span />
                        <span />
                        <span />
                      </div>
                      <a
                        href={resolvedUrl}
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
                      href={resolvedUrl}
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

                  <ul className="pj-clean-bullets">
                    {bullets.map(renderBulletWithBoldLead)}
                  </ul>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
