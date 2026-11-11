# Arquitectura del Repositorio Dedicado (`argentina-macro-pipeline`) y Prompt Inicial Maestro

Carpeta creada lista para abrir como workspace independiente:
`/home/alejandrocamerlengo/Projects/argentina-macro-pipeline`

Dentro de `/home/alejandrocamerlengo/Projects/argentina-macro-pipeline/bootstrap/` ya quedaron copiados:
- `bootstrap/raw_data/`: Los **9 archivos oficiales crudos** descargados hoy (`wb_inflacion.zip`, `wb_pbi_growth.zip`, `gasto_publico.xls`, `sipa_trabajo_registrado.xlsx`, `indec_indice_salarios.csv`, `indec_variaciones_salarios.xls`, `indec_salarios_hist_2012.xls`, `indec_emae.xls`, `indec_ipc.csv`).
- `bootstrap/Argentina_Macroeconomia_y_empleo.ipynb`: Tu notebook original.
- `bootstrap/reference_visuals_pipeline.py`: El script de referencia determinístico que genera las 5 gráficas mejoradas sin superposiciones.

---

## 1. Estructura Propuesta para el Repositorio Dedicado

```text
argentina-macro-pipeline/
├── pyproject.toml                       # Dependencias (pandas, numpy, matplotlib, statsmodels, ruptures, pydantic, httpx, beautifulsoup4, google-genai)
├── README.md                            # Documentación técnica y arquitectura del pipeline
├── config/
│   ├── sources.yaml                     # URLs fijas, páginas madre de auto-discovery y selectores/offsets por fuente
│   ├── golden_anchors.json              # Valores históricos inmutables ("Golden Tests") para validar lecturas
│   └── regimes.yaml                     # Definición vigente de regímenes macroeconómicos y umbrales
├── data/
│   ├── last_known_good/                 # Snapshots limpios en Parquet/CSV (fallback si cae un servidor .gob.ar)
│   └── raw_cache/                       # Últimos archivos crudos descargados con su hash SHA-256
├── src/
│   ├── __init__.py
│   ├── main.py                          # Orquestador principal del pipeline mensual
│   ├── collectors/                      # 100% Determinístico: descarga + auto-discovery por regex en páginas madre
│   │   ├── world_bank.py
│   │   ├── ministerio_economia.py
│   │   ├── sipa_trabajo.py
│   │   └── indec.py
│   ├── validators/                      # 100% Determinístico: Pydantic/Pandera schemas + Golden Anchor Checks
│   │   └── schema_and_golden.py
│   ├── transformers/                    # 100% Determinístico: empalmes geométricos, desestacionalización, índices base 100
│   │   └── macro_employment.py
│   ├── models/                          # 100% Determinístico: Detección estadística de quiebres (PELT/CUSUM) + Forecasts (SARIMAX/VAR)
│   │   ├── structural_breaks.py
│   │   └── forecaster.py
│   ├── visualizers/                     # 100% Determinístico: Generación de las 5 figuras con zonas reservadas anti-colisión
│   │   └── charts.py
│   ├── agents/                          # Capa Probabilística estrictamente encapsulada (SOLO se invoca ante excepciones)
│   │   ├── ingestion_healer_agent.py    # Agente 1: Diagnostica cambios en DOM/Excel y propone nuevo offset validado contra Golden Tests
│   │   └── visual_and_regime_agent.py   # Agente 2: QA Multimodal (0 texto pisado) + Redacción de PR si structural_breaks detecta nuevo régimen
│   └── monitoring/                      # Reporte estructurado y alertas Always-On (Telegram / Email / GitHub Issue)
│       └── notifier.py
├── outputs/
│   ├── macro_argentina_latest.json      # Contrato JSON liviano (~35 KB) listo para ser consumido por personal_website
│   ├── run_report_latest.json           # Telemetría de la última corrida (estado por fuente, filas nuevas, QA status)
│   └── figures/                         # Las 5 gráficas en PNG/SVG de alta resolución
├── tests/
│   ├── test_golden_anchors.py           # Verifica que los parsers reproduzcan al centésimo los hitos históricos
│   └── test_transformers.py             # Tests unitarios de composición geométrica y empalmes
└── .github/
    └── workflows/
        └── monthly_update.yml           # Cron mensual (día 25) + ejecución manual (workflow_dispatch)
```

