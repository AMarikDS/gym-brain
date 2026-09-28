import React from 'react';
import { useTranslation } from 'react-i18next';
import Alert from './Alert';

const StepBio = ({ state, setState, nextStep, error }) => {
  const { t } = useTranslation();

  return (
    <div className="glass-card">
      <h2 style={{ marginBottom: '1.5rem' }}>{t('stepBio.title')}</h2>
      
      <div className="form-grid">
        <div className="form-group">
          <label>{t('stepBio.level')}</label>
          <select 
            value={state.level} 
            onChange={(e) => setState({ ...state, level: e.target.value })}
          >
            <option value="Novice">{t('options.levels.Novice', 'Novice')}</option>
            <option value="Beginner">{t('options.levels.Beginner', 'Beginner')}</option>
            <option value="Intermediate">{t('options.levels.Intermediate', 'Intermediate')}</option>
            <option value="Advanced">{t('options.levels.Advanced', 'Advanced')}</option>
          </select>
        </div>

        <div className="form-group">
          <label>{t('stepBio.goal')}</label>
          <select 
            value={state.goal} 
            onChange={(e) => setState({ ...state, goal: e.target.value })}
          >
            <option value="Bodybuilding">{t('options.goals.Bodybuilding', 'Bodybuilding')}</option>
            <option value="Powerlifting">{t('options.goals.Powerlifting', 'Powerlifting')}</option>
            <option value="Powerbuilding">{t('options.goals.Powerbuilding', 'Powerbuilding')}</option>
            <option value="Athletics">{t('options.goals.Athletics', 'Athletics')}</option>
            <option value="General Fitness">{t('options.goals.Fitness', 'General Fitness')}</option>
          </select>
        </div>

        <div className="form-group">
          <label>{t('stepBio.sex')}</label>
          <select 
            value={state.sex} 
            onChange={(e) => setState({ ...state, sex: e.target.value })}
          >
            <option value="Male">{t('options.sexes.Male')}</option>
            <option value="Female">{t('options.sexes.Female')}</option>
          </select>
        </div>

        <div className="form-group">
          <label>{t('stepBio.age')}</label>
          <input 
            type="number" 
            min="10" 
            max="120"
            value={state.age} 
            onChange={(e) => setState({ ...state, age: e.target.value })}
          />
        </div>

        <div className="form-group full-width">
          <label>{t('stepBio.bodyweight')}</label>
          <input 
            type="number" 
            min="20" 
            max="300"
            value={state.bw} 
            onChange={(e) => setState({ ...state, bw: e.target.value })}
          />
        </div>
      </div>

      <Alert message={error} />

      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <button className="btn btn-primary" onClick={nextStep}>
          {t('stepBio.nextStep')}
        </button>
      </div>
    </div>
  );
};

export default StepBio;
