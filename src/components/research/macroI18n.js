import { tx, txList } from '../../i18n/localeService';

// Diccionario multilingüe (56 idiomas) para la sección de Análisis y los 5 gráficos nativos.

export const MACRO_I18N = {
  ES: {
    hubTitle: 'Investigaciones cuantitativas y económicas construidas desde datos primarios',
    hubLead: 'Estudios realizados cruzando series oficiales y modelos econométricos para responder preguntas concretas con criterio de dominio.',
    studyTitle: 'Macroeconomía, Gasto Público y Degradación del Empleo en Argentina',
    studyOneLiner: 'Radiografía empírica en 4 ejes (1980–Presente): inflación, gasto público/PBI, estancamiento privado, caída del salario real y proyecciones SARIMAX.',
    thesisTag: 'TESIS CENTRAL',
    thesisText: 'El estancamiento del PBI desde 2011 y el salto del gasto público/PBI financiando déficits con emisión no solo erosionaron el salario real, sino que ocultaron el freno del empleo asalariado privado detrás de un crecimiento artificial de modalidades precarizadas y empleo público.',
    bullets: [
      'Eje 1 (Políticas, Gasto e Inflación desde 1980): Tres regímenes macroeconómicos marcados por la duplicación del gasto público/PBI en los 2000s sin contraparte sostenible de producto.',
      'Eje 2 y 3 (Cantidad y Calidad del Empleo): El empleo privado registrado quedó virtualmente congelado frente al crecimiento demográfico (+22.1%), perdiendo 8.1 pp de participación en el padrón formal.',
      'Eje 4 (Precio / Salario Real y Proyección SARIMAX): Caída acumulada de ~24.6% en el poder adquisitivo real respecto del pico de 2012, estrechamente atada a la contracción del producto.'
    ],
    readCta: 'Leer Ensayo Completo ↗',
    backBtn: '← Volver a Análisis',
    repoLink: 'Pipeline & Código ↗',
    essayMainTitle: 'Argentina: Macroeconomía, Gasto Público y Degradación del Empleo (1980–Presente)',
    essaySubtitle: 'En este análisis se ilustran en cinco visualizaciones fundamentales los problemas macroeconómicos estructurales de Argentina y cómo impactan de forma directa sobre el empleo tanto en materia de cantidad y calidad como de precio (salario real).',
    sec1Num: 'EJE 01 // 1980–',
    sec1Title: 'Política económica, gasto público y crecimiento',
    sec1P1: 'La economía argentina desde 1880 hasta la actualidad tuvo únicamente dos décadas completas de estancamiento neto: 1980–1989 y 2010–2019 (prolongada en la primera mitad de los 2020s). Para entender por qué ocurre esto hay que observar las dos caras de la política económica: la política fiscal (cuánto gasta el Estado y cuánto necesita extraer del sector privado) y la política monetaria (el equilibrio entre oferta y demanda de dinero que determina la estabilidad de precios).',
    sec1P2: 'Cuanto menor y más eficiente es el gasto público consolidado, mayor cantidad de recursos quedan disponibles en el sector privado para ampliar su capacidad productiva. Por el contrario, cuando el gasto público salta estructuralmente por encima de la recaudación genuina y se financia con endeudamiento o emisión monetaria, el resultado es crisis de deuda o aceleración inflacionaria.',
    sec1P3: 'El primer gráfico muestra con claridad los tres grandes regímenes: durante 1980–1990, a pesar de tener un gasto público cercano al ~19.3% del PBI, el descontrol monetario ahogó a la economía en alta inflación hasta desembocar en las hiperinflaciones de 1989 y 1990. Durante 1991–2001, la Convertibilidad eliminó la inflación (promedio 4.4% anual) y permitió expandir el PBI real, aunque el aumento gradual del déficit fiscal financiado con deuda terminó en la crisis de 2001–2002. Finalmente, tras la recuperación de 2003–2011 impulsada por el ajuste inicial y el boom de materias primas, el gasto público consolidado duplicó su peso hasta promediar 37.8% del PBI en 2011–2024 junto con una inflación promedio superior al 69% anual, bloqueando el crecimiento económico desde 2011.',
    sec2Num: 'EJE 02 // 2009–',
    sec2Title: 'Empleo (Cantidad): Sin crecimiento del PBI no hay empleo privado',
    sec2P1: 'El segundo gráfico exhibe el efecto directo que tiene la falta de crecimiento económico sobre la generación de puestos de trabajo. Es fundamental poner el foco en el empleo asalariado privado registrado porque es el sector que financia de forma genuina al resto de la economía y representa el núcleo productivo del trabajo formal.',
    sec2P2: (r, beta) => `Durante la ventana de crecimiento 2009–2011, la expansión de la actividad económica (EMAE) traccionó la creación neta de empleo privado formal. Sin embargo, a partir del freno macroeconómico de 2012 en adelante, tanto la actividad como el empleo privado entraron en una meseta estructural (con una correlación de r = ${r} y una elasticidad empleo-producto de β = ${beta}: cada 10% de caída o estancamiento del producto impacta en ~4.4% sobre el empleo privado formal).`,
    sec3Num: 'EJE 03 // 2012–',
    sec3Title: 'Empleo (Calidad): Degradación composicional frente al crecimiento demográfico',
    sec3P1: 'La primera reflexión al cruzar todas las modalidades ocupacionales con la evolución demográfica es contundente: el total de ocupados registrados creció apenas a la par de la población, pero a expensas de una severa reducción en su calidad. En Argentina conviven seis grandes figuras dentro del sistema registrado:',
    sec3Li1: (gap) => `Asalariados Privados y Autónomos: El núcleo de mayor productividad y generación de valor agregado (donde los autónomos representan además el semillero de futuras empresas). Entre 2012 y la actualidad su crecimiento neto fue virtualmente nulo o negativo (-0.4% y -6.8%) frente a una población que creció +22.1%, abriendo una brecha demográfica de ${gap}.`,
    sec3Li2: 'Empleo Público y Monotributo Estándar: Crecieron muy por encima de la economía productiva (+33.1% en empleo público y +68.5% en monotributo independiente de menor capacidad contributiva).',
    sec3Li3: 'Monotributo Social: La categoría subsidiada de menores ingresos del sistema llegó a expandirse más de +160% en la década 2012–2023 y, aun tras la depuración de padrones de 2024–2025, acumula +31.8% desde 2012.',
    sec3P2: 'En términos de participación sobre el total del trabajo registrado (Visual 04), el empleo asalariado privado cayó del 55.86% en enero de 2012 al 47.79% actual (-8.06 pp), siendo desplazado por monotributistas (+5.38 pp) y empleo público (+3.33 pp).',
    sec4Num: 'EJE 04 // 2005–',
    sec4Title: 'Empleo (Precio): Evolución del salario real y poder adquisitivo',
    sec4P1: 'Al estudiar la evolución del precio del trabajo (el salario real), se comprueba que la capacidad de compra de los trabajadores crece sí y solo sí la economía crece de forma sostenida. Cuando el PBI se estanca o retrocede y la inflación se acelera, el poder adquisitivo cae de manera continua y tarda años en recuperarse.',
    sec4P2: (idx) => `Tras alcanzar su máximo histórico en 2012–2013 (Índice = 100), el estancamiento productivo combinado con el salto inflacionario a partir de 2018 provocó un desplome estructural del salario real, que se ubica en ${idx} puntos (base 2012 = 100): una pérdida cercana a una cuarta parte del poder de compra real respecto de hace poco más de una década.`,
    sec5Num: 'ANEXO CUANTITATIVO // PROYECCIÓN SARIMAX & FUENTES',
    sec5Title: 'Proyección base a 6 meses (SARIMAX) y trazabilidad de fuentes oficiales',
    fcCard1: 'Actividad Económica (EMAE Desestacionalizado • Base Ene-2009 = 100)',
    fcCard2: 'Empleo Asalariado Privado Registrado (SIPA • Base Ene-2009 = 100)',
    fcColPeriod: 'Período',
    fcColPoint: 'Proyección Puntual',
    fcColCi: 'IC 95% (Banda Inferior – Superior)',
    sourcesTitle: 'FUENTES PRIMARIAS OFICIALES',
    cutoffLabel: 'Corte',
    expandedHeader: 'VISTA AMPLIADA',
    zoomBtn: 'Ampliar gráfico ⤢',
    closeBtn: '✕ Cerrar',
    v1Badge: 'VISUAL 01 // PBI REAL, GASTO PÚBLICO E INFLACIÓN (1980–PRESENTE)',
    v1Title: 'Política Económica, Gasto Público Consolidado y Estancamiento del PBI Real',
    v1Sub: 'Panel superior: Índice PBI Real (1980=100), Gasto Público (% PBI) e Inflación acotada a 100% • Panel inferior: Variación anual PBI Real (%)',
    v1LegendGdp: 'PBI Real (Índice 1980 = 100)',
    v1LegendExp: 'Gasto Público Consolidado (% PBI)',
    v1LegendInf: 'Inflación Deflactor PBI (tope visual 100%)',
    v1Regime1: '1980–1990: Descontrol Monetario',
    v1Regime1Sub: 'Gasto: 19.3% PBI • Infl. prom: 592%',
    v1Regime2: '1991–2001: Convertibilidad',
    v1Regime2Sub: 'Gasto: 22.8% PBI • Infl. prom: 4.4%',
    v1Regime3: '2011–Presente: Salto Fiscal & Estanflación',
    v1Regime3Sub: 'Gasto: 37.8% PBI • Infl. prom: >69%',
    v1BarTitle: 'Variación Interanual del PBI Real (%)',
    v1Caption: 'Fuente: Elaboración propia automatizada sobre datos del Banco Mundial y Ministerio de Economía.',
    v2Badge: 'VISUAL 02 // ELASTICIDAD EMPLEO PRIVADO VS. ACTIVIDAD ECONÓMICA (EMAE)',
    v2Title: 'Evolución del Empleo Asalariado Privado Registrado vs. Actividad Económica (EMAE)',
    v2Sub: 'Números índice Base Enero 2009 = 100 y banda de proyección SARIMAX (6 meses)',
    v2LegendJobs: 'Empleo Asalariado Privado (SIPA)',
    v2LegendEmaeTc: 'EMAE Tendencia-Ciclo',
    v2LegendEmaeDes: 'EMAE Desestacionalizado',
    v2LegendEmaeOrig: 'EMAE Serie Original',
    v2LegendForecast: 'Proyección SARIMAX (IC 95%)',
    v2RegimeA: '2009–2011: Expansión',
    v2RegimeASub: 'PBI y empleo privado crecen a la par',
    v2RegimeB: '2012–Presente: Meseta Estructural',
    v2RegimeBSub: 'Correlación r = 82.3% • Elasticidad β = 0.44',
    v2Caption: 'Fuente: SIPA (Secretaría de Trabajo) e INDEC (EMAE Base 2004=100, re-indexados a Enero 2009 = 100).',
    v3Badge: 'VISUAL 03 // CRECIMIENTO ACUMULADO POR MODALIDAD VS. DEMOGRAFÍA (BASE 2012 = 0%)',
    v3Title: 'Crecimiento Acumulado por Modalidad Ocupacional vs. Crecimiento Poblacional',
    v3Sub: 'Variación porcentual acumulada desde Enero 2012 (0%) hasta el último corte oficial',
    v3ModSoc: 'Monotributo Social',
    v3ModMono: 'Monotributo Estándar',
    v3ModPub: 'Empleo Público',
    v3ModPop: 'Crecimiento Poblacional (+22.1%)',
    v3ModTot: 'Total Registrado',
    v3ModPriv: 'Empleo Asalariado Privado (-0.4%)',
    v3ModDom: 'Casas Particulares',
    v3ModAut: 'Autónomos (-6.8%)',
    v3CalloutTitle: 'Pico pre-reforma (Dic 2023): +160.3%',
    v3CalloutSub: 'Depuración de padrón 2024–2025 → +31.8% actual',
    v3Caption: 'Fuente: SIPA / Secretaría de Trabajo y proyecciones demográficas Banco Mundial / INDEC (Enero 2012 = 0%).',
    v4Badge: 'VISUAL 04 // CAMBIO ESTRUCTURAL EN LA COMPOSICIÓN DEL TRABAJO REGISTRADO',
    v4Title: 'Participación Porcentual de cada Modalidad sobre el Total del Empleo Registrado',
    v4Sub: 'Comparativa estructural entre Enero 2012, Marzo 2022 y el último corte disponible',
    v4ColMod: 'Modalidad Ocupacional',
    v4Col2012: 'Ene 2012',
    v4Col2022: 'Mar 2022',
    v4ColLatest: 'Actual',
    v4ColDelta: 'Cambio Neto (2012 → Actual)',
    v4Caption: 'Fuente: SIPA / Secretaría de Trabajo. El empleo asalariado privado perdió 8.06 pp de participación en el total formal.',
    v5Badge: 'VISUAL 05 // SALARIO REAL VS. PBI REAL (ÍNDICE BASE 2012 = 100 Y VARIACIÓN ANUAL)',
    v5Title: 'Evolución del Poder Adquisitivo (Salario Real) vs. PBI Real',
    v5Sub: 'Panel superior: Números índice Base 2012 = 100 • Panel inferior: Variación interanual (%)',
    v5LegendWage: 'Salario Real Promedio (Base 2012 = 100)',
    v5LegendGdp: 'PBI Real (Base 2012 = 100)',
    v5BarTitle: 'Variación Interanual: Salario Real vs. PBI Real (%)',
    v5Callout: 'Pérdida de ~24.6% en el salario real respecto del máximo de 2012–2013',
    v5Caption: 'Fuente: Empalme de series históricas de Índice de Salarios (INDEC), deflactor implícito y PBI real (Banco Mundial).'
  },
  EN: {
    hubTitle: 'Quantitative and economic research built from primary data',
    hubLead: 'Empirical studies combining official time series and econometric models to answer concrete questions with domain expertise.',
    studyTitle: 'Macroeconomics, Public Spending & Labor Quality Degradation in Argentina',
    studyOneLiner: 'Empirical analysis across 4 axes (1980–Present): inflation, public spending/GDP, private job stagnation, real wage erosion & SARIMAX forecasts.',
    thesisTag: 'CORE THESIS',
    thesisText: 'GDP stagnation since 2011 and the structural jump in public spending/GDP financed through monetary issuance not only eroded real wages, but masked the freeze in formal private wage employment behind an expansion of subsidized low-income categories and public sector jobs.',
    bullets: [
      'Axis 1 (Policy, Spending & Inflation since 1980): Three macroeconomic regimes marked by the doubling of public spending/GDP in the 2000s without sustainable output growth.',
      'Axis 2 & 3 (Employment Quantity & Quality): Registered private wage employment remained virtually frozen against demographic growth (+22.1%), losing 8.1 pp of formal share.',
      'Axis 4 (Price / Real Wage & SARIMAX Forecast): Cumulative ~24.6% loss in real purchasing power relative to the 2012 peak, tightly bound to output contraction.'
    ],
    readCta: 'Read Full Essay ↗',
    backBtn: '← Back to Research',
    repoLink: 'Pipeline & Code ↗',
    essayMainTitle: 'Argentina: Macroeconomics, Public Spending & Labor Degradation (1980–Present)',
    essaySubtitle: 'This study illustrates across five core visualizations the structural macroeconomic problems of Argentina and how they directly impact employment both in quantity/quality and in price (real wages).',
    sec1Num: 'AXIS 01 // 1980–',
    sec1Title: 'Economic policy, public spending and output growth',
    sec1P1: 'From 1880 to the present, Argentina experienced only two full decades of net economic stagnation: 1980–1989 and 2010–2019 (extended into the first half of the 2020s). Understanding why requires examining both sides of economic policy: fiscal policy (how much the state spends and extracts from the private sector) and monetary policy (the balance between money supply and demand that governs price stability).',
    sec1P2: 'The lower and more efficient consolidated public spending is, the greater the resources left available in the private sector to expand productive capacity. Conversely, when public spending jumps structurally above genuine tax revenue and is financed through debt or money printing, the result is either sovereign debt crisis or chronic inflation.',
    sec1P3: 'Visual 01 highlights three distinct regimes: during 1980–1990, despite relatively low public spending (~19.3% of GDP), monetary financing triggered chronic inflation culminating in the 1989–1990 hyperinflations. During 1991–2001, Convertibility eliminated inflation (averaging 4.4% annually) and enabled strong real GDP expansion, though rising debt-financed deficits ended in the 2001–2002 crisis. Finally, after the 2003–2011 commodity-backed recovery, consolidated public spending doubled to average 37.8% of GDP in 2011–2024 alongside average inflation above 69%, halting economic growth since 2011.',
    sec2Num: 'AXIS 02 // 2009–',
    sec2Title: 'Employment (Quantity): Without GDP growth there is no private employment',
    sec2P1: 'The second chart demonstrates the direct link between economic growth and job creation. Focusing on registered private wage employment is essential because it is the sector that genuinely finances public spending and represents the productive core of formal labor.',
    sec2P2: (r, beta) => `During the 2009–2011 growth window, expanding economic activity (EMAE) drove net private job creation. However, starting with the 2012 macroeconomic freeze, both economic activity and private formal employment entered a structural plateau (with correlation r = ${r} and employment-output elasticity β = ${beta}: every 10% drop or stagnation in output translates into a ~4.4% impact on private formal jobs).`,
    sec3Num: 'AXIS 03 // 2012–',
    sec3Title: 'Employment (Quality): Compositional degradation against demographic growth',
    sec3P1: 'Crossing all registered occupational modalities against demographic growth reveals a stark reality: total registered employment barely kept pace with population growth, but at the expense of a severe degradation in job quality across the six legal categories:',
    sec3Li1: (gap) => `Private Wage Earners & Autonomous Workers: The highest-productivity, highest-value-added core (where autonomous workers represent future enterprises). Between 2012 and the present, their net growth was virtually zero or negative (-0.4% and -6.8%) against +22.1% population growth, opening a demographic gap of ${gap}.`,
    sec3Li2: 'Public Sector & Standard Monotributo: Grew far above the productive economy (+33.1% in public employment and +68.5% in lower-contribution independent monotributo).',
    sec3Li3: 'Social Monotributo: The lowest-income subsidized category expanded by over +160% between 2012 and 2023 and, even after the 2024–2025 registry audits, remains +31.8% above 2012.',
    sec3P2: 'In terms of share over total registered employment (Visual 04), formal private wage employment fell from 55.86% in January 2012 to 47.79% today (-8.06 pp), displaced by Monotributo (+5.38 pp) and public employment (+3.33 pp).',
    sec4Num: 'AXIS 04 // 2005–',
    sec4Title: 'Employment (Price): Real wage evolution and purchasing power',
    sec4P1: 'Examining the price of labor (the real wage) confirms that workers’ purchasing power grows if and only if the economy grows sustainably. When GDP stagnates or contracts and inflation accelerates, purchasing power falls continuously and takes years to recover.',
    sec4P2: (idx) => `After reaching its historical peak in 2012–2013 (Index = 100), output stagnation combined with the inflationary surge from 2018 onward caused a structural collapse in real wages, which now stand at ${idx} points (base 2012 = 100): a loss of nearly one-fourth of real purchasing power over little more than a decade.`,
    sec5Num: 'QUANTITATIVE ANNEX // SARIMAX FORECAST & SOURCES',
    sec5Title: '6-month baseline projection (SARIMAX) and official primary sources',
    fcCard1: 'Economic Activity (Seasonally Adjusted EMAE • Base Jan-2009 = 100)',
    fcCard2: 'Registered Private Wage Employment (SIPA • Base Jan-2009 = 100)',
    fcColPeriod: 'Period',
    fcColPoint: 'Point Forecast',
    fcColCi: '95% CI (Lower – Upper Bound)',
    sourcesTitle: 'OFFICIAL PRIMARY SOURCES',
    cutoffLabel: 'Cutoff',
    expandedHeader: 'EXPANDED VIEW',
    zoomBtn: 'Expand chart ⤢',
    closeBtn: '✕ Close',
    v1Badge: 'VISUAL 01 // REAL GDP, PUBLIC SPENDING & INFLATION (1980–PRESENT)',
    v1Title: 'Economic Policy, Consolidated Public Spending & Real GDP Stagnation',
    v1Sub: 'Top panel: Real GDP Index (1980=100), Public Spending (% GDP) & Inflation capped at 100% • Bottom panel: Annual Real GDP Growth (%)',
    v1LegendGdp: 'Real GDP (Index 1980 = 100)',
    v1LegendExp: 'Public Spending (% GDP)',
    v1LegendInf: 'GDP Deflator Inflation (capped at 100%)',
    v1Regime1: '1980–1990: Monetary Instability',
    v1Regime1Sub: 'Spending: 19.3% GDP • Avg Infl: 592%',
    v1Regime2: '1991–2001: Convertibility',
    v1Regime2Sub: 'Spending: 22.8% GDP • Avg Infl: 4.4%',
    v1Regime3: '2011–Present: Fiscal Jump & Stagflation',
    v1Regime3Sub: 'Spending: 37.8% GDP • Avg Infl: >69%',
    v1BarTitle: 'Annual Real GDP Growth (%)',
    v1Caption: 'Source: Automated calculations based on World Bank and Ministry of Economy.',
    v2Badge: 'VISUAL 02 // PRIVATE EMPLOYMENT ELASTICITY VS. ECONOMIC ACTIVITY (EMAE)',
    v2Title: 'Registered Private Wage Employment vs. Economic Activity (EMAE)',
    v2Sub: 'Index numbers Base Jan 2009 = 100 and 6-month SARIMAX forecast band',
    v2LegendJobs: 'Private Wage Employment (SIPA)',
    v2LegendEmaeTc: 'EMAE Trend-Cycle',
    v2LegendEmaeDes: 'EMAE Seasonally Adjusted',
    v2LegendEmaeOrig: 'EMAE Original Series',
    v2LegendForecast: 'SARIMAX Forecast (95% CI)',
    v2RegimeA: '2009–2011: Expansion',
    v2RegimeASub: 'Output and private jobs grow together',
    v2RegimeB: '2012–Present: Structural Plateau',
    v2RegimeBSub: 'Correlation r = 82.3% • Elasticity β = 0.44',
    v2Caption: 'Source: SIPA (Ministry of Labor) and INDEC (EMAE Base 2004=100, re-indexed to Jan 2009 = 100).',
    v3Badge: 'VISUAL 03 // CUMULATIVE GROWTH BY LABOR MODALITY VS. DEMOGRAPHICS (BASE 2012 = 0%)',
    v3Title: 'Cumulative Growth by Labor Modality vs. Population Growth',
    v3Sub: 'Cumulative percentage change from January 2012 (0%) to latest official cutoff',
    v3ModSoc: 'Social Monotributo (Subsidized)',
    v3ModMono: 'Standard Monotributo',
    v3ModPub: 'Public Sector Employment',
    v3ModPop: 'Population Growth (+22.1%)',
    v3ModTot: 'Total Registered Jobs',
    v3ModPriv: 'Private Wage Employment (-0.4%)',
    v3ModDom: 'Domestic Workers',
    v3ModAut: 'Autonomous Workers (-6.8%)',
    v3CalloutTitle: 'Pre-reform peak (Dec 2023): +160.3%',
    v3CalloutSub: '2024–2025 registry audit → +31.8% latest',
    v3Caption: 'Source: SIPA / Ministry of Labor and World Bank / INDEC demographic projections (Jan 2012 = 0%).',
    v4Badge: 'VISUAL 04 // STRUCTURAL SHIFT IN REGISTERED EMPLOYMENT COMPOSITION',
    v4Title: 'Percentage Share of Each Labor Modality in Total Registered Employment',
    v4Sub: 'Structural comparison across January 2012, March 2022, and latest cutoff',
    v4ColMod: 'Labor Modality',
    v4Col2012: 'Jan 2012',
    v4Col2022: 'Mar 2022',
    v4ColLatest: 'Latest',
    v4ColDelta: 'Net Shift (2012 → Latest)',
    v4Caption: 'Source: SIPA / Ministry of Labor. Formal private wage employment lost 8.06 pp of total share.',
    v5Badge: 'VISUAL 05 // REAL WAGE VS. REAL GDP (INDEX BASE 2012 = 100 & ANNUAL CHANGE)',
    v5Title: 'Purchasing Power Evolution (Real Wage) vs. Real GDP',
    v5Sub: 'Top panel: Index numbers Base 2012 = 100 • Bottom panel: Year-over-Year change (%)',
    v5LegendWage: 'Average Real Wage (Base 2012 = 100)',
    v5LegendGdp: 'Real GDP (Base 2012 = 100)',
    v5BarTitle: 'Year-over-Year Change: Real Wage vs. Real GDP (%)',
    v5Callout: '~24.6% real purchasing power loss since the 2012–2013 peak',
    v5Caption: 'Source: Linked historical Wage Index series (INDEC), implicit deflator and Real GDP (World Bank).'
  }
};

