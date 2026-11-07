# Alejandro Camerlengo — Personal Website, Research & Playground

Repositorio de [alejandrocamerlengo.com](https://www.alejandrocamerlengo.com/): un laboratorio y observatorio personal diseñado para **leer investigaciones ad-hoc con datos reales** y **explorar herramientas/plataformas interactivas**, acompañado de un recorrido visual por la evolución profesional desde **Finanzas & Modelado Cuantitativo $\rightarrow$ Data Science $\rightarrow$ Data Engineering (Tongo) $\rightarrow$ AI Engineering End-to-End**.

---

## 📚 Documentación Rectora

Toda la definición estratégica, de producto y de arquitectura se encuentra en [`docs/`](docs/):

1. **[`docs/MASTER_BLUEPRINT.md`](docs/MASTER_BLUEPRINT.md) — Plan Maestro de Visión, Contenido y Hoja de Ruta:**
   - Filosofía centrada en aportar valor al lector (*Leer, Jugar y Explorar*) en lugar de un folleto de CV.
   - Las **4 Áreas del Sitio**:
     1. **Proyecto Estrella:** [QuantLambda (`quantlambda.dev`)](https://quantlambda.dev)
     2. **Investigaciones Ad-Hoc (`Leer`):** Análisis propios con datos reales (comenzando por *Macroeconomía y Degradación del Empleo en Argentina*).
     3. **Playground (`Jugar`):** Proyectos de aprendizaje interactivos (*Spark Encyclopedia*, *Global QoL Explorer*, *BTC Dashboard*, *World Map*).
     4. **Trayectoria (`Sobre Mí`):** Pestaña dedicada con el **Timeline Proporcional de Doble Eje (`2011–2026`)**.
   - **Hoja de Ruta en 5 Etapas** (ordenadas de mayor a menor carga de desarrollo).
2. **[`docs/UI_AND_ARCHITECTURE_SPEC.md`](docs/UI_AND_ARCHITECTURE_SPEC.md) — Especificación de Diseño y Arquitectura (`ADR-001`):**
   - Stack moderno en **React + Vite (SWC)**, soporte **Dual Theme (Dark Technical / Light Editorial)** e internacionalización (`i18n`) escalable.
   - Evaluación técnica de lenguajes de bajo nivel (`Rust`, `Go`, `C`, `C++`): por qué se descartan para la web personal y dónde sí aplica **Rust (`WASM` / `Polars` / `PyO3`)** como evolución en `quantlambda.dev`.
   - Especificación detallada de cada módulo de las 5 etapas.

---

## 🗄️ Versión Legacy (`_legacy/`)

La versión anterior en Flask + Dash se conserva localmente en `_legacy/` (excluida de Git mediante [`.gitignore`](.gitignore)) como referencia de textos y datos crudos de las investigaciones previas.

```bash
cd _legacy
source .venv/bin/activate
FLASK_ENV=development python main.py
# Disponible en http://127.0.0.1:5000
```
