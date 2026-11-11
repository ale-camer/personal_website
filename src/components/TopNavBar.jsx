import React from 'react';
import { tx, useSiteLocale } from '../i18n/localeService';

export const NAV_ITEMS = [
  { id: 'playground', labelEs: 'Proyectos', labelEn: 'Projects' },
  { id: 'research', labelEs: 'Análisis', labelEn: 'Research' },
  { id: 'timeline', labelEs: 'Mi CV', labelEn: 'My CV' }
];

export function getNavLabel(id, lang = 'ES') {
  const item = NAV_ITEMS.find((it) => it.id === id);
  if (!item) return '';
  return tx(item.labelEs, item.labelEn, lang);
}

export default function TopNavBar({
  activeId = null,
  onSelect,
  lang = 'ES',
  navStyle = 'capsule',
  navFont = 'orbitron',
  accentHex = '#25D366'
}) {
  useSiteLocale(lang);

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
            <span className="nav-item-label">{tx(item.labelEs, item.labelEn, lang)}</span>
          </button>
        );
      })}
    </nav>
  );
}
