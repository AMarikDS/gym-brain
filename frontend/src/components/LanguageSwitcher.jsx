import React from 'react';
import { useTranslation } from 'react-i18next';

const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'ru' : 'en';
    i18n.changeLanguage(newLang);
  };

  return (
    <div style={{ position: 'absolute', top: '1.5rem', right: '1.5rem', zIndex: 10, display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.5rem' }}>
      <button
        onClick={toggleLanguage}
        className="glass-card"
        style={{
          padding: '0.5rem 1rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          cursor: 'pointer',
          border: '1px solid rgba(255,255,255,0.3)',
          background: 'rgba(255,255,255,0.7)',
          backdropFilter: 'blur(10px)',
          borderRadius: '20px',
          fontWeight: 600,
          color: '#0f172a',
          transition: 'all 0.2s ease',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
        }}
        onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
        onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}
      >
        <span style={{ opacity: i18n.language === 'en' ? 1 : 0.4 }}>EN</span>
        <span style={{ fontSize: '0.8rem', opacity: 0.5 }}>|</span>
        <span style={{ opacity: i18n.language === 'ru' ? 1 : 0.4 }}>RU</span>
      </button>

      {i18n.language === 'ru' && (
        <div style={{
          fontSize: '0.75rem',
          color: '#64748b',
          background: 'rgba(255,255,255,0.7)',
          padding: '0.25rem 0.5rem',
          borderRadius: '8px',
          backdropFilter: 'blur(4px)',
          border: '1px solid rgba(255,255,255,0.3)',
          animation: 'fadeIn 0.3s ease',
          boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
        }}>
          ML Translation (Beta)
        </div>
      )}
    </div>
  );
};

export default LanguageSwitcher;