---

## 2. Prompt Inicial Maestro (Copiá y pegá esto al abrir `argentina-macro-pipeline`)

```markdown
# ROL Y OBJETIVO DEL PROYECTO

Estamos construyendo `argentina-macro-pipeline`, un motor de ingeniería de datos, análisis macroeconómico cuantitativo y generación de visualizaciones de grado de publicación que alimenta la sección `#analisis` de mi web personal (`personal_website`).

El principio rector de arquitectura es:
**"Núcleo 100% determinístico; uso de LLMs/Agentes estrictamente limitado y encapsulado a los dos puntos débiles del flujo (auto-reparación de ingesta ante cambios de formato oficial y QA visual / propuesta de nuevos regímenes ante quiebres estructurales), con monitoreo y alertas obligatorias en cada ejecución."**

En la carpeta `./bootstrap/` de este workspace ya tenés:
1. `./bootstrap/raw_data/`: Los archivos oficiales crudos descargados de las 7 fuentes.
2. `./bootstrap/Argentina_Macroeconomia_y_empleo.ipynb`: El notebook original donde nació la tesis.
3. `./bootstrap/reference_visuals_pipeline.py`: El script de referencia funcionando que carga las 7 fuentes desde `./bootstrap/raw_data/`, aplica las transformaciones matemáticas corregidas y genera las 5 gráficas mejoradas sin superposiciones. **Leé este archivo antes de empezar porque contiene todos los offsets exactos de filas/columnas y el diseño visual aprobado.**

---

# 1. ESPECIFICACIÓN DE LAS 7 FUENTES OFICIALES Y SUS "GOLDEN TESTS"

El pipeline debe ingerir estas 7 fuentes oficiales sin intervención manual:

1. **Inflación Anual (Deflactor del PBI, 1961–Presente):**
   - URL fija ZIP/CSV: `https://api.worldbank.org/v2/en/indicator/NY.GDP.DEFL.KD.ZG?downloadformat=csv` (o API JSON equivalente para `ARG`).
   - Golden Test: `1980 = 20.310698` (en 1961), `2017 = 26.006379`, `2020 = 40.083088`.
2. **Crecimiento del PBI Real Anual (1961–Presente):**
   - URL fija ZIP/CSV: `https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=csv` (`ARG`).
   - Golden Test: `1961 = 5.427843`, `2011 = 6.003952`, `2017 = 2.818503`.
3. **Gasto Público Consolidado en % del PBI (1980–Presente):**
   - Página madre para auto-discovery: `https://www.argentina.gob.ar/economia/politicaeconomica/macroeconomica/gastopublicoconsolidado`
   - Última URL directa conocida: `https://www.argentina.gob.ar/sites/default/files/gasto_publico_consolidado_desde_1980_2.xls` (Hoja `% del PIB`, fila de años en índice 2 limpiando `*`, fila `1.0 GASTO PÚBLICO TOTAL` en índice 4).
   - Golden Test: `1980 = 29.037146`, `2011 = 40.006699`.
4. **Trabajo Registrado SIPA (Serie Mensual 2009–Presente y Modalidades 2012–Presente):**
   - Página madre para auto-discovery: `https://www.argentina.gob.ar/trabajo/estadisticas` (buscar el link al `.xlsx` de Situación y Evolución del Trabajo Registrado, cuyo nombre sigue el patrón `trabajoregistrado_AAMM_estadisticas.xlsx`).
   - Última URL directa conocida: `https://www.argentina.gob.ar/sites/default/files/trabajoregistrado_2607_estadisticas.xlsx`.
   - **Serie 4a (Modalidades desde 01/2012):** Hoja `T.2.1` (columnas `Empleo privado`, `Empleo público`, `Empleo en casas particulares`, `Autónomos`, `Monotributo`, `Monotributo Social`, `Total`).
     - Golden Test (`2012-01-01`): `Empleo privado = 6106.0`, `Empleo público = 2543.7`, `Total = 10931.3`; proporciones en `2012-01`: `55.86%`, `23.27%`, `12.03%`, `3.75%`, `3.56%`, `1.53%`.
   - **Serie 4b (Empleo Privado Provincial desde 01/2009):** Hoja `A.5.1` (suma horizontal de las 24 provincias en miles).
     - Golden Test (`2009-01-01`): `total = 5659.961`, `2009-02-01 = 5647.381`.
