import React from 'react';
import { useTranslation } from 'react-i18next';

const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'ru' : 'en';
    i18n.changeLanguage(newLang);
  };

  return (
    <div className="absolute top-6 right-6 z-10 flex flex-col items-end gap-2">
      <button 
        onClick={toggleLanguage}
        className="flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-md border border-slate-200 
                   rounded-full font-semibold text-slate-800 shadow-sm transition-all duration-200 
                   hover:-translate-y-0.5 hover:shadow-md"
      >
        <span className={i18n.language === 'en' ? 'opacity-100' : 'opacity-40'}>EN</span>
        <span className="text-sm opacity-30">|</span>
        <span className={i18n.language === 'ru' ? 'opacity-100' : 'opacity-40'}>RU</span>
      </button>

      {i18n.language === 'ru' && (
        <div className="text-xs text-slate-500 bg-white/80 px-3 py-1.5 rounded-lg backdrop-blur-sm 
                        border border-slate-200 shadow-sm animate-fade-in font-medium">
          ML Translation (Beta)
        </div>
      )}
    </div>
  );
};

export default LanguageSwitcher;
