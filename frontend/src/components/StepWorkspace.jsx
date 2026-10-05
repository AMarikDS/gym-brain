import React, { useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Trash2, RotateCcw, Undo2, Loader2 } from 'lucide-react';

const StepWorkspace = ({ state, resetWorkout, undoLastExercise, addExercise }) => {
  const listContainerRef = useRef(null);
  const { t, i18n } = useTranslation();

  useEffect(() => {
    if (listContainerRef.current) {
      listContainerRef.current.scrollTop = listContainerRef.current.scrollHeight;
    }
  }, [state.history_names]);

  return (
    <div className="card mb-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:divide-x divide-slate-100 md:h-[70vh] md:max-h-[550px] min-h-[400px]">
        {/* Left Column: Trajectory */}
        <div className="flex flex-col h-full min-h-0">
          <h2 className="text-xl font-bold text-slate-800 mb-4 shrink-0">{t('stepWorkspace.currentTrajectory')}</h2>
          
          <div 
            ref={listContainerRef}
            className="bg-slate-50 rounded-xl p-4 border border-slate-100 flex-1 min-h-0 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-200 scroll-smooth"
          >
            <div className="flex flex-col gap-2">
              {state.history_names.map((name, index) => {
                const isLast = index === state.history_names.length - 1;
                return (
                  <div key={index} className="flex justify-between items-center p-2.5 bg-white rounded-lg border border-slate-200 shadow-sm">
                    <span className="font-semibold text-slate-800 text-sm">
                      <span className="text-slate-400 mr-3">{index + 1}.</span>
                      {name}
                    </span>
                    {isLast && (
                      <button 
                        className="text-slate-400 hover:text-red-500 hover:bg-red-50 p-1.5 rounded-md transition-colors"
                        onClick={undoLastExercise}
                        title={t('stepWorkspace.undoExercise')}
                      >
                        <Trash2 size={18} />
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {state.current_prediction && (
            <div className="mt-3 p-3 bg-primary-50 rounded-xl border border-primary-100 animate-fade-in shrink-0">
              <div className="text-xs font-bold text-primary-600 uppercase tracking-wider mb-0.5">{t('stepWorkspace.aiTargetPrediction')}</div>
              <div className="text-xl font-black text-primary-900">{state.current_prediction}</div>
            </div>
          )}

          <div className="flex flex-col gap-2 mt-4 shrink-0">
            <button className="btn-secondary flex justify-center items-center gap-2 py-2" onClick={undoLastExercise}>
              <Undo2 size={18} /> {t('stepWorkspace.undoLastAction')}
            </button>
            <button className="btn-danger flex justify-center items-center gap-2 py-2" onClick={resetWorkout}>
              <RotateCcw size={18} /> {t('stepWorkspace.restartSession')}
            </button>
          </div>
        </div>

        {/* Right Column: Recommendations */}
        <div className="flex flex-col md:pl-6 pt-6 md:pt-0 h-full min-h-0">
          <h2 className="text-xl font-bold text-slate-800 mb-4 shrink-0">{t('stepWorkspace.aiNextStepGeneration')}</h2>
          
          {state.is_loading ? (
            <div className="flex justify-center p-12">
              <Loader2 className="animate-spin text-primary-500" size={40} />
            </div>
          ) : (
            <div className="flex flex-col gap-3 flex-1 min-h-0 overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-slate-200">
              {state.recommendations.map((rec, i) => (
                <div 
                  key={i} 
                  className="flex justify-between items-center p-3 bg-white rounded-xl border border-slate-200 
                             shadow-sm hover:shadow-md hover:border-primary-300 transition-all cursor-pointer 
                             group animate-fade-in"
                  onClick={() => addExercise(rec.exercise_id, rec.exercise_name, rec.translated_name, rec.equipment)}
                >
                  <span className="text-base font-bold text-slate-700 group-hover:text-primary-700 transition-colors">{rec.translated_name}</span>
                  <span className="px-2 py-0.5 text-xs font-semibold bg-slate-100 text-slate-500 rounded-md">
                    {t(`options.equipments.${rec.equipment}`, rec.equipment)}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default StepWorkspace;
