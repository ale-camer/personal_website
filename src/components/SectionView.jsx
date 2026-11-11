import React, { useState, useEffect } from 'react';
import TimelineSection from './timeline/TimelineSection';
import ProjectsSection from './projects/ProjectsSection';
import ResearchSection from './research/ResearchSection';
import { tx, useSiteLocale } from '../i18n/localeService';

/**
 * Panel central HUD con barra superior propia fija y scroll interno.
 * Se cierra con ✕, Esc, clic afuera o volviendo a tocar el botón activo.
 */
export default function SectionView({ sectionId, label, colorMode = 'dark', lang = 'ES', onClose }) {
  useSiteLocale(lang);
  const [hudOverride, setHudOverride] = useState(null);

  useEffect(() => {
    setHudOverride(null);
  }, [sectionId]);

  useEffect(() => {
    const handleKey = (e) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [onClose]);

  return (
    <div className="sv-a-backdrop" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <section className="sv-a-card" aria-label={label}>
        {/* Mirillas tácticas HUD en las 4 esquinas del contenedor */}
        <span className="tl-hud-corner tl-corner-tl sv-hud-corner" aria-hidden="true" />
        <span className="tl-hud-corner tl-corner-tr sv-hud-corner" aria-hidden="true" />
        <span className="tl-hud-corner tl-corner-bl sv-hud-corner" aria-hidden="true" />
        <span className="tl-hud-corner tl-corner-br sv-hud-corner" aria-hidden="true" />

        {/* BARRA SUPERIOR PROPIA FIJA (NUNCA PISA EL CONTENIDO) */}
        <header className="sv-hud-topbar">
          <div className="sv-hud-topbar-left">
            {hudOverride?.onBack ? (
              <button
                type="button"
                className="sv-hud-back-btn"
                onClick={hudOverride.onBack}
              >
                {hudOverride.backLabel}
              </button>
            ) : (
              <div className="sv-hud-brand">
                <span className="sv-hud-dot" aria-hidden="true" />
                <span className="sv-hud-title">{label}</span>
              </div>
            )}
          </div>

          <div className="sv-hud-topbar-right">
            {sectionId === 'timeline' && (
              <a
                href="/Alejandro_Camerlengo_Data_Engineer.pdf"
                download="Alejandro_Camerlengo_CV.pdf"
                target="_blank"
                rel="noreferrer"
                className="sv-hud-cv-btn"
                title={tx('Descargar CV en formato PDF', 'Download CV in PDF format', lang)}
              >
                {tx('Descargar CV (PDF) ↓', 'Download CV (PDF) ↓', lang)}
              </a>
            )}
            {hudOverride?.repoHref && (
              <a
                href={hudOverride.repoHref}
                target="_blank"
                rel="noreferrer"
                className="sv-hud-action-link"
              >
                {hudOverride.repoLabel}
              </a>
            )}
            <button
              type="button"
              className="sv-close"
              onClick={onClose}
              title={tx('Cerrar (Esc)', 'Close (Esc)', lang)}
              aria-label={tx('Cerrar', 'Close', lang)}
            >
              ✕
            </button>
          </div>
        </header>

        <div className="sv-a-scroll">
          {sectionId === 'timeline' ? (
            <TimelineSection colorMode={colorMode} lang={lang} />
          ) : sectionId === 'playground' ? (
            <ProjectsSection colorMode={colorMode} lang={lang} />
          ) : (
            <ResearchSection
              colorMode={colorMode}
              lang={lang}
              onHudChange={setHudOverride}
            />
          )}
        </div>
      </section>
    </div>
  );
}
