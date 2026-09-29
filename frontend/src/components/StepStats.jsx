import React from 'react';
import { useTranslation } from 'react-i18next';
import Alert from './Alert';

const StepStats = ({ state, setState, nextStep, prevStep, error }) => {
  const { t } = useTranslation();

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-slate-800 mb-6">{t('stepStats.title')}</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="flex flex-col gap-1.5 md:col-span-2">
          <label className="text-sm font-semibold text-slate-700">{t('stepStats.equipment')}</label>
          <select 
            className="input-field"
            value={state.equipment} 
            onChange={(e) => setState({ ...state, equipment: e.target.value })}
          >
            <option value="All (Gym Mixed)">{t('options.equipments.All (Gym Mixed)')}</option>
            <option value="Barbell">{t('options.equipments.Barbell')}</option>
            <option value="Dumbbell">{t('options.equipments.Dumbbell')}</option>
            <option value="Machine">{t('options.equipments.Machine')}</option>
            <option value="Cable">{t('options.equipments.Cable')}</option>
            <option value="Bodyweight">{t('options.equipments.Bodyweight')}</option>
            <option value="Cardio">{t('options.equipments.Cardio')}</option>
          </select>
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-semibold text-slate-700">{t('stepStats.squat1RM')}</label>
          <input 
            className="input-field"
            type="number" 
            min="0"
            value={state.squat} 
            onChange={(e) => setState({ ...state, squat: e.target.value })}
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-semibold text-slate-700">{t('stepStats.bench1RM')}</label>
          <input 
            className="input-field"
            type="number" 
            min="0"
            value={state.bench} 
            onChange={(e) => setState({ ...state, bench: e.target.value })}
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-semibold text-slate-700">{t('stepStats.deadlift1RM')}</label>
          <input 
            className="input-field"
            type="number" 
            min="0"
            value={state.deadlift} 
            onChange={(e) => setState({ ...state, deadlift: e.target.value })}
          />
        </div>
      </div>

      <Alert message={error} />


      <div className="flex justify-between items-center gap-4 mt-6">
        <button className="btn-secondary" onClick={prevStep}>
          {t('stepStats.back')}
        </button>
        <button className="btn-primary" onClick={nextStep}>
          {t('stepStats.reviewProfile')}
        </button>
      </div>
    </div>
  );
};

export default StepStats;
