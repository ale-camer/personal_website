# Plan Maestro de Visión, Contenido y Hoja de Ruta (`MASTER_BLUEPRINT.md`)

Documento rector que define la filosofía centrada en el lector, la estructura de secciones y el plan de ejecución paso a paso para la reconstrucción de `alejandrocamerlengo.com`.

---

## 1. Filosofía Central: Un Laboratorio y Observatorio Abierto (No un Folleto de CV)

### 1.1 El Espíritu de la Web: "Leer, Jugar y Explorar"
El propósito principal del sitio **no es "vender un CV"**, sino ofrecer **valor real, analítico e interactivo a cualquier persona que entre**:
- Quien visita la página debe encontrar **análisis originales con datos reales y tesis propia** (*para leer*) y **aplicaciones/simuladores interactivos** (*para jugar y aprender*).
- El posicionamiento profesional hacia **AI Engineer (AIE) End-to-End** (con base en Finanzas/Matemática $\rightarrow$ Data Science $\rightarrow$ Data Engineering en **Tongo** $\rightarrow$ Sistemas Agénticos) no se impone como un discurso de ventas en la portada, sino que **se demuestra por añadidura** a través de la calidad de lo que está construido y analizado en la web, complementado por una pestaña dedicada de **Trayectoria**.

### 1.2 Criterio de Curaduría: Qué se descarta vs. Qué se potencia de `_legacy/`
1. **Se descarta lo comoditizado por LLMs:**
   - Tutoriales teóricos de manual exportados de Jupyter (*Introducción al Álgebra Lineal*, *Normas Vectoriales*) y herramientas viejas que exigían subir archivos `.txt` o `.xlsx` manuales (*Keyphrases*, *Seasonality*), ya que hoy cualquiera las resuelve con un prompt.
2. **Se rescata y potencia lo que tiene ADN propio (*Authorial Skin in the Game*):**
   - **Investigaciones ad-hoc hechas 100% a pulmón con conocimiento de dominio:** como el análisis sobre **Macroeconomía, Inflación, Gasto Público y Degradación del Mercado Laboral en Argentina** (donde el valor no está en "tirar un comando de Python", sino en el criterio económico, el conocimiento institucional de figuras como *Monotributo Social vs. Autónomos vs. Empleo Privado Formal* y la lectura estructural de los datos).
   - **Proyectos de aprendizaje (*Learning by Building*):** aplicaciones construidas para dominar tecnologías o explorar preguntas reales (*Spark Encyclopedia*, *Global Quality of Life Explorer*, *BTC Dashboard*, *World Map*), presentadas con una estructura clara y *user-friendly*.

---

## 2. Arquitectura de Contenido y Topología de Subdominios

### 2.1 Topología de Despliegue en Subdominios
La web central y cada una de las aplicaciones satélite (proyectos interactivos y análisis profundo) operan bajo una arquitectura de **subdominios dedicados**, permitiendo despliegues independientes, URLs limpias y desacople total:

| Dominio / Subdominio Objetivo | URL Productiva Actual (Origen) | Contenido / Aplicación | Estado |
| :--- | :--- | :--- | :--- |
| **`alejandrocamerlengo.com`** | *(Por mapear)* | **Web Personal Central:** Portada (`Home`), `Mi CV` (Timeline 2011–2026), Hub de Proyectos y Análisis con enlaces directos a sus subdominios. | En desarrollo / Base activa |
| **`spark.alejandrocamerlengo.com`** | `https://spark-encyclopedia-pro-twg7ion2rq-uc.a.run.app/?phase=contexto` | **Spark Learning:** Enciclopedia interactiva y grafo de decisiones de Apache Spark 3.5. | En producción (Cloud Run `200 OK`) |
| **`worldmap.alejandrocamerlengo.com`** | `https://mi-servicio-726519885138.us-central1.run.app/` | **World Map Explorer:** Visualizador geográfico interactivo multi-idioma. | En producción (Cloud Run `200 OK`) |
| **`explorer.alejandrocamerlengo.com`** | `https://storage.googleapis.com/global-qol-explorer-frontend/index.html` | **World Quality of Life Explorer:** Comparador de calidad de vida global (Frontend GCS + API Cloud Run `qol-api-service`). | En producción (`200 OK`) |
| **`macro.alejandrocamerlengo.com`** | *(Repo `argentina-macro-pipeline`)* | **Análisis Macroeconómico:** Investigación interactiva sobre Macroeconomía, Gasto Público y Empleo en Argentina. | Pipeline productivo (`OK_DETERMINISTIC`) + UI nativa en React |
| **`quantlambda.dev`** | `https://quantlambda.dev` | **Proyecto Estrella:** Plataforma financiera cuantitativa y comité multi-agente en GCP. | En producción (Dominio propio) |

