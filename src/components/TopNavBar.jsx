import React from 'react';

export const NAV_ITEMS = [
  { id: 'flagship', label: 'QuantLambda' },
  { id: 'research', label: 'Análisis' },
  { id: 'playground', label: 'Proyectos' },
  { id: 'timeline', label: 'Recorrido' }
];

export default function TopNavBar({
  activeId = null,
  onSelect,
  navStyle = 'capsule',
  navFont = 'orbitron',
  accentHex = '#25D366'
}) {
  return (
    <nav
      className={`top-nav-container nav-style-${navStyle} nav-font-${navFont}`}
      style={{ '--nav-accent': accentHex }}
    >
      {NAV_ITEMS.map((item) => {
        const isActive = activeId === item.id;
        return (
          <button
            key={item.id}
            type="button"
            className={`nav-item-btn ${isActive ? 'is-active' : ''}`}
            onClick={() => onSelect && onSelect(isActive ? null : item.id)}
          >
            <span className="nav-item-label">{item.label}</span>
          </button>
        );
      })}
    </nav>
  );
}
