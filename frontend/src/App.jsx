import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import StepBio from './components/StepBio'
import StepStats from './components/StepStats'
import StepMuscle from './components/StepMuscle'
import StepWorkspace from './components/StepWorkspace'
import LanguageSwitcher from './components/LanguageSwitcher'

function App() {
  const { t, i18n } = useTranslation();

  const [state, setState] = useState(() => {
    const savedState = localStorage.getItem('gymBrainState');
    if (savedState) {
      try {
        return JSON.parse(savedState);
      } catch (e) {
        console.error("Failed to parse saved state", e);
      }
    }
    return {
      current_step: 1,
      level: "Intermediate",
      goal: "Bodybuilding",
      sex: "Male",
      age: "25",
      bw: "80",
      equipment: "All (Gym Mixed)",
      squat: "0",
      bench: "0",
      deadlift: "0",
      history_ids: [],
      history_names: [], // stores display names (localized)
      recommendations: [],
      current_prediction: "",
      is_loading: false
    };
  });

  useEffect(() => {
    localStorage.setItem('gymBrainState', JSON.stringify(state));
  }, [state]);

  const [error, setError] = useState("");

  const nextStep = () => {
    setError("");
    if (state.current_step === 1) {
      const ageVal = parseFloat(state.age);
      if (isNaN(ageVal) || ageVal < 12 || ageVal > 100) {
        setError(t('errors.invalidAge'));
        return;
      }
      const bwVal = parseFloat(state.bw);
      if (isNaN(bwVal) || bwVal < 30 || bwVal > 300) {
        setError(t('errors.invalidBodyweight'));
        return;
      }
    } else if (state.current_step === 2) {
      const lifts = [
        { name: "Squat", val: state.squat },
        { name: "Bench", val: state.bench },
        { name: "Deadlift", val: state.deadlift }
      ];
      for (let lift of lifts) {
        const val = parseFloat(lift.val);
        if (isNaN(val) || val < 0 || val > 500) {
          setError(t('errors.invalid1RM', { lift: lift.name }));
          return;
        }
      }
    }

    if (state.current_step < 4) {
      setState(prev => ({ ...prev, current_step: prev.current_step + 1 }));
    }
  };

  const prevStep = () => {
    setError("");
    if (state.current_step > 1) {
      setState(prev => ({ ...prev, current_step: prev.current_step - 1 }));
    }
  };

  const buildProfile = () => ({
    sex: state.sex,
    age: Math.max(10.0, Math.min(120.0, parseFloat(state.age) || 25.0)),
    bw: Math.max(20.0, Math.min(300.0, parseFloat(state.bw) || 80.0)),
    level: state.level,
    goal: state.goal,
    equipment: state.equipment,
    sbd: [
      parseFloat(state.squat || 0.0),
      parseFloat(state.bench || 0.0),
      parseFloat(state.deadlift || 0.0)
    ]
  });

  const getRecommendations = async (currentHistory) => {
    setState(prev => ({ ...prev, is_loading: true }));
    try {
      const response = await fetch('/api/v1/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          history_ids: currentHistory,
          profile: buildProfile(),
          top_k: 10,
          language: i18n.language
        })
      });
      if (response.ok) {
        const data = await response.json();
        setState(prev => ({ ...prev, recommendations: data.recommendations || [] }));
      }
    } catch (e) {
      console.error("Error fetching recommendations:", e);
    } finally {
      setState(prev => ({ ...prev, is_loading: false }));
    }
  };

  const startWorkout = async (first_ex_id, first_ex_name_en, first_ex_name_local, raw_eq) => {
    const newHistoryIds = [first_ex_id];
    const newHistoryNames = [first_ex_name_local || first_ex_name_en];

    setState(prev => ({
      ...prev,
      history_ids: newHistoryIds,
      history_names: newHistoryNames,
      current_prediction: t('stepWorkspace.calculating'),
      current_step: 4
    }));

    try {
      const response = await fetch('/api/v1/predict_weight', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          profile: buildProfile(),
          exercise_name: first_ex_name_en,
          raw_equipment: raw_eq,
          language: i18n.language
        })
      });
      if (response.ok) {
        const data = await response.json();
        setState(prev => ({ ...prev, current_prediction: data.target_text || "" }));
      }
    } catch (e) {
      console.error("Error predicting weight:", e);
      setState(prev => ({ ...prev, current_prediction: "" }));
    }

    await getRecommendations(newHistoryIds);
  };

  const addExercise = async (ex_id, ex_name_en, ex_name_local, raw_eq) => {
    const newHistoryIds = [...state.history_ids, ex_id];
    const newHistoryNames = [...state.history_names, ex_name_local || ex_name_en];

    setState(prev => ({
      ...prev,
      history_ids: newHistoryIds,
      history_names: newHistoryNames,
    }));

    try {
      const response = await fetch('/api/v1/predict_weight', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          profile: buildProfile(),
          exercise_name: ex_name_en,
          raw_equipment: raw_eq,
          language: i18n.language
        })
      });
      if (response.ok) {
        const data = await response.json();
        setState(prev => ({ ...prev, current_prediction: data.target_text || "" }));
      }
    } catch (e) {
      console.error("Error predicting weight:", e);
    }

    await getRecommendations(newHistoryIds);
  };

  const undoLastExercise = async () => {
    if (state.history_ids.length === 0) return;

    if (state.history_ids.length === 1) {
      resetWorkout();
      return;
    }

    const newHistoryIds = state.history_ids.slice(0, -1);
    const newHistoryNames = state.history_names.slice(0, -1);

    setState(prev => ({
      ...prev,
      history_ids: newHistoryIds,
      history_names: newHistoryNames,
      current_prediction: t('stepWorkspace.recalculating')
    }));

    await getRecommendations(newHistoryIds);
  };

  const resetWorkout = () => {
    setState(prev => ({
      ...prev,
      history_ids: [],
      history_names: [],
      recommendations: [],
      current_prediction: "",
      current_step: 3
    }));
  };

  return (
    <div className="min-h-screen flex flex-col items-center py-12 px-4 relative">
      <LanguageSwitcher />
      
      <div className="text-center mb-10 max-w-2xl">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-primary-600 mb-4 animate-fade-in">
          {t('app.title')}
        </h1>
        <p className="text-lg text-slate-500 font-medium">
          {t('app.subtitle')}
        </p>
      </div>

      <div className={`w-full transition-all duration-500 ease-in-out ${state.current_step === 4 ? 'max-w-5xl' : 'max-w-xl'} animate-fade-in`}>
      {state.current_step === 1 && (
        <StepBio state={state} setState={setState} nextStep={nextStep} error={error} />
      )}
      {state.current_step === 2 && (
        <StepStats state={state} setState={setState} nextStep={nextStep} prevStep={prevStep} error={error} />
      )}
      {state.current_step === 3 && (
        <StepMuscle prevStep={prevStep} startWorkout={startWorkout} />
      )}
      {state.current_step === 4 && (
        <StepWorkspace
          state={state}
          resetWorkout={resetWorkout}
          undoLastExercise={undoLastExercise}
          addExercise={addExercise}
        />
      )}
      </div>
      
      <footer className="mt-auto pt-16 pb-4 text-center text-sm text-slate-400 font-medium">
        Gym Brain AI v1.0.0 • © 2026 Artem Markov
      </footer>
    </div>
  )
}

export default App
