import React, { useState } from 'react';

export const PLAYGROUND_PROJECTS = [
  {
    id: 'spark-encyclopedia',
    num: '01',
    hash: 'a94f2c',
    branch: 'feat/spark-3.5-internals',
    title: 'Spark Pipeline Architecture & Encyclopedia',
    oneLiner: 'Grafo interactivo de decisiones en 6 fases y enciclopedia técnica de Apache Spark 3.5.',
    objective:
      'Bajar a tierra el funcionamiento interno de Apache Spark 3.5 (gestión unificada de memoria, Shuffle, Data Skew, AQE y Catalyst) transformando conceptos abstractos de sistemas distribuidos en un grafo de decisiones interactivo.',
    domain: 'Data & AI Engineering',
    colorAccent: '#f43f5e',
    colorRgb: '244, 63, 94',
    appUrl: '#proyectos/spark-encyclopedia',
    appLabel: 'Abrir Spark Encyclopedia ↗',
    flow: ['Cluster & RAM', 'Ingest & Parquet', 'Shuffle & AQE', 'Serving Sink'],
    bullets: [
      'Grafo interactivo (React Flow) con los trade-offs reales de cada etapa del pipeline.',
      'Modales "Deep Dive" con código PySpark, planes físicos y mitigación de cuellos de botella.',
      'Buscador unificado que conecta decisiones de arquitectura con artículos técnicos.'
    ],
    tags: ['Apache Spark 3.5', 'PySpark', 'React Flow', 'TypeScript', 'AQE']
  },
  {
    id: 'crypto-analytics',
    num: '02',
    hash: 'e31b80',
    branch: 'feat/polars-airflow-gcp',
    title: 'Crypto Analytics Platform (Polars + Airflow)',
    oneLiner: 'Pipeline ETL diario con cálculo vectorial en Polars, Airflow 3, BigQuery y Terraform.',
    objective:
      'Dominar el stack moderno de ingeniería de datos reemplazando Pandas por procesamiento vectorial in-memory con Polars (Rust), orquestación productiva en Apache Airflow 3 e infraestructura reproducible con Terraform sobre GCP.',
    domain: 'Data Engineering & Quant',
    colorAccent: '#10b981',
    colorRgb: '16, 185, 129',
    appUrl: '#proyectos/crypto-analytics',
    appLabel: 'Abrir Crypto Analytics App ↗',
    flow: ['Market REST API', 'Polars Engine', 'GCS Raw Lake', 'BigQuery DWH'],
    bullets: [
      'Cálculo vectorizado de MACD, RSI y Bandas de Bollinger en memoria con Polars.',
      'Data Lake inmutable en Cloud Storage y tablas analíticas particionadas en BigQuery.',
      'Infraestructura 100% como código (IaC) aprovisionada con Terraform y Docker.'
    ],
    tags: ['Polars', 'Apache Airflow 3', 'GCP BigQuery', 'Terraform', 'Python 3.12']
  },
  {
    id: 'geospatial-world-map',
    num: '03',
    hash: '7d2c19',
    branch: 'feat/folium-i18n-atlas',
    title: 'World Map & Geospatial Explorer',
    oneLiner: 'Cartografía interactiva en 15 idiomas con Folium/Leaflet, estadísticas por continente y Excel.',
    objective:
      'Explorar la visualización de datos geoespaciales (GeoJSON, Folium y Leaflet.js) e implementar una arquitectura multi-idioma completa (15 lenguajes, incluyendo escrituras RTL y CJK) con importación/exportación de datos en Excel.',
    domain: 'Geospatial Analytics',
    colorAccent: '#38bdf8',
    colorRgb: '56, 189, 248',
    appUrl: '#proyectos/geospatial-world-map',
    appLabel: 'Abrir World Map Explorer ↗',
    flow: ['GeoJSON ISO', 'Excel I/O', 'Folium Layers', '15-Lang Stats'],
    bullets: [
      'Selección interactiva de países con cambio de mapas base (Positron, OSM, Dark Matter).',
      'Métricas en vivo de cobertura por continente y subregión geográfica.',
      'Interfaz traducida a 15 idiomas e integrada con carga/descarga de plantillas Excel.'
    ],
    tags: ['Python', 'Flask', 'Folium / Leaflet', 'GeoJSON', 'Pandas']
  },
  {
    id: 'world-bank-qol',
    num: '04',
    hash: '4f89a1',
    branch: 'feat/worldbank-macro-api',
    title: 'Global Socioeconomic & World Bank Explorer',
    oneLiner: 'Comparador entre países sobre 19 indicadores estructurales del Banco Mundial.',
    objective:
      'Aprender a consumir, limpiar y armonizar series macroeconómicas internacionales desde la API oficial del Banco Mundial para contrastar desarrollo, estructura productiva, energía y empleo entre países.',
    domain: 'Macroeconomics & Viz',
    colorAccent: '#f59e0b',
    colorRgb: '245, 158, 11',
    appUrl: '#proyectos/world-bank-qol',
    appLabel: 'Abrir World Bank Explorer ↗',
    flow: ['World Bank API', '19 Indicators', 'Time / Ranking', 'Comparative Plot'],
    bullets: [
      'Cruza PBI per cápita, exportaciones high-tech, crédito privado, energía nuclear y empleo.',
      'Doble vista: evolución histórica de un país o ranking comparativo transversal por año.',
      'Normalización automática de series internacionales con ventanas temporales dispares.'
    ],
    tags: ['World Bank API', 'Macro Data', 'Python', 'Pandas', 'Time Series']
  }
];