5. **Índice de Salarios INDEC — Serie Vigente (10/2015–Presente):**
   - Página madre: `https://www.indec.gob.ar/Nivel4/Tema/4/31/61`
   - URL directa CSV fija: `https://www.indec.gob.ar/ftp/cuadros/sociedad/indice_salarios.csv` (separador `;`, decimal `,`, columnas `IS_sector_privado_registrado` e `IS_sector_publico`).
6. **Índice de Salarios INDEC — Serie Histórica Empalmada (10/2001–10/2015):**
   - URL directa XLS fija: `https://www.indec.gob.ar/ftp/cuadros/sociedad/serie_is_2012.xls` (Hoja `Serie histórica IS`, desde fila 6, columnas `Unnamed: 1` privado y `Unnamed: 3` público).
   - Golden Test (`2001-10-01`): `sectorPrivado = 14.22`, `sectorPublico = 27.99`.
7. **EMAE — Estimador Mensual de Actividad Económica Base 2004=100 (01/2004–Presente):**
   - Página madre: `https://www.indec.gob.ar/Nivel4/Tema/3/9/48`
   - URL directa XLS fija: `https://www.indec.gob.ar/ftp/cuadros/economia/sh_emae_mensual_base2004.xls` (desde fila 4: col 2 = `Serie Original`, col 4 = `Serie Desestacionalizada`, col 6 = `Tendencia-Ciclo`).
   - Golden Test (`2004-01-01`): `Original = 92.6275`, `Desestacionalizada = 98.5292`, `Tendencia-Ciclo = 96.0499`.

---

# 2. ARQUITECTURA DEL FLUJO Y FRONTERA DETERMINÍSTICA VS. AGÉNTICA

Implementá la estructura modular del repositorio respetando estrictamente estas etapas:

## Etapa 1: Ingesta Determinística + Fallback + Agente 1 (`SelfHealingIngestionAgent`)
- Cada colector intenta primero descargar la fuente por código determinístico (API directa o scraper regex de la página madre).
- Inmediatamente corre el validador determinístico (`schema_and_golden.py`):
  1. Verifica tipos, ausencia de `NaN` en períodos cerrados y continuidad temporal (`MS` o `YS`).
  2. Verifica que los **Golden Tests** históricos listados arriba coincidan al centésimo.
- **¿Cuándo y cómo interviene el Agente 1?**
  - **ÚNICAMENTE** si falla la descarga (404 / cambio de URL en la página madre que el regex no encontró) o si falla la validación de esquema/Golden Test (ej. el organismo agregó filas de título o movió una columna en el Excel).
  - El Agente 1 inspecciona el HTML de la página madre o las primeras 25 filas/columnas del Excel crudo, deduce el nuevo link o los nuevos índices de fila/columna (`row_offset`, `col_indices`) y vuelve a correr el **Golden Test determinístico**.
  - **Regla de oro:** Si la configuración propuesta por el Agente 1 pasa el Golden Test determinístico al 100%, se acepta, se registra el evento `HEALED_BY_AGENT` y se actualiza el snapshot `data/last_known_good/`. Si no pasa el Golden Test, se aborta el parche del agente, se usa el snapshot `data/last_known_good/` para no romper producción y se dispara alerta crítica.

## Etapa 2: Transformaciones Matemáticas y Modelos Estadísticos (100% Determinístico)
Ningún LLM interviene acá. Replicar exactamente la matemática de `./bootstrap/reference_visuals_pipeline.py`:
1. **Visual 1 (`1980–Presente`):** Índice Geométrico Real del PBI (`Base 1980 = 100`, $I_t = I_{t-1}(1 + g_t/100)$), tendencias exponenciales (`CAGR`) por régimen macroeconómico, Gasto Público / PBI (%) e Inflación anual en escala logarítmica.
2. **Visual 2 (`01/2009–Presente`):** Empleo Privado Registrado vs. EMAE Desestacionalizado y Tendencia-Ciclo re-expresados en `Base Ene-2009 = 100` + regresión de elasticidad empleo-producto ($\beta$).
3. **Visual 3 (`01/2012–Presente`):** Crecimiento relativo acumulado geométrico exacto ($\frac{X_t}{X_0} - 1$) por modalidad SIPA + proyección demográfica intercensal y brecha demográfica vs. empleo privado.
4. **Visual 4 (`01/2012` vs `03/2022` vs `Último mes`):** Participación porcentual sobre el total registrado y desplazamiento neto en puntos porcentuales (`pp`).
5. **Visual 5 (`2005–Presente`):** Empalme geométrico deduplicado en `2015-10` del Índice de Salarios privado registrado deflactado contra inflación anual $\rightarrow$ Índice de Salario Real y PBI Real en `Base 2012 = 100` + variaciones interanuales (`% YoY`).
6. **Detector Estadístico de Quiebres de Régimen (`structural_breaks.py`):**
   - Evaluar de forma determinística (usando `ruptures` / `PELT` o reglas cuantitativas explícitas en `config/regimes.yaml`, como cambio de signo sostenido en la pendiente de 24 meses o cruce de umbrales estructurales como `Gasto/PBI < 40%`) si los nuevos datos rompen la tendencia del último régimen declarado.

