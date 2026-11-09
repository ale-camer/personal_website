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

## 2. Arquitectura de Contenido (Las 4 Áreas del Sitio)

```text
+-----------------------------------------------------------------------------------+
| 0. MARCO GLOBAL (Header • Navegación • Conmutador Dark/Light • Selector Idioma)   |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ 1. PROYECTO ESTRELLA ]   QuantLambda (quantlambda.dev)                         |
|                             Estación cuantitativa, derivados e IA multi-agente    |
|                             en producción (P-01 a P-11 en GCP bajo < $10/mes).    |
|                                                                                   |
|  [ 2. INVESTIGACIONES ]     Análisis Ad-Hoc con Datos y Tesis Propia ("Leer")     |
|                             • Macroeconomía y calidad del empleo en Argentina.    |
|                             • Futuros ensayos con datos (Calidad de vida global,  |
|                               realidad del mercado laboral DS/DE vs. AIE, etc.).  |
|                                                                                   |
|  [ 3. PLAYGROUND ]          Sandboxes & Proyectos de Aprendizaje ("Jugar")        |
|                             • Spark 3.5 Pipeline Architecture & Encyclopedia      |
|                             • Global Quality of Life Explorer                     |
|                             • BTC Analytics Dashboard & World Map Explorer        |
|                                                                                   |
+-----------------------------------------------------------------------------------+
|  [ 4. PESTAÑA APARTE: TRAYECTORIA ]                                               |
|  • Timeline Proporcional de Doble Eje (2011–2026): Trabajo (izq) vs Estudio (der) |
|  • Síntesis de evolución: Finanzas/Quant -> DS -> DE (Tongo) -> AI Engineering    |
+-----------------------------------------------------------------------------------+
```

### Detalle de cada Área

