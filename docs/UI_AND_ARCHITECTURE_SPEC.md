# Especificación de Diseño, Arquitectura e Interfaz (`UI_AND_ARCHITECTURE_SPEC.md`)

Documento técnico y visual que define el stack, el sistema de temas duales (**Dark / Light** con impronta propia) y las especificaciones de cada uno de los módulos del plan de 5 etapas.

---

## 1. Arquitectura Frontend y Decisión sobre Lenguajes de Bajo Nivel (ADR-001)

### 1.1 Stack Elegido para la Web Personal: `React + Vite (SWC)` Puro
- **React + Vite (con compilador SWC y linter Oxlint basados en Rust)** para lograr carga instantánea, transiciones fluidas entre vistas (*Inicio*, *Investigaciones*, *Playground*, *Trayectoria*) y componentes interactivos ricos (gráficos dinámicos en las investigaciones y línea de tiempo proporcional en Trayectoria).
- **Cero Backend Acoplado:** Al tratarse de contenido editorial/analítico, visualizaciones de series macroeconómicas (~60 a 200 puntos por serie) y un timeline geométrico, todo corre en `< 1 ms` directamente en el motor JS del navegador.

### 1.2 Evaluación de Lenguajes de Sistemas (`Rust`, `Go`, `C`, `C++`): ¿Dónde sí y dónde no?
Se evaluó la conveniencia de incorporar lenguajes compilados de alto rendimiento (`Rust`, `Go`, `C`, `C++`) para maximizar la eficiencia:

1. **Por qué se descartan en la estructura de `personal_website`:**
   - Servir vistas, artículos e indicadores macroeconómicos mediante un backend en Go/Rust o compilar la UI a WebAssembly no aporta ganancia perceptible frente a archivos estáticos precompilados, y en cambio introduce complejidad innecesaria de compilación y despliegue (*sobre-ingeniería*).
2. **Por qué `Rust` (y no `C/C++` ni `Go`) es la apuesta estratégica correcta para el perfil DE / AIE:**
   - **C / C++:** Alta fricción de toolchain para web (`Emscripten`) y menor alineación directa con el stack moderno de ingeniería de datos/IA.
   - **Go:** Excelente para microservicios de red y concurrencia en backend, pero genera binarios pesados en WebAssembly (al incluir su *garbage collector*) y no está orientado a cómputo numérico matricial.
   - **Rust:** Sin *garbage collector*, genera binarios `.wasm` ultralivianos para el navegador y es hoy el estándar industrial sobre el que se construye la infraestructura moderna de Data Engineering e IA (*Polars, Apache Arrow/DataFusion, Qdrant, LanceDB, Ruff, uv, tokenizers y extensiones Python vía PyO3*).
3. **Dónde SÍ se recomienda aplicar `Rust` (En `quantlambda.dev` post-MVP o en motores de cálculo intensivo):**
   - Dado que `quantlambda.dev` se desarrolla por separado como la estación cuantitativa y agéntica principal, **es allí donde realmente tiene sentido técnico evaluar Rust** (sin bloquear el cierre de su MVP actual):
     - **Caso A — Frontend Quant (`Rust -> WebAssembly` en el navegador, costo Cloud \$0):** Para motores numéricos pesados en tiempo real que superen a JS (ej. simulaciones de Monte Carlo de `100.000+` trayectorias para *VaR / Expected Shortfall*, árboles binomiales densos o calibración de superficies de volatilidad en vivo a 60 FPS usando la CPU del cliente).
     - **Caso B — Backend / Pipelines (`Polars` / `Rust + PyO3` en Cloud Run Jobs `P-01..P-06`):** Para optimizar consumo de RAM (`512Mi`–`1Gi`) y tiempos de ejecución en procesos ETL y de detección de anomalías bajo la restricción FinOps (`< $10/mes`).

### 1.3 Internacionalización (`i18n`) e Identidad Visual Dual (Dark & Light)
- **Internacionalización (`i18n`) Limpia y Escalable:**
  - Diccionarios modulares por sección (`common`, `trajectory`, `research`, `playground`, `flagship`).
  - Base inicial cuidada al detalle en **Español (`es`)** e **Inglés (`en`)**, lista para incorporar más idiomas (como Alemán `de`, etc.) y el selector modal con banderas utilizado en `quantlambda.dev`.
