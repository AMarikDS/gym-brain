import React from 'react';
import { useTranslation } from 'react-i18next';
import Alert from './Alert';

const StepBio = ({ state, setState, nextStep, error }) => {
  const { t } = useTranslation();

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-slate-800 mb-6">{t('stepBio.title')}</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-semibold text-slate-700">{t('stepBio.level')}</label>
          <select 
            className="input-field"
            value={state.level} 
            onChange={(e) => setState({ ...state, level: e.target.value })}
          >
            <option value="Novice">{t('options.levels.Novice', 'Novice')}</option>
            <option value="Beginner">{t('options.levels.Beginner', 'Beginner')}</option>
            <option value="Intermediate">{t('options.levels.Intermediate', 'Intermediate')}</option>
            <option value="Advanced">{t('options.levels.Advanced', 'Advanced')}</option>
          </select>
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-semibold text-slate-700">{t('stepBio.goal')}</label>
          <select 
            className="input-field"
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

        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-semibold text-slate-700">{t('stepBio.sex')}</label>
          <select 
            className="input-field"
            value={state.sex} 
            onChange={(e) => setState({ ...state, sex: e.target.value })}
          >
            <option value="Male">{t('options.sexes.Male')}</option>
            <option value="Female">{t('options.sexes.Female')}</option>
          </select>
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-semibold text-slate-700">{t('stepBio.age')}</label>
          <input 
            className="input-field"
            type="number" 
            min="10" 
            max="120"
            value={state.age} 
            onChange={(e) => setState({ ...state, age: e.target.value })}
          />
        </div>

        <div className="flex flex-col gap-1.5 md:col-span-2">
          <label className="text-sm font-semibold text-slate-700">{t('stepBio.bodyweight')}</label>
          <input 
            className="input-field"
            type="number" 
            min="20" 
            max="300"
            value={state.bw} 
            onChange={(e) => setState({ ...state, bw: e.target.value })}
          />
        </div>
      </div>

      <Alert message={error} />

      <div className="flex justify-end mt-4">
        <button className="btn-primary" onClick={nextStep}>
          {t('stepBio.nextStep')}
        </button>
      </div>
    </div>
  );
};

export default StepBio;
