import React from 'react';
import { useTranslation } from 'react-i18next';
import Alert from './Alert';

const StepStats = ({ state, setState, nextStep, prevStep, error }) => {
  const { t } = useTranslation();

  return (
    <div className="glass-card">
      <h2 style={{ marginBottom: '1.5rem' }}>{t('stepStats.title')}</h2>
      
      <div className="form-grid">
        <div className="form-group">
          <label>{t('stepStats.equipment')}</label>
          <select 
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

        <div className="form-group">
          <label>{t('stepStats.squat1RM')}</label>
          <input 
            type="number" 
            min="0"
            value={state.squat} 
            onChange={(e) => setState({ ...state, squat: e.target.value })}
          />
        </div>

        <div className="form-group">
          <label>{t('stepStats.bench1RM')}</label>
          <input 
            type="number" 
            min="0"
            value={state.bench} 
            onChange={(e) => setState({ ...state, bench: e.target.value })}
          />
        </div>

        <div className="form-group">
          <label>{t('stepStats.deadlift1RM')}</label>
          <input 
            type="number" 
            min="0"
            value={state.deadlift} 
            onChange={(e) => setState({ ...state, deadlift: e.target.value })}
          />
        </div>
      </div>

      <Alert message={error} />

      <div className="flex-between">
        <button className="btn btn-outline" onClick={prevStep}>
          {t('stepStats.back')}
        </button>
        <button className="btn btn-primary" onClick={nextStep}>
          {t('stepStats.reviewProfile')}
        </button>
      </div>
    </div>
  );
};

export default StepStats;