## Etapa 3: Generación de Gráficas + Agente 2 (`VisualQAAndRegimeAgent`)
- El módulo `visualizers/charts.py` genera las 5 figuras con el diseño exacto de `./bootstrap/reference_visuals_pipeline.py` (leyendas fuera del área de datos con `bbox_to_anchor` y tarjetas de régimen en bandas superiores reservadas dinámicamente para evitar colisiones).
- **¿Cuándo y cómo interviene el Agente 2?**
  1. **Inspector de QA Visual Multimodal:** Recibe las 5 imágenes PNG generadas y verifica mediante visión que no exista ningún texto cortado, leyenda superpuesta a barras/líneas ni ejes ilegibles. Devuelve un JSON estructurado (`{"visual_qa_passed": bool, "issues": [...]}`).
  2. **Asistente de Nuevo Régimen (solo si `structural_breaks.py` levantó `REGIME_SHIFT_DETECTED = True`):** Si el test estadístico determinístico detectó un cambio de tendencia/régimen, el Agente 2 redacta una propuesta de actualización para `config/regimes.yaml` y genera el cuerpo de un **Pull Request** con el antes/después para revisión humana (nunca sobreescribe la tesis macroeconómica en `main` sin aprobación).

## Etapa 4: Contrato de Salida + Monitoreo y Alertas "Always-On" (`notifier.py`)
- Exportar `outputs/macro_argentina_latest.json` con metadatos de corrida, fecha de corte de cada una de las 7 fuentes, series listas para graficar en la web y métricas resumen.
- **Monitoreo obligatorio en cada ejecución (éxito o fallo):**
  - Generar `outputs/run_report_latest.json` y enviar notificación (vía Telegram Bot API / Email SMTP / GitHub Issue) detallando:
    - Estado general: `OK_DETERMINISTIC` | `HEALED_BY_AGENT` | `REGIME_SHIFT_PR_OPENED` | `FALLBACK_USED` | `FAILED`.
    - Tabla de las 7 fuentes: período anterior vs. período nuevo descargado, cantidad de observaciones agregadas y resultado del Golden Test.
    - Resultado del QA Visual (`5/5 PASS`).

---

# PLAN DE TRABAJO PASO A PASO

Por favor ejecutá la construcción en este orden:
1. Inicializá el proyecto Python (`pyproject.toml` / entorno virtual) e inspeccioná `./bootstrap/reference_visuals_pipeline.py` y `./bootstrap/raw_data/`.
2. Construí `config/golden_anchors.json`, `config/sources.yaml` y `config/regimes.yaml`.
3. Implementá los colectores determinísticos (`src/collectors/`), el validador con Golden Tests (`src/validators/`) y poblá `data/last_known_good/` usando los datos verificados.
4. Implementá `src/transformers/`, `src/models/structural_breaks.py` y `src/visualizers/charts.py`, verificando que genere las 5 figuras limpias y `outputs/macro_argentina_latest.json`.
5. Implementá los dos agentes encapsulados (`src/agents/ingestion_healer_agent.py` y `src/agents/visual_and_regime_agent.py`) con fallback determinístico seguro si no hay `GEMINI_API_KEY` configurada.
6. Implementá el sistema de monitoreo y alertas (`src/monitoring/notifier.py`), la suite de `pytest` (`tests/`) y el workflow `.github/workflows/monthly_update.yml`.
```

