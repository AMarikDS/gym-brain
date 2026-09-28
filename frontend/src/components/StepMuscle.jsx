import React from 'react';
import { useTranslation } from 'react-i18next';

const StepMuscle = ({ prevStep, startWorkout }) => {
  const { t } = useTranslation();

  return (
    <div className="glass-card">
      <div style={{ marginBottom: '2rem', textAlign: 'center' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 600, color: '#0f172a' }}>
          {t('stepMuscle.successTitle')}
        </h2>
        <p style={{ color: '#64748b', marginTop: '0.5rem' }}>
          {t('stepMuscle.successSubtitle')}
        </p>
      </div>

      <h3 style={{ fontSize: '1.125rem', marginBottom: '1rem', color: '#0f172a' }}>
        {t('stepMuscle.selectInitial')}
      </h3>
      
      <div className="step-buttons">
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(15, "Bench Press (Barbell)", "Barbell")}
        >
          {t('stepMuscle.chest')}
        </button>
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(5, "Squat (Barbell)", "Barbell")}
        >
          {t('stepMuscle.legs')}
        </button>
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(720, "Deadlift (Barbell)", "Barbell")}
        >
          {t('stepMuscle.back')}
        </button>
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(1778, "Overhead Press (Barbell)", "Barbell")}
        >
          {t('stepMuscle.shoulders')}
        </button>
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(363, "Bicep Curl (Dumbbell)", "Dumbbell")}
        >
          {t('stepMuscle.arms')}
        </button>
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(130, "Abs Crunch (Bodyweight)", "Bodyweight")}
        >
          {t('stepMuscle.core')}
        </button>
      </div>

      <div style={{ marginTop: '2rem', display: 'flex' }}>
        <button className="btn btn-outline" onClick={prevStep}>
          {t('stepMuscle.backToStats')}
        </button>
      </div>
    </div>
  );
};

export default StepMuscle;
