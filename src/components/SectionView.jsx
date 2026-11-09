import React, { useEffect } from 'react';
import QuantLambdaSection from './quantlambda/QuantLambdaSection';
import TimelineSection from './timeline/TimelineSection';
import ProjectsSection from './projects/ProjectsSection';
import ResearchSection from './research/ResearchSection';

/**
 * Panel central translúcido donde se abre cada sección (scroll interno).
 * Se cierra con ✕, Esc, clic afuera o volviendo a tocar el botón activo.
 */
export default function SectionView({ sectionId, label, colorMode = 'dark', onClose }) {
  useEffect(() => {
    const handleKey = (e) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [onClose]);

  return (
    <div className="sv-a-backdrop" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <section className="sv-a-card" aria-label={label}>
        <button
          type="button"
          className="sv-close"
          onClick={onClose}
          title="Cerrar (Esc)"
          aria-label="Cerrar"
        >
          ✕
        </button>
        <div className="sv-a-scroll">
          {sectionId === 'flagship' ? (
            <QuantLambdaSection colorMode={colorMode} />
          ) : sectionId === 'timeline' ? (
            <TimelineSection colorMode={colorMode} />
          ) : sectionId === 'playground' ? (
            <ProjectsSection colorMode={colorMode} />
          ) : (
            <ResearchSection colorMode={colorMode} />
          )}
        </div>
      </section>
    </div>
  );
}