```text
+-----------------------------------------------------------------------------------+
| 0. MARCO GLOBAL (Avatar/Chat WhatsApp • Menú 3 Vistas • Idioma Modal • Dark/Light)|
+-----------------------------------------------------------------------------------+
|  PORTADA (HOME): Animación corta de arranque (AC) -> Terminal Guía Interactiva    |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ 1. PROYECTOS ]  (#proyectos)                                                   |
|     ├── PROYECTO INSIGNIA (Destacado arriba): QuantLambda (quantlambda.dev)       |
|     │   Plataforma principal de mercados globales, carteras e IA en producción.   |
|     └── EXPLORADORES / LABORATORIO (Desplegables abajo):                          |
|         • Spark Learning  • World Map  • Quality of Life Explorer                 |
|                                                                                   |
|  [ 2. ANÁLISIS ]   (#analisis)                                                    |
|     • Investigaciones propias con datos primarios y criterio de dominio           |
|       (Macroeconomía, Gasto Público y Empleo en Argentina + futuros estudios).    |
|                                                                                   |
|  [ 3. MI CV ]      (#mi-cv)                                                       |
|     • Timeline DAG de Doble Eje (2011–2026): Experiencia (izq) vs Educación (der) |
|     • Botón directo para descargar CV en PDF en la barra superior HUD.            |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

### Detalle de cada Pilar y Criterio de Presentación
- **Enfoque centrado en el usuario/lector (Producto primero, Ingeniería en su lugar):** Los nombres, bajadas y bullets hablan siempre desde el valor para quien usa la aplicación o lee el análisis (sin sopa de tecnologías ni etiquetas redundantes). Quien quiera indagar en el *cómo está construido* (Tech Recruiters / Hiring Managers) cuenta con los enlaces dedicados a telemetría, pipelines y documentación técnica.

| Pestaña | Rol para el Visitante / Recruiter | Contenido y Jerarquía |
| :--- | :--- | :--- |
| **1. `Proyectos` (`#proyectos`)** | Ver de inmediato tu capacidad de construir productos reales end-to-end sin perderse la plataforma principal. | • **Arriba (Proyecto Insignia abierto):** **QuantLambda (`quantlambda.dev`)**, presentado explícitamente como tu plataforma principal.<br>• **Abajo (Exploradores / Desarrollos de práctica, cerrados por defecto):** *Spark Learning*, *World Map* y *Quality of Life Explorer*, enmarcados con naturalidad como desarrollos acotados de exploración e interactividad. |
| **2. `Análisis` (`#analisis`)** | Demostrar tu diferencial frente a un perfil 100% dev puro: criterio económico, financiero y estadístico sobre problemas reales. | • **Ensayo interactivo:** *Macroeconomía, Gasto Público y Degradación del Empleo en Argentina (1980–Presente)* alimentado automáticamente por `argentina-macro-pipeline`.<br>• Estructura lista para sumar futuros estudios propios. |
| **3. `Mi CV` (`#mi-cv`)** | Validar en segundos tu seniority, empresas y formación académica (y llevarse el PDF estándar ATS en 1 clic). | • **Grafo DAG proporcional (`2011–2026`):** *Best Day $\rightarrow$ Portfolio Manager $\rightarrow$ Balanz $\rightarrow$ Lumen $\rightarrow$ AB InBev $\rightarrow$ Siemens Advanta $\rightarrow$ **Tongo*** y *UNLZ $\rightarrow$ UBA Finanzas $\rightarrow$ UBA Data Science $\rightarrow$ UCEMA*.<br>• Acción directa **`Descargar CV (PDF)`** en la barra HUD. |

---

## 3. Orden de Ejecución y Hoja de Ruta (De Mayor a Menor Esfuerzo de Desarrollo)

El desarrollo se organiza en **5 etapas secuenciales**, comenzando por el marco estructural y avanzando desde los módulos que requieren mayor construcción a medida dentro de este repositorio hacia los que integran plataformas ya existentes:

1. **Etapa 1 — Diseño General de la Web (Marco Estructural y Sistema de Diseño):**
   - Inicialización del proyecto moderno (**React + Vite**).
   - Definición del sistema de diseño dual (**Dark Mode Técnico** + **Light Mode Editorial** con personalidad propia, inspirado en las buenas prácticas de `quantlambda.dev`).
   - Construcción del *App Shell*: cabecera, navegación entre las vistas (*Inicio*, *Investigaciones*, *Playground*, *Trayectoria*), pie de página y base multi-idioma (`ES` / `EN` escalable).