// Traducciones localizadas para los otros 15 idiomas del selector global
const LOCALIZED_OVERRIDES = {
  FI: {
    hubTitle: 'Kvantitatiiviset ja taloudelliset tutkimukset primääridatasta',
    hubLead: 'Empiiriset tutkimukset, jotka yhdistävät viralliset aikasarjat ja ekonometriset mallit.',
    studyTitle: 'Makrotalous, julkiset menot ja työmarkkinoiden laadun heikkeneminen Argentiinassa',
    studyOneLiner: 'Empiirinen analyysi 4 akselilla (1980–nykyhetki): inflaatio, julkiset menot/BKT, yksityisen työllisyyden pysähtyminen ja reaalipalkat.',
    thesisTag: 'KESKEINEN TEESI',
    thesisText: 'BKT:n pysähtyminen vuodesta 2011 ja julkisten menojen kasvu suhteessa BKT:hen eivät ainoastaan heikentäneet reaalipalkkoja, vaan peittivät yksityisen sektorin työpaikkojen pysähtymisen tuettujen työmuotojen ja julkisen sektorin kasvun taakse.',
    bullets: [
      'Akseli 1 (Talouspolitiikka, menot ja inflaatio vuodesta 1980): Kolme makrotaloudellista regiimiä ja julkisten menojen kaksinkertaistuminen.',
      'Akseli 2 & 3 (Työllisyyden määrä ja laatu): Rekisteröity yksityinen palkkatyö pysyi lähes muuttumattomana väestönkasvuun (+22.1%) nähden (-8.1 pp osuus).',
      'Akseli 4 (Hinta / Reaalipalkka & SARIMAX-ennuste): Kumulatiivinen ~24.6% ostovoiman menetys vuoden 2012 huipusta.'
    ],
    readCta: 'Lue koko tutkielma ↗',
    backBtn: '← Takaisin analyyseihin',
    repoLink: 'Putkisto & Koodi ↗',
    essayMainTitle: 'Argentiina: Makrotalous, julkiset menot ja työllisyyden rapautuminen (1980–nykyhetki)',
    essaySubtitle: 'Tässä tutkimuksessa havainnollistetaan viidellä keskeisellä kuviolla Argentiinan rakenteellisia makrotaloudellisia ongelmia ja niiden suoraa vaikutusta työllisyyden määrään, laatuun ja hintaan (reaalipalkkaan).',
    sec1Title: 'Talouspolitiikka, julkiset menot ja talouskasvu',
    sec2Title: 'Työllisyys (Määrä): Ilman BKT:n kasvua ei synny yksityisiä työpaikkoja',
    sec3Title: 'Työllisyys (Laatu): Rakenteellinen heikkeneminen suhteessa väestönkasvuun',
    sec4Title: 'Työllisyys (Hinta): Reaalipalkan ja ostovoiman kehitys',
    sec5Title: '6 kuukauden SARIMAX-ennuste ja viralliset primäärilähteet',
    sourcesTitle: 'VIRALLISET PRIMÄÄRILÄHTEET',
    cutoffLabel: 'Viimeisin',
    expandedHeader: 'LAAJENNETTU NÄKYMÄ',
    zoomBtn: 'Suurenna kaavio ⤢',
    closeBtn: '✕ Sulje',
    v1Title: 'Talouspolitiikka, julkiset menot (% BKT) ja reaalisen BKT:n pysähtyminen',
    v1LegendGdp: 'Reaalinen BKT (Indeksi 1980 = 100)',
    v1LegendExp: 'Julkiset menot (% BKT)',
    v1LegendInf: 'BKT-deflaattori-inflaatio (katto 100%)',
    v1BarTitle: 'Reaalisen BKT:n vuosimuutos (%)',
    v2Title: 'Rekisteröity yksityinen palkkatyö vs. taloudellinen toimeliaisuus (EMAE)',
    v2LegendJobs: 'Yksityinen palkkatyö (SIPA)',
    v2LegendEmaeTc: 'EMAE Trendi-sykli',
    v2LegendEmaeDes: 'EMAE Kausitasoitettu',
    v2LegendEmaeOrig: 'EMAE Alkuperäinen',
    v2LegendForecast: 'SARIMAX-ennuste (95% LV)',
    v3Title: 'Kumulatiivinen kasvu työmuodoittain vs. väestönkasvu (2012 = 0%)',
    v3ModSoc: 'Sosiaalinen Monotributo',
    v3ModMono: 'Monotributo',
    v3ModPub: 'Julkinen sektori',
    v3ModPop: 'Väestönkasvu (+22.1%)',
    v3ModTot: 'Rekisteröidyt yhteensä',
    v3ModPriv: 'Yksityinen sektori (-0.4%)',
    v3ModDom: 'Kotitaloustyö',
    v3ModAut: 'Yrittäjät / Autónomos (-6.8%)',
    v4Title: 'Työmuotojen prosenttiosuus kaikista rekisteröidyistä työpaikoista',
    v4ColMod: 'Työmuoto',
    v4Col2012: 'Tammi 2012',
    v4Col2022: 'Maalis 2022',
    v4ColLatest: 'Nykyinen',
    v4ColDelta: 'Nettomuutos (2012 → Nykyinen)',
    v5Title: 'Ostovoiman kehitys (Reaalipalkka) vs. Reaalinen BKT (2012 = 100)',
    v5LegendWage: 'Keskimääräinen reaalipalkka (2012 = 100)',
    v5LegendGdp: 'Reaalinen BKT (2012 = 100)',
    v5BarTitle: 'Vuosimuutos: Reaalipalkka vs. Reaalinen BKT (%)'
  },
  PT: {
    hubTitle: 'Pesquisas quantitativas e econômicas construídas a partir de dados primários',
    studyTitle: 'Macroeconomia, Gasto Público e Degradação do Emprego na Argentina',
    readCta: 'Ler Ensaio Completo ↗',
    backBtn: '← Voltar para Análises',
    essayMainTitle: 'Argentina: Macroeconomia, Gasto Público e Degradação do Emprego (1980–Presente)',
    zoomBtn: 'Ampliar gráfico ⤢',
    closeBtn: '✕ Fechar'
  },
  DE: {
    hubTitle: 'Quantitative und ökonomische Forschung auf Basis von Primärdaten',
    studyTitle: 'Makroökonomie, Staatsausgaben und Arbeitsmarktdegradation in Argentinien',
    readCta: 'Vollständige Studie lesen ↗',
    backBtn: '← Zurück zur Analyse',
    essayMainTitle: 'Argentinien: Makroökonomie, Staatsausgaben & Arbeitsmarkt (1980–Heute)',
    zoomBtn: 'Grafik vergrößern ⤢',
    closeBtn: '✕ Schließen'
  },
  FR: {
    hubTitle: 'Recherches quantitatives et économiques construites à partir de données primaires',
    studyTitle: 'Macroéconomie, Dépenses Publiques et Dégradation de l’Emploi en Argentine',
    readCta: 'Lire l’étude complète ↗',
    backBtn: '← Retour aux Analyses',
    essayMainTitle: 'Argentine : Macroéconomie, Dépenses Publiques et Emploi (1980–Présent)',
    zoomBtn: 'Agrandir le graphique ⤢',
    closeBtn: '✕ Fermer'
  },
  IT: {
    hubTitle: 'Ricerche quantitative ed economiche costruite da dati primari',
    studyTitle: 'Macroeconomia, Spesa Pubblica e Degrado dell’Occupazione in Argentina',
    readCta: 'Leggi Studio Completo ↗',
    backBtn: '← Torna alle Analisi',
    essayMainTitle: 'Argentina: Macroeconomia, Spesa Pubblica e Occupazione (1980–Presente)',
    zoomBtn: 'Ingrandisci grafico ⤢',
    closeBtn: '✕ Chiudi'
  }
};