- **Identidad Visual Dual (Dark & Light con Personalidad):**
  - **Tipografía:**
    - `--font-serif` (*Playfair Display* / *Lora*): Títulos de investigaciones, encabezados editoriales y citas de tesis.
    - `--font-sans` (*Plus Jakarta Sans* / *Inter*): Navegación, controles interactivos y cuerpo de lectura con interlineado descansado (`1.75`–`1.80`).
    - `--font-mono` (*JetBrains Mono*): Años del eje temporal (`2011`–`2026`), series de datos, etiquetas de stack y métricas.
  - **Modo Oscuro (*Obsidian Quant*):** Superficies profundas (`#07090e` / `#0d1321`), bordes sutiles de `1px` y acentos de alto contraste inspirados en `quantlambda.dev`.
  - **Modo Claro (*Swiss Editorial Paper*):** Superficie cálida tipo papel editorial (`#f6f5f2` / `#efede8`), libre de encandilamiento blanco puro, ideal para la lectura prolongada de investigaciones y para lucir los bloques cromáticos del Timeline.

---

## 2. Reglas de UX, Proceso de Trabajo y Distribución Espacial

### 2.1 Regla de Proceso de Trabajo (Elemento por Elemento)
- **Flujo obligatorio en 3 pasos:** **1° Proponer ideas conceptuales $\rightarrow$ 2° El usuario decide $\rightarrow$ 3° Recién ahí se ejecuta en código/documentos**.
- **Construcción de a UN elemento por vez:** En lugar de poblar toda la pantalla con cajas invasivas simultáneamente, la landing se construye con el centro despejado cerrando un único elemento por iteración:
  1. **Elemento 1:** El Lienzo / Fondo (Oscuro y Claro).
  2. **Elemento 2:** Identidad Discreta arriba a la izquierda (Foto + Nombre).
  3. **Elemento 3:** Marco Periférico Inferior (Riel vertical de redes + Idioma/Tema).
  4. **Elemento 4:** Barra de Navegación hacia los 4 destinos.
  5. **Elemento 5:** Animación Inicial (`AC`) y Detalle Central no invasivo.

### 2.2 Reglas Espaciales (Definidas por Iteración sobre Referencias)
A partir del análisis crítico de referencias reales (*Brittany Chiang v4*, *Jhey Tompkins*, *Lee Robinson*, *Shu Ding*, *Cassidoo*, *Anthony Fu*, etc.), se establecieron las siguientes **reglas inquebrantables de diseño** para la landing page:

1. **El Deseo Exploratorio hay que Ganárselo (Cero "Diario de Texto" y Cero Abrumar):**
   - Sitios puramente textuales o minimalistas extremos fallan porque exigen que un desconocido o reclutador invierta media hora leyendo para descubrir si hay valor (*"si tengo ganas de leer me compro el diario"*).
   - Sitios recargados de paneles y texto abrumador también expulsan al visitante.
   - La primera vista debe caber en **una sola pantalla limpia (sin scroll obligatorio)** y despertar curiosidad inmediata a través de **navegación clara y ganchos visuales concretos**, no bloques de texto ni formularios.
2. **Foto + Nombre Unificados en un Lugar que No Moleste (Arriba a la Izquierda):**
   - La foto de perfil y el nombre (`Alejandro Camerlengo`) no deben ocupar el centro de la pantalla como en la versión legacy.
   - Se unifican en una **insignia de identidad compacta (Avatar circular + Nombre)** en la esquina superior izquierda del Header. Así el visitante identifica al autor al instante, liberando el centro de la pantalla para el contenido y la navegación.
3. **Animación Inicial de Entrada con Iniciales (`AC`):**
   - Inspirado en la apertura de *Brittany Chiang v4*: al entrar a la web se ejecuta una animación corta y precisa que juega geométricamente con las iniciales **`AC`** antes de revelar la pantalla principal.
4. **Protagonismo para la Navegación, No para "Herramientas de Exploración" (Buscadores/Filtros):**
   - Barras de búsqueda grandes (`Search projects...`) y nubes de tags/filtros no deben ocupar el centro de la aplicación.
   - Lo que sí ocupa el centro y la estructura principal son los **accesos de navegación directa** hacia los pilares definidos de la app:
     1. **Proyecto Estrella (`QuantLambda`)**
     2. **Investigaciones (`Leer`)**
     3. **Playground (`Jugar`)**
     4. **Trayectoria (`Timeline 2011–2026`)**
5. **Footer Vertical Lateral + Selector de Idioma en el Pie:**
   - El selector de idioma sale del Header superior y pasa al **Footer**, manteniendo la cabecera despejada.
   - Los enlaces de contacto (`GitHub`, `LinkedIn`, `Email`) se disponen en sentido **vertical en un riel lateral inferior** (inspirado en el riel vertical de *Brittany Chiang*), acompañado del selector de idioma/tema en la base.

### 2.1 Etapa 2: Trayectoria — Timeline Proporcional de Doble Eje (`2011–2026`)
Basado en la referencia visual (`_legacy/reference_timeline_cv.jpg`), vive en su propia pestaña para mantener la web libre de formato "currículum corporativo":

