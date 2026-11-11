# Alejandro Camerlengo — Personal Observatory & Engineering Hub (`alejandrocamerlengo.com`)

[![React 19](https://img.shields.io/badge/React-19.2-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Vite 8](https://img.shields.io/badge/Vite-8.0-646CFF?logo=vite&logoColor=white)](https://vite.dev/)
[![Oxlint](https://img.shields.io/badge/Oxlint-Zero_Warnings-10b981)](https://oxc.rs/)
[![Locales](https://img.shields.io/badge/i18n-56_Languages-38bdf8)](#4-sistema-de-internacionalizacion-56-idiomas)
[![Keyboard Navigation](https://img.shields.io/badge/UX-100%25_Keyboard_First-f59e0b)](#3-navegacion-100-con-teclado-y-terminal-interactiva)

Repositorio central de **`alejandrocamerlengo.com`**: un observatorio técnico, analítico e interactivo diseñado bajo la premisa de **"Leer, Jugar y Explorar"** en lugar de un folleto estático de CV.

---

## 1. Filosofía de Producto y Diseño

El sitio está concebido bajo tres principios:
1. **Valor Real para el Visitante (*Product-First*):** Quien entra encuentra plataformas cuantitativas en producción, exploradores interactivos y ensayos macroeconómicos propios alimentados por pipelines automatizados.
2. **Navegación Dual (*Mouse + 100% Keyboard-First*):** Desde la secuencia de bienvenida (`> Welcome`) y la **Terminal Guía `AI CLI Moderna`** en la portada, toda la web se puede recorrer íntegramente con el teclado o mediante la interfaz visual HUD.
3. **Estética Técnica Dual (*Dark HUD & Editorial Light Mode*):** Sistema visual de alto contraste con escalado dinámico para pantallas HiDPI/Retina (`devicePixelRatio`), monograma geométrico con chevrons (`∧⊂_`) en [`public/favicon.svg`](public/favicon.svg) y tipografía unificada en tres familias (`Orbitron`, `Plus Jakarta Sans`, `JetBrains Mono`).

---

## 2. Arquitectura de Secciones y Topología de Subdominios

La aplicación se estructura en **Portada (`Home`)** + **3 Vistas Principales** (`Proyectos`, `Análisis`, `Mi CV`), articuladas con un ecosistema de subdominios independientes:

```text
+-----------------------------------------------------------------------------------+
| MARCO GLOBAL HUD (Avatar/Chat • 3 Vistas • Selector Modal 56 Idiomas • Dark/Light)|
+-----------------------------------------------------------------------------------+
| PORTADA (HOME): Secuencia "> Welcome" -> Terminal Guía Interactiva (AI CLI)       |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ 1. PROYECTOS ]  (#proyectos)                                                   |
|     ├── PROYECTO INSIGNIA (Abierto arriba): QuantLambda (quantlambda.dev)         |
|     │   Plataforma cuantitativa, monitoreo macro/mercados y comité multi-agente.  |
|     └── EXPLORADORES INTERACTIVOS (Acordeones desplegables abajo):                |
|         • Spark Learning (spark.alejandrocamerlengo.com)                          |
|         • World Map Explorer (worldmap.alejandrocamerlengo.com)                   |
|         • Quality of Life Explorer (explorer.alejandrocamerlengo.com)             |
|                                                                                   |
|  [ 2. ANÁLISIS ]   (#analisis • macro.alejandrocamerlengo.com)                    |
|     • Macroeconomía, Gasto Público y Degradación del Empleo en Argentina          |
|       (5 visualizaciones nativas SVG + proyección SARIMAX vía pipeline mensual).  |
|                                                                                   |
|  [ 3. MI CV ]      (#mi-cv)                                                       |
|     • Grafo DAG proporcional de doble eje (2011–2026): Experiencia vs. Educación  |
|     • Descarga directa de CV estándar ATS en PDF desde la barra superior HUD.     |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

### Mapa de Dominios y Servicios en Producción

| Dominio / Subdominio | Origen Productivo / Servicio | Descripción Técnica |
| :--- | :--- | :--- |
| **`alejandrocamerlengo.com`** | SPA Central (`personal_website`) | Hub principal, Terminal Guía `AI CLI`, Timeline DAG (`2011–2026`), proyectos y ensayo macro nativo. |
| **`quantlambda.dev`** | `https://quantlambda.dev` | **Proyecto Insignia:** Plataforma de inteligencia de mercados globales, optimización de carteras (`CVaR`/`HRP`) y comité multi-agente sobre 13 microservicios en GCP. |
| **`spark.alejandrocamerlengo.com`** | `https://spark-encyclopedia-pro-twg7ion2rq-uc.a.run.app/` | **Spark Learning:** Enciclopedia interactiva y simulador de arquitectura distribuida de Apache Spark 3.5. |
| **`worldmap.alejandrocamerlengo.com`** | `https://mi-servicio-726519885138.us-central1.run.app/` | **World Map Explorer:** Cartografía interactiva multi-idioma con proyecciones geográficas y datos demográficos. |
| **`explorer.alejandrocamerlengo.com`** | `https://storage.googleapis.com/global-qol-explorer-frontend/index.html` | **Quality of Life Explorer:** Comparador global de calidad de vida y poder adquisitivo (Frontend GCS + API Cloud Run `qol-api-service`). |
| **`macro.alejandrocamerlengo.com`** | Subdominio directo a `#analisis/macro-argentina` | **Análisis Macroeconómico:** Detectado automáticamente por `window.location.hostname.startsWith('macro.')` en [`src/App.jsx`](src/App.jsx) y alimentado por el pipeline mensual `argentina-macro-pipeline`. |

---

## 3. Navegación 100% con Teclado y Terminal Interactiva

Tanto escribiendo comandos dentro del prompt de la **Terminal Guía (`AI CLI Moderna`)** en el `Home` como presionando atajos directos en cualquier vista (cuando no hay un input de texto enfocado), el sitio responde a los siguientes comandos:

| Comando / Tecla | Acción en el Sitio |
| :--- | :--- |
| **`1`** | Ir a **Proyectos** (`#proyectos`: `QuantLambda` + Exploradores interactivos) |
| **`2`** | Ir a **Análisis** (`#analisis`: Investigaciones y ensayos con datos reales) |
| **`3`** | Ir a **Mi CV** (`#mi-cv`: Recorrido profesional y académico `2011–2026`) |
| **`c`** | Abrir o cerrar el **Chat interactivo** sobre el recorrido y proyectos de Alejandro |
| **`gh`** / **`li`** / **`gm`** | Abrir **GitHub** (`gh`), **LinkedIn** (`li`) o copiar/abrir **Gmail** (`gm`) |
| **`l`** | Abrir el **Selector Modal de Idioma** (56 idiomas con buscador en lengua nativa) |
| **`t`** | Alternar entre **Modo Oscuro (`Dark Mode`)** y **Modo Claro (`Light Mode`)** |
| **`d`** | *(En `Mi CV`)* Descargar directamente el **CV en formato PDF** |
| **`↑` `↓` `←` `→`** + **`Enter`** | Desplazarse entre tarjetas, proyectos, ensayos o nodos del CV y abrir/expandir el elemento activo |
| **`Esc`** | Cerrar modales activos, contraer vistas expandidas o volver a la portada (`Home`) |

---

## 4. Sistema de Internacionalización (56 Idiomas)

El motor de localización propio ([`src/i18n/languages.jsx`](src/i18n/languages.jsx) + [`src/i18n/localeService.js`](src/i18n/localeService.js) + [`src/components/LanguageModal.jsx`](src/components/LanguageModal.jsx)) ofrece soporte completo sin dependencias pesadas externas:
- **Idiomas base integrados en bundle:** Español (`es`) e Inglés (`en`) para carga instantánea (`0ms` de latencia de red).
- **54 diccionarios adicionales bajo demanda (`public/locales/<code >.json`):** Portugués (`pt`), Francés (`fr`), Alemán (`de`), Italiano (`it`), Japonés (`ja`), Chino Simplificado (`zh`), Chino Tradicional (`zht`), Coreano (`ko`), Árabe (`ar`, con soporte automático de layout `dir="rtl"`), Hebreo (`he`), Ruso (`ru`), Ucraniano (`uk`), Polaco (`pl`), Neerlandés (`nl`), Sueco (`sv`), Noruego (`no`), Danés (`da`), Finés (`fi`), Griego (`el`), Turco (`tr`), Hindi (`hi`), Bengalí (`bn`), Vietnamita (`vi`), Tailandés (`th`), Indonesio (`id`), Catalán (`ca`), Euskera (`eu`), Gallego (`gl`), entre otros (277 claves por idioma).
- **Banderas SVG vectoriales inline (`FlagBadge`):** Renderizadas directamente en SVG para garantizar nitidez en Linux, Windows y macOS sin depender de emojis de bandera del sistema operativo.

---

## 5. Estructura del Repositorio

```text
personal_website/
├── public/
│   ├── Alejandro_Camerlengo_Data_Engineer.pdf # CV descargable desde #mi-cv
│   ├── data/
│   │   └── macro_argentina.json               # Dataset vivo generado por argentina-macro-pipeline
│   ├── favicon.svg                            # Monograma geométrico ∧⊂_ con chevrons de terminal
│   ├── images/projects/                       # Vistas previas de los proyectos interactivos
│   └── locales/                               # 54 diccionarios JSON completos (277 claves c/u)
├── src/
│   ├── components/
│   │   ├── HomeCenterShowcase.jsx             # Apertura "> Welcome" + Terminal Guía AI CLI Moderna
│   │   ├── TopNavBar.jsx                      # Navegación superior (Proyectos · Análisis · Mi CV)
│   │   ├── SectionView.jsx                    # Contenedor HUD con cabecera fija y botón PDF
│   │   ├── IdentityBadge.jsx                  # Avatar + Chat estilo WhatsApp + Contacto
│   │   ├── LanguageModal.jsx                  # Modal centrado con buscador para los 56 idiomas
│   │   ├── quantlambda/QuantLambdaSection.jsx # Showcase del Proyecto Insignia (quantlambda.dev)
│   │   ├── projects/ProjectsSection.jsx       # Hub de Proyectos (Insignia + 3 Exploradores)
│   │   ├── research/
│   │   │   ├── ResearchSection.jsx            # Motor de ensayos + Macroeconomía Argentina
│   │   │   ├── MacroCharts.jsx                # 5 gráficos SVG interactivos + Lightbox
│   │   │   └── macroI18n.js                   # Traducciones del ensayo macroeconómico
│   │   └── timeline/TimelineSection.jsx       # Grafo DAG proporcional de doble eje (2011–2026)
│   ├── data/
│   │   ├── profile.json                       # Datos estructurados de experiencia y educación
│   │   ├── playground.json                    # Metadatos de proyectos interactivos
│   │   └── research.json                      # Catálogo y contenido base de ensayos
│   ├── i18n/
│   │   ├── languages.jsx                      # Catálogo de 56 idiomas + componente FlagBadge SVG
│   │   └── localeService.js                   # Hook useSiteLocale, tx(), txList() y caché de JSONs
│   ├── App.jsx                                # Enrutamiento hash, subdominio macro. y teclado global
│   └── index.css                              # Sistema de diseño CSS (Dark HUD + Light Mode Editorial)
├── docs/
│   └── MASTER_BLUEPRINT.md                    # Plan Maestro de visión, curaduría y arquitectura
├── Dockerfile                                 # Build multi-stage (Node 22 Alpine -> Nginx Alpine)
├── nginx.conf                                 # Servidor estático optimizado para Cloud Run (puerto 8080)
└── vercel.json                                # Reglas de ruteo SPA y cabeceras de caché para Vercel
```

---

## 6. Seguridad y Variables de Entorno

El bundle cliente **no expone ninguna clave privada ni API Key** (`VITE_GEMINI_API_KEY` fue desacoplada del frontend por seguridad).
- El asistente de chat en [`src/components/IdentityBadge.jsx`](src/components/IdentityBadge.jsx) cuenta con un motor determinístico local multi-idioma (`getLocalScopedResponse`) que responde instantáneamente sobre experiencia, educación, proyectos, análisis y contacto sin costo ni exposición de credenciales.
- Opcionalmente, si deseás conectarlo a un proxy backend propio en Cloud Run / Cloud Functions, podés configurar `VITE_CHAT_API_URL` (ver [`.env.example`](.env.example)).

---

## 7. Desarrollo Local, Linting y Despliegue Productivo

### Requisitos Previos
- **Node.js** `>= 20.x` (recomendado `22 LTS`) y **npm** `>= 10.x`.

### Comandos Principales

```bash
# 1. Instalar dependencias
npm install

# 2. Levantar servidor de desarrollo en http://localhost:5173
npm run dev

# 3. Ejecutar linter estático ultrarrápido (Oxlint — debe reportar 0 warnings y 0 errors)
npm run lint

# 4. Generar build optimizado de producción en dist/
npm run build

# 5. Previsualizar build de producción localmente
npm run preview
```

### Despliegue en Google Cloud Run (`Dockerfile` + `nginx.conf`)
El repositorio incluye un [`Dockerfile`](Dockerfile) multi-stage y [`nginx.conf`](nginx.conf) listos para escuchar en el puerto `8080` estándar de Cloud Run:

```bash
gcloud run deploy personal-website \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### Configuración DNS de Dominio y Subdominios
1. **`alejandrocamerlengo.com`** y **`macro.alejandrocamerlengo.com`**: Apuntan al servicio principal de `personal_website` (cuando el visitante ingresa por `macro.alejandrocamerlengo.com`, [`src/App.jsx`](src/App.jsx) abre directamente el estudio `#analisis/macro-argentina`).
2. **`spark.alejandrocamerlengo.com`**: Custom Domain Mapping en Cloud Run hacia `spark-encyclopedia-pro`.
3. **`worldmap.alejandrocamerlengo.com`**: Custom Domain Mapping en Cloud Run hacia `mi-servicio` (World Map Explorer).
4. **`explorer.alejandrocamerlengo.com`**: CNAME / Load Balancer hacia el bucket productivo `global-qol-explorer-frontend`.
5. **`quantlambda.dev`**: Dominio dedicado de la plataforma principal QuantLambda.