export function getMacroText(lang = 'ES') {
  if (lang === 'ES') return MACRO_I18N.ES;
  if (lang === 'EN') return MACRO_I18N.EN;

  const ov = LOCALIZED_OVERRIDES[lang] || {};
  const esObj = MACRO_I18N.ES;
  const enObj = MACRO_I18N.EN;
  const result = {};

  for (const key of Object.keys(enObj)) {
    if (ov[key] !== undefined) {
      result[key] = ov[key];
      continue;
    }
    const enVal = enObj[key];
    const esVal = esObj[key];
    if (typeof enVal === 'string') {
      result[key] = tx(esVal, enVal, lang);
    } else if (Array.isArray(enVal)) {
      result[key] = txList(esVal, enVal, lang);
    } else if (typeof enVal === 'function') {
      if (key === 'sec2P2') {
        result[key] = (r, beta) => {
          const tpl = tx(
            'Durante la ventana de crecimiento 2009–2011, la expansión de la actividad económica (EMAE) traccionó la creación neta de empleo privado formal. Sin embargo, a partir del freno macroeconómico de 2012 en adelante, tanto la actividad como el empleo privado entraron en una meseta estructural (con una correlación de r = {0} y una elasticidad empleo-producto de β = {1}: cada 10% de caída o estancamiento del producto impacta en ~4.4% sobre el empleo privado formal).',
            'During the 2009–2011 growth window, expanding economic activity (EMAE) drove net private job creation. However, starting with the 2012 macroeconomic freeze, both economic activity and private formal employment entered a structural plateau (with correlation r = {0} and employment-output elasticity β = {1}: every 10% drop or stagnation in output translates into a ~4.4% impact on private formal jobs).',
            lang
          );
          return tpl.replace('{0}', r).replace('{1}', beta);
        };
      } else if (key === 'sec3Li1') {
        result[key] = (gap) => {
          const tpl = tx(
            'Asalariados Privados y Autónomos: El núcleo de mayor productividad y generación de valor agregado (donde los autónomos representan además el semillero de futuras empresas). Entre 2012 y la actualidad su crecimiento neto fue virtualmente nulo o negativo (-0.4% y -6.8%) frente a una población que creció +22.1%, abriendo una brecha demográfica de {0}.',
            'Private Wage Earners & Autonomous Workers: The highest-productivity, highest-value-added core (where autonomous workers represent future enterprises). Between 2012 and the present, their net growth was virtually zero or negative (-0.4% and -6.8%) against +22.1% population growth, opening a demographic gap of {0}.',
            lang
          );
          return tpl.replace('{0}', gap);
        };
      } else if (key === 'sec4P2') {
        result[key] = (idx) => {
          const tpl = tx(
            'Tras alcanzar su máximo histórico en 2012–2013 (Índice = 100), el estancamiento productivo combinado con el salto inflacionario a partir de 2018 provocó un desplome estructural del salario real, que se ubica en {0} puntos (base 2012 = 100): una pérdida cercana a una cuarta parte del poder de compra real respecto de hace poco más de una década.',
            'After reaching its historical peak in 2012–2013 (Index = 100), output stagnation combined with the inflationary surge from 2018 onward caused a structural collapse in real wages, which now stand at {0} points (base 2012 = 100): a loss of nearly one-fourth of real purchasing power over little more than a decade.',
            lang
          );
          return tpl.replace('{0}', idx);
        };
      } else {
        result[key] = enVal;
      }
    } else {
      result[key] = enVal;
    }
  }

  return result;
}