| Área | Rol para el Visitante | Contenido y Alcance |
| :--- | :--- | :--- |
| **1. Proyecto Estrella (`QuantLambda`)** | Explorar y usar una plataforma financiera y agéntica real de punta a punta. | • Presentación destacada de [`quantlambda.dev`](https://quantlambda.dev).<br>• Vista rápida e interactiva de cómo combina finanzas cuantitativas (10 clases de activos, superficies 3D, curvas soberanas), ingeniería de datos/MLOps y un comité multi-agente en LangGraph sobre GCP.<br>• Acceso directo a la app en vivo. |
| **2. Investigaciones (`Leer`)** | Aprender de análisis económicos, laborales y cuantitativos hechos a medida con opinión propia. | • **Artículo Fundacional:** *Macroeconomía y Degradación del Empleo en Argentina* (modernizado de notebook estático a ensayo interactivo con sus 4 ejes: *Políticas/Inflación/Gasto desde 1961*, *Empleo Privado vs. Crecimiento*, *Composición por Modalidad: el espejismo del Monotributo Social +160% vs. estancamiento privado/autónomo* y *Salario Real*).<br>• **Estructura extensible** para publicar nuevos análisis ad-hoc sobre temas en curso (mercado laboral tech/IA, comparativas de calidad de vida y poder adquisitivo, etc.). |
| **3. Playground (`Jugar`)** | Experimentar con herramientas educativas y exploradores construidos para aprender distintas tecnologías. | Hub curado y *user-friendly* de desarrollos de práctica (*Learning by Building*):<br>• **Spark Encyclopedia Pro:** Grafo interactivo de decisiones y enciclopedia de Apache Spark 3.5.<br>• **Global Quality of Life Explorer:** Explorador comparativo de calidad de vida.<br>• **BTC Dashboard & World Map Tool:** Visualizadores temáticos interactivos. |
| **4. Trayectoria (`Sobre Mí / CV`)** | Conocer quién está detrás del laboratorio sin invadir la experiencia de lectura/juego. | • Ubicado en su propia vista/pestaña dedicada.<br>• **Timeline Proporcional de Doble Eje (`2011–2026`)** inspirado en `_legacy/reference_timeline_cv.jpg`: **Experiencia Laboral** a la izquierda (*Best Day $\rightarrow$ Balanz $\rightarrow$ Lumen $\rightarrow$ AB InBev $\rightarrow$ Siemens Advanta $\rightarrow$ **Tongo***) y **Educación** a la derecha (*UNLZ $\rightarrow$ UBA Finanzas $\rightarrow$ UBA Data Science $\rightarrow$ UCEMA Financial Math*), con paneles desplegables al hacer click.<br>• Breve narrativa de transición hacia **AI Engineering E2E**. |

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

## 4. Orden de Avance Actual (De lo Más Fácil a lo Más Difícil) y Pendientes Acordados

### 4.1 Orden de Ejecución Definido
1. **`1. Recorrido` (`#recorrido`)**:
   - Limpieza de etiquetas (`RUNNING`, `SUCCESS`, `ARTIFACT`, `pipeline: ...` y tags) y etiquetas en 2 líneas (Rol/Título arriba + Empresa/Universidad abajo) — **hecho**.
   - **Pendiente anotado:** Agregar el contenido definitivo del CV en el que Alejandro está trabajando actualmente cuando esté listo.
2. **`2. Análisis` (`#analisis`)**:
   - Rehacer los estudios con los datos pertinentes actualizados (fuentes propias) y evaluar agregar **Forecast** a las series.
3. **`3. Proyectos` (`#proyectos`)**:
   - Darles una nueva estética (lavada de cara Sci-Fi/Tech) y **rehacer todo el código** de las 4 aplicaciones interactivas (*Spark 3.5 Encyclopedia*, *Crypto Analytics*, *World Map Explorer* y *World Bank Explorer*) para que corran integradas en la web.
4. **`4. Home y Cierre General`**:
   - Frase central de la portada, pase de diseño general unificado, selector de idiomas y traducciones.

### 4.2 Tabla de Pendientes Acordados

| Pendiente | Decisión / Detalle | Cuándo |
| :--- | :--- | :--- |
| **Contenido definitivo del CV en `Recorrido` (`#recorrido`)** | Incorporar el texto definitivo de responsabilidades y logros del CV en el que Alejandro está trabajando actualmente. | Cuando esté cerrada la nueva versión del CV. |
| **Pulir perfil de GitHub (`https://github.com/ale-camer/`)** | El ícono de GitHub en el Home ya apunta a `https://github.com/ale-camer/` (y el de Gmail a `mailto:alejandrocamerlengo@gmail.com`). Queda anotado pulir el perfil público de GitHub (README de perfil, repos fijados, descripciones). | Tarea de perfil externo. |
| **Rehacer `Análisis` (`#analisis`) con datos actualizados + Forecast** | Actualizar las series con fuentes propias, rehacer el estudio de Macroeconomía y Empleo en Argentina (y demás análisis) e incorporar proyecciones / **Forecast**. | Paso 2 del orden actual. |
| **Rehacer código y estética de las 4 apps de `Proyectos` (`#proyectos`)** | No mostrar los repositorios de GitHub sino **las aplicaciones interactivas en sí**, rehaciendo su código y dándoles una nueva estética moderna/Sci-Fi coherente con el sitio. | Paso 3 del orden actual. |
| **Unificación de patrones de diseño (Design System final — Estética Sci-Fi / Tech Engineering)** | Definir y estandarizar cómo deben verse todos los elementos que cumplen la misma función en las 4 secciones (jerarquía de títulos/subtítulos, `cards`, badges, bullets, botones, espaciados y bordes) explorando variantes **Sci-Fi / Futuristas inspiradas en herramientas reales de ingeniería** (*DAG Pipeline*, *Git Branch Graph*, *PCB Circuit*, *Telemetry HUD*, *Terminal Trace*). | Paso 4 (Al final, con las secciones listas). |
| **Propuesta central de la landing (`Home`)** | Una sola línea corta en el centro de la pantalla (`.hero-tagline-slot` en `src/App.jsx`). Se propondrán 3–4 frases para elegir. | Paso 4 (`Home`). |
| **Selector de idioma masivo (estilo `quantlambda.dev`) + Traducciones** | Incorporar la mayor cantidad de idiomas posibles (como el catálogo de **56 idiomas con banderas SVG y ventana modal centrada con buscador** de `quantlambda.dev` en `market-intelligence-dashboard/src/data/i18n/languages.js`), realizando las traducciones recién cuando todo el texto definitivo esté cerrado. | Al final de todo el proyecto. |
| **Mejoras técnicas menores y seguridad** | Canvas nítido en pantallas retina (`devicePixelRatio`), respeto de `prefers-reduced-motion`, mover utilidades de `App.jsx` a `components/`, y asegurar `VITE_GEMINI_API_KEY` detrás de un proxy antes de publicar. | Pulido previo al despliegue. |
