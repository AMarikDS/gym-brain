import React from 'react';
import { useTranslation } from 'react-i18next';

const StepMuscle = ({ prevStep, startWorkout }) => {
  const { t } = useTranslation();

  return (

    <div className="card text-center">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-slate-800 mb-2">
          {t('stepMuscle.successTitle')}
        </h2>
        <p className="text-slate-500 font-medium">
          {t('stepMuscle.successSubtitle')}
        </p>
      </div>

      <h3 className="text-lg font-semibold text-slate-700 mb-4 text-left">
        {t('stepMuscle.selectInitial')}
      </h3>
      
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        <button 
          className="btn-secondary py-4 hover:border-primary-500 hover:text-primary-600"
          onClick={() => startWorkout(15, "Bench Press (Barbell)", t('stepMuscle.chest'), "Barbell")}
        >
          {t('stepMuscle.chest')}
        </button>
        <button 
          className="btn-secondary py-4 hover:border-primary-500 hover:text-primary-600"
          onClick={() => startWorkout(5, "Squat (Barbell)", t('stepMuscle.legs'), "Barbell")}
        >
          {t('stepMuscle.legs')}
        </button>
        <button 
          className="btn-secondary py-4 hover:border-primary-500 hover:text-primary-600"
          onClick={() => startWorkout(720, "Deadlift (Barbell)", t('stepMuscle.back'), "Barbell")}
        >
          {t('stepMuscle.back')}
        </button>
        <button 
          className="btn-secondary py-4 hover:border-primary-500 hover:text-primary-600"
          onClick={() => startWorkout(1778, "Overhead Press (Barbell)", t('stepMuscle.shoulders'), "Barbell")}
        >
          {t('stepMuscle.shoulders')}
        </button>
        <button 
          className="btn-secondary py-4 hover:border-primary-500 hover:text-primary-600"
          onClick={() => startWorkout(363, "Bicep Curl (Dumbbell)", t('stepMuscle.arms'), "Dumbbell")}
        >
          {t('stepMuscle.arms')}
        </button>
        <button 
          className="btn-secondary py-4 hover:border-primary-500 hover:text-primary-600"
          onClick={() => startWorkout(130, "Abs Crunch (Bodyweight)", t('stepMuscle.core'), "Bodyweight")}
        >
          {t('stepMuscle.core')}
        </button>
      </div>

      <div className="mt-8 flex justify-start">
        <button className="btn-secondary max-w-[200px]" onClick={prevStep}>
          {t('stepMuscle.backToStats')}
        </button>
      </div>
    </div>
  );
};

export default StepMuscle;
