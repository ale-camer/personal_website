# Backlog Transversal: Hardening, Normas ISO y Auditoría de Calidad Web vía MCP + Modelos Frontera

Documento de trabajo para ejecutar en una etapa dedicada sobre el ecosistema web personal:
- **Web Personal (`personal_website`)**
- **QuantLambda**
- *(Extensible también a `plan_n_travel` cuando salga a producción pública)*

---

## 1. Hardening Técnico y de Seguridad Web
Revisar y endurecer de punta a punta cabeceras, transporte, dependencias y superficie expuesta:
- **Cabeceras HTTP de seguridad estrictas:** `Content-Security-Policy` (CSP sin `unsafe-inline` innecesarios), `Strict-Transport-Security` (HSTS con `preload`), `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy` y aislamiento `Cross-Origin-*` (`COOP`/`CORP`).
- **Superficie de red, TLS y DNS:** Configuración TLS 1.3 moderna, registros DNS (`CAA`), protección anti-abuso / *rate-limiting* en bordes/endpoints y minimización de puertos/rutas expuestas en contenedores (`Dockerfile` sin usuario `root`, imágenes mínimas y dependencias fijadas).
- **Cadena de suministro y secretos:** Escaneo automático de vulnerabilidades (`npm audit` / Dependabot / OSV), cero credenciales o *tokens* en cliente/historial Git y validación estricta de entradas en cualquier formulario o API.

## 2. Alineación con Estándares y Normas ISO Aplicables a Software y Web
Usar marcos ISO/estándares internacionales como lista de control objetiva de ingeniería y calidad:
- **ISO/IEC 25010 (Calidad de Producto de Software — SQuaRE):** Evaluar sistemáticamente *Adecuación funcional, Eficiencia de desempeño (Core Web Vitals), Compatibilidad, Usabilidad/Accesibilidad (ISO/IEC 40500 / WCAG 2.2 AA), Fiabilidad, Seguridad, Mantenibilidad y Portabilidad*.
- **ISO/IEC 27001 / 27002 (Seguridad de la Información) + OWASP ASVS:** Controles técnicos aplicables a activos web, gestión de logs sin PII, respaldo, trazabilidad de cambios y configuración segura por defecto.
- **ISO 9241 (Ergonomía de la interacción humano-sistema):** Claridad visual, consistencia de controles, carga cognitiva mínima y feedback inmediato en la interfaz.

## 3. Auditoría Automatizada e Interactiva con MCP + Modelo de Frontera
Armar un flujo reproducible donde un modelo de primer nivel inspeccione las webs reales mediante **servidores MCP** (navegador real + herramientas de auditoría):
- **MCP de Navegador / DevTools / Playwright + Lighthouse:** Que el modelo navegue en vivo cada página (escritorio y móvil), capture DOM, consola, red, tiempos de carga, contraste visual, *layout shifts* y capturas por sección.
- **MCP de Seguridad / Cabeceras / Accesibilidad (`axe-core`, observatorio HTTP):** Chequeo automatizado contra reglas WCAG, CSP/HSTS, SEO técnico (` robots.txt`, `sitemap.xml`, OpenGraph, JSON-LD, canónicos) y rendimiento.
- **Entregable por cada sitio (`personal_website` y `QuantLambda`):** Matriz priorizada de hallazgos (`Crítico / Alto / Medio / Pulido`) con evidencia reproducible y plan quirúrgico de remediación.
