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