export default function ProjectsSection() {
  const [openId, setOpenId] = useState('spark-encyclopedia');

  const toggleProject = (id) => {
    setOpenId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="pj-root">
      {/* CABECERA CON EL PROPÓSITO GENERAL DE ESTOS PROYECTOS */}
      <div className="pj-purpose-header">
        <div className="tl-eyebrow">SYS.LAB // LEARNING BY BUILDING • PROYECTOS DE APRENDIZAJE</div>
        <h2 className="tl-main-title">
          Aprender tecnologías y dominar problemas construyendo aplicaciones de punta a punta
        </h2>
        <p className="pj-purpose-lead">
          Cada uno de estos desarrollos nació con un <strong>objetivo técnico concreto</strong>:
          elegir un motor distribuido, un stack de datos o un dominio nuevo y construir una
          herramienta funcional para entenderlo a fondo. Hacé click en cualquiera para ver qué
          busqué aprender y cómo está armado.
        </p>
      </div>

      {/* LISTA ESTILO GIT MINIMAL (SUBRAYADO EDITORIAL EXPANDIBLE) */}
      <div className="pj-acc-list mode-git">
        {PLAYGROUND_PROJECTS.map((proj) => {
          const isOpen = openId === proj.id;

          return (
            <div
              key={proj.id}
              className={`pj-acc-item mode-v2 ${isOpen ? 'is-open' : ''}`}
              style={{
                '--item-accent': proj.colorAccent,
                '--item-rgb': proj.colorRgb
              }}
            >
              {/* FILA CABECERA CLICKEABLE */}
              <button
                type="button"
                className="pj-acc-trigger"
                onClick={() => toggleProject(proj.id)}
                aria-expanded={isOpen}
              >
                <div className="pj-acc-trigger-left">
                  <span className="pj-git-node-dot" aria-hidden="true" />
                  <span className="pj-acc-code">commit {proj.hash}</span>
                  <div className="pj-acc-titles">
                    <div className="pj-acc-title-row">
                      <span className="pj-acc-title">{proj.title}</span>
                      <span className="pj-git-branch-pill">{proj.branch}</span>
                    </div>
                    <span className="pj-acc-oneliner">{proj.oneLiner}</span>
                  </div>
                </div>

                <div className="pj-acc-trigger-right">
                  <div className="pj-acc-preview-tags">
                    {proj.tags.slice(0, 3).map((t) => (
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

              {/* PANEL DESPLEGABLE IN-PLACE CON EL OBJETIVO EXPLÍCITO */}
              {isOpen && (
                <div className="pj-acc-body">
                  {/* BLOQUE EXPLÍCITO: OBJETIVO DEL PROYECTO (QUÉ BUSQUÉ APRENDER / RESOLVER) */}
                  <div className="pj-objective-banner">
                    <span className="pj-objective-tag">OBJETIVO DE APRENDIZAJE // POR QUÉ LO CONSTRUÍ</span>
                    <p className="pj-objective-text">{proj.objective}</p>
                  </div>

                  {/* Pipeline visual de 4 nodos */}
                  <div className="pj-flow-strip">
                    {proj.flow.map((step, idx) => (
                      <React.Fragment key={step}>
                        <div className="pj-flow-node">
                          <span className="pj-flow-idx">0{idx + 1}</span>
                          <span className="pj-flow-label">{step}</span>
                        </div>
                        {idx < proj.flow.length - 1 && (
                          <span className="pj-flow-connector" aria-hidden="true">
                            ───●
                          </span>
                        )}
                      </React.Fragment>
                    ))}
                  </div>

                  {/* 3 Bullets de qué hace + Tags + Botón al repositorio */}
                  <div className="pj-body-main-row">
                    <ul className="pj-clean-bullets">
                      {proj.bullets.map((b) => (
                        <li key={b}>{b}</li>
                      ))}
                    </ul>

                    <div className="pj-body-side-actions">
                      <div className="pj-all-tags">
                        {proj.tags.map((t) => (
                          <span key={t} className="tl-tag-pill">
                            {t}
                          </span>
                        ))}
                      </div>

                      <a
                        href={proj.appUrl}
                        className="pj-repo-cta"
                        style={{
                          '--insp-accent': proj.colorAccent,
                          '--insp-rgb': proj.colorRgb
                        }}
                      >
                        <span>{proj.appLabel}</span>
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
  );
}
