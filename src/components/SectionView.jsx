import React, { useEffect } from 'react';

/**
 * Panel central translúcido donde se abre cada sección (scroll interno).
 * Se cierra con ✕, Esc, clic afuera o volviendo a tocar el botón activo.
 * El contenido actual es placeholder hasta armar cada sección.
 */

// Bloque de texto falso: barras grises de distinto largo
function SkeletonLines({ count = 4 }) {
  const widths = [100, 94, 97, 88, 92, 76, 99, 84];
  return (
    <div className="ph-lines">
      {Array.from({ length: count }).map((_, i) => (
        <span key={i} className="ph-line" style={{ width: `${widths[i % widths.length]}%` }} />
      ))}
    </div>
  );
}

function PlaceholderContent({ label }) {
  return (
    <>
      <div className="ph-hero-box">
        <span className="ph-tag">Placeholder</span>
        <h2 className="ph-hero-title">{label}</h2>
        <SkeletonLines count={2} />
      </div>

      <div className="ph-card-grid">
        {[1, 2, 3].map((n) => (
          <div key={n} className="ph-card">
            <span className="ph-card-title">Bloque {n}</span>
            <SkeletonLines count={3} />
          </div>
        ))}
      </div>

      {[1, 2, 3, 4, 5].map((n) => (
        <div key={n} className="ph-section">
          <h3 className="ph-section-title">Subsección {n}</h3>
          <SkeletonLines count={6} />
          {n === 2 && <div className="ph-chart">[ gráfico / visualización ]</div>}
        </div>
      ))}
    </>
  );
}

export default function SectionView({ label, onClose }) {
  useEffect(() => {
    const handleKey = (e) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [onClose]);

  return (
    <div className="sv-a-backdrop" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <section className="sv-a-card" aria-label={label}>
        <button type="button" className="sv-close" onClick={onClose} title="Cerrar (Esc)" aria-label="Cerrar">
          ✕
        </button>
        <div className="sv-a-scroll">
          <PlaceholderContent label={label} />
        </div>
      </section>
    </div>
  );
}