```text
          WORK EXPERIENCE                                  EDUCATION
   (Altura proporcional a duración)                 (Altura proporcional a duración)

  +--------------------------------+     2026
  | Data Engineer                  |       |
  | Tongo                          |       |
  +--------------------------------+       |
  | Data Engineer (Global)         |     2025
  | Siemens Advanta                |       |
  +--------------------------------+       |
  |                                |     2024
  | Data Scientist (Global)        |       |
  | AB InBev                       |       |
  +--------------------------------+     2023     +--------------------------------+
  |                                |       |      | Financial Mathematics          |
  | Data Scientist (LATAM)         |       |      | University of CEMA (UCEMA)     |
  | Lumen Technologies             |     2022     +--------------------------------+
  |                                |       |      |                                |
  +--------------------------------+       |      | Data Science (MSc)             |
  | Quantitative Analyst (Buy-Side)|     2021     | Universidad de Buenos Aires    |
  | Balanz Capital                 |       |      |                                |
  +--------------------------------+     2020     +--------------------------------+
                                           |      |                                |
                                         2019     | Corporate Finance (MSc)        |
                                           |      | Universidad de Buenos Aires    |
  +--------------------------------+     2018     +--------------------------------+
  |                                |       |      |                                |
  | Semi Senior Treasury Analyst   |     2017     |                                |
  | (South America)                |       |      |                                |
  | Best Day Travel Group          |     2016     | Business Administration and    |
  |                                |       |      | Management (BSc)               |
  +--------------------------------+     2015     | Universidad Nacional de        |
                                           |      | Lomas de Zamora (UNLZ)         |
                                         2014     |                                |
                                           |      |                                |
                                         2013     |                                |
                                           |      |                                |
                                         2012     |                                |
                                           |      +--------------------------------+
                                         2011
```

- **Geometría:** Posicionamiento vertical calculado matemáticamente a partir de `(año_inicio, mes_inicio)` y `(año_fin, mes_fin)` sobre el eje continuo `2011–2026`.
- **Interacción:** Vista limpia de bloques por defecto; al hacer click sobre un bloque laboral o académico, se abre una ficha detallada con responsabilidades, problemas modelados, alcance regional y tecnologías.
- **Narrativa Complementaria:** Encabezado conciso explicando el hilo conductor (*Finanzas/Matemática $\rightarrow$ Data Science $\rightarrow$ Data Engineering en Tongo $\rightarrow$ AI Engineering E2E*).

---

### 2.2 Etapa 3: Investigaciones — Artículos Interactivos con Datos Propios
Reemplaza las antiguas páginas generadas con `nbconvert` por un sistema de **Ensayos Interactivos**:
- **Sin ruido de código crudo:** El lector no ve celdas `import pandas as pd` ni tablas HTML sin estilo, sino una narrativa clara acompañada de gráficos interactivos (con *tooltips*, filtros de series y resaltado de períodos históricos).
- **Primer Caso (Macroeconomía y Empleo en Argentina):**
  1. *Crecimiento del PBI, Inflación y Gasto Público / PBI (1961–Presente)*: visualización de regímenes macroeconómicos.
  2. *Estancamiento del Empleo Asalariado Privado (2009–Presente)*: impacto de la falta de crecimiento en el sector que financia a la economía.
  3. *Degradación por Modalidad Laboral (2012–Presente)*: comparativa interactiva entre crecimiento nulo de *Privados/Autónomos* frente a la expansión de *Empleo Público (+30%)* y *Monotributo Social (+160%)*.
  4. *Evolución del Salario Real y Poder de Compra (2001–Presente)*.

---

### 2.3 Etapa 4: Playground — Proyectos de Aprendizaje (*Learning by Building*)
Diseño de tarjetas y contenedores pensados para la exploración sin fricción:
- Cada proyecto indica: **Qué podés hacer/jugar**, **Qué busqué aprender al construirlo** y **Stack utilizado**.
- Proyectos incluidos:
  1. **Spark Pipeline Architecture & Encyclopedia** (`spark-encyclopedia-pro`)
  2. **Global Quality of Life Explorer** (`global-qol-explorer`)
  3. **BTC Analytics Dashboard** (`btc-dashboard`)
  4. **World Map Visualization Tool** (`geospacial_projects`)

---

### 2.4 Etapa 5: Proyecto Estrella — `QuantLambda` (`quantlambda.dev`)
Módulo de alto impacto visual en la portada que conecta la web personal con la plataforma principal:
- Muestra el alcance funcional (213 activos en 10 clases, superficies de volatilidad 3D, curvas soberanas de 42 países, RAG financiero y Comité Multi-Agente) y el resumen de ingeniería (`P-01` a `P-11` en GCP con Terraform y FinOps `< $10/mes`).
- Botones de acción directa: **Abrir Plataforma en Vivo (`quantlambda.dev`)** y **Explorar Arquitectura**.