2. **Etapa 2 — Trayectoria (Timeline Proporcional de Doble Eje `2011–2026`):**
   - Construcción a medida del motor geométrico de línea de tiempo vertical (`2011` a `2026`) con alturas proporcionales a la duración real de cada etapa laboral y educativa.
   - Integración de los datos actualizados (incluyendo **Tongo** y todas las etapas previas) y del panel interactivo de detalle (*click-to-expand*).
3. **Etapa 3 — Investigaciones (Motor de Ensayos Interactivos + Macroeconomía Argentina):**
   - Diseño del layout de lectura editorial e integración de componentes de visualización interactiva (adaptables a Dark/Light mode) reemplazando las viejas tablas y gráficos estáticos de Jupyter.
   - Migración, pulido visual y puesta en valor del análisis de **Macroeconomía y Mercado Laboral Argentino** como primer ensayo insignia.
4. **Etapa 4 — Playground (Hub de Proyectos de Aprendizaje y Mejoras de UX):**
   - Creación de la sección **Playground** con tarjetas interactivas, contexto de aprendizaje (*qué problema o tecnología motivó cada desarrollo*), previsualización y lanzamiento limpio.
   - Iteración opcional sobre el diseño/UX de los proyectos de juguete para darles cohesión visual.
5. **Etapa 5 — Proyecto Estrella (`QuantLambda` Showcase):**
   - Construcción del bloque destacado de **QuantLambda (`quantlambda.dev`)**: resumen visual e interactivo de su arquitectura end-to-end (`P-01..P-11`), sus capacidades cuantitativas/agénticas y el puente directo hacia la plataforma en producción.
6. **Paso $n-1$ (Etapa 6) — Diseño del Ícono de la Pestaña (*Favicon*):**
   - Diseño e iteración del ícono/monograma que se muestra en la pestaña del navegador (`index.html` / `public/`), alineado con la identidad visual definitiva de la web.
7. **Paso $n$ (Etapa 7) — Documentación Integral de la Aplicación:**
   - Documentación técnica y funcional completa de la aplicación (`README.md`, arquitectura de componentes, configuración de variables de entorno como `gemini-flash`, estructura de datos de ensayos/timeline y guía de despliegue/mantenimiento).

---

## 4. Estado Actual y Plan Formal de Próximos Pasos (Hoja de Ruta de Cierre)

### 4.1 Hitos Completados (`Hecho`)
1. **`Mi CV` (`#mi-cv`, antes `Recorrido`)**:
   - Renombrado en la navegación y rutas (`#mi-cv`).
   - Limpieza de etiquetas técnicas artificiales (`RUNNING`, `SUCCESS`, `ARTIFACT`, `pipeline: ...` y tags), nodos en 2 líneas (Rol/Título + Empresa/Universidad) con timestamp a la derecha, e incorporación del contenido actualizado del CV (`profile.json` + Portfolio Manager + Best Day Travel Group + planes de estudio universitarios) — **hecho**.
2. **`Análisis` (`#analisis` y `#analisis/macro-argentina`)**:
   - Pipeline mensual automatizado en repositorio dedicado (`argentina-macro-pipeline`) conectado a las 7 fuentes oficiales + proyección SARIMAX a 6 meses.
   - Renderizado nativo e interactivo en React (`MacroCharts.jsx` + `ResearchSection.jsx`) sin scroll horizontal y reactivo al cambio de idioma — **hecho**.
3. **`Proyectos` (`#proyectos`)**:
   - Lavada de cara estética y despliegue productivo de las 3 aplicaciones interactivas (*Spark Pipeline & Encyclopedia*, *World Map Explorer* y *Global Quality of Life Explorer*) — **hecho**.
   - Incorporación de marco visual con imagen/vista previa inicial en cada proyecto al estilo de `QuantLambda` — **hecho**.
4. **Infraestructura Cloud & Keepalive**:
   - Verificación en BigQuery Studio de los proyectos activos y automatización quincenal del keepalive para MongoDB Atlas (`P-04` y `P-07`) en `portfolio-infra` — **hecho**.

---

### 4.2 Plan de Ejecución Actualizado (De Acá al Cierre)

| Orden | Fase / Tarea | Alcance y Detalle | Estado |
| :--- | :--- | :--- | :--- |
| **Base UX** | **Diseño General HUD, Tipografía y Limpieza de Etiquetas (Sub-pasos 1.1 a 1.4)** | • Contenedor central HUD con barra superior fija (`SectionView.jsx`), unificación tipográfica en 3 familias (`Orbitron`, `Plus Jakarta Sans`, `JetBrains Mono`), descripciones orientadas al usuario, escalado Retina (`devicePixelRatio`) y purga de etiquetas sobrantes. | **Hecho** |
| **Paso 1** | **Consolidación en 3 Pestañas (`Proyectos` · `Análisis` · `Mi CV`) + Descarga PDF** | • Simplificar el menú superior a las **3 vistas autoexplicativas (`Proyectos` · `Análisis` · `Mi CV`)** (manteniendo redirección limpia si alguien entra a `#quantlambda`).<br>• Dentro de **`Proyectos`**: ubicar **`QuantLambda` arriba como Proyecto Insignia** (abierto y protagonista) y debajo un bloque diferenciado y honesto de **Exploradores / proyectos de práctica** (*Spark Learning*, *World Map*, *Quality of Life Explorer*, iniciando cerrados).<br>• Dentro de **`Mi CV`**: sumar en la barra superior fija HUD el botón directo para **descargar el CV en PDF**. | **Hecho** |
| **Paso 2** | **Portada (`Home`): Apertura `> Welcome` + Terminal Guía `AI CLI Moderna` + Navegación 100% Teclado** | • Secuencia de apertura corta (`1C-5` escribiendo `> Welcome` antes de abrir la app).<br>• **Terminal Guía del Home (`03 · AI CLI Moderna` sobre estructura `T1`)**: saludo, agradecimiento, qué vas a encontrar y viñetas de comandos (`1`, `2`, `3`, `c`, `gh/li/gm`, `l`, `t`) + prompt interactivo inferior con soporte de navegación 100% por teclado en toda la web. | **Hecho** |
| **Paso 3** | **Pulido de `Light Mode`, Chat WhatsApp y Resguardo de API Key** | • Contraste y estética pulidos en **Modo Claro (`Light Mode`)** en las 3 vistas (`Proyectos`, `Análisis`, `Mi CV`), la Terminal `AI CLI Moderna` y los 5 gráficos nativos de Macro.<br>• Contexto del chat estilo WhatsApp (`IdentityBadge.jsx`) actualizado a las 3 vistas + atajos de teclado y resguardo de clave privada (sin exponer `VITE_GEMINI_API_KEY` en el bundle cliente, soportando proxy `VITE_CHAT_API_URL`). | **Hecho** |
| **Paso 4** | **Selector Modal de Idioma (~56 idiomas) + Traducción Integral** | • Reemplazado el dropdown provisorio inferior derecho por la **ventana modal centrada con buscador en lengua nativa y 56 banderas SVG** (`LanguageModal.jsx` + `FlagBadge`, estilo `quantlambda.dev`).<br>• Traducción integral de todos los textos definitivos cerrados (`Home`/Terminal, `Proyectos`/`QuantLambda`, `Análisis`, `Mi CV`, Chat y UI global) en los 56 idiomas (`ES`, `EN` + 54 diccionarios en `public/locales/`). | **Hecho** |
| **Paso 5 (`n-1`)** | **Diseño del Ícono de la Pestaña (*Favicon*)** | • Diseñado y fijado en `public/favicon.svg` + `index.html` el monograma geométrico con chevrons de terminal (`#07 · ∧⊂_`: la `A` como chevron ascendente `∧` con punto esmeralda, la `C` como chevron lateral `<` y el cursor `_`). | **Hecho** |
| **Paso 6 (`n`)** | **Documentación Integral, Subdominios y Puesta en Producción** | • Documentación técnica y funcional completa (`README.md`) para quien quiera indagar en el *cómo se construyó*, junto con configuraciones productivas (`Dockerfile`, `nginx.conf`, `vercel.json`, `.env.example`).<br>• Configuración de DNS y despliegue productivo: `alejandrocamerlengo.com` (web central) + `spark.`, `worldmap.`, `explorer.`, `macro.` (más `quantlambda.dev`). | **Hecho** |
| **Paso 7 (`Post-Web`)** | **Lavada de Cara del Perfil de GitHub (`github.com/ale-camer`)** | • Rediseño integral de la página de inicio del perfil personal de GitHub (repositorio especial `ale-camer/ale-camer` -> `README.md` de portada).<br>• Alineación visual y narrativa con `alejandrocamerlengo.com` y `quantlambda.dev`: presentación limpia y directa, enlaces a la web central y sus subdominios (`quantlambda.dev`, `macro.`, `spark.`, `worldmap.`, `explorer.`), y curaduría de los **Pinned Repositories** principales. | **Pendiente (Próximo objetivo al cerrar el deploy)** |
