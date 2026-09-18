import React from 'react';
import Alert from './Alert';

const StepStats = ({ state, setState, nextStep, prevStep, error }) => {
  return (
    <div className="glass-card">
      <h2 style={{ marginBottom: '1.5rem' }}>Step 2: Equipment & Base Strength</h2>
      
      <div className="form-grid">
        <div className="form-group">
          <label>Available Equipment</label>
          <select 
            value={state.equipment} 
            onChange={(e) => setState({ ...state, equipment: e.target.value })}
          >
            <option>All (Gym Mixed)</option>
            <option>Barbell</option>
            <option>Dumbbell</option>
            <option>Machine</option>
            <option>Cable</option>
            <option>Bodyweight</option>
            <option>Cardio</option>
          </select>
        </div>

        <div className="form-group">
          <label>Squat 1RM (kg)</label>
          <input 
            type="number" 
            min="0"
            value={state.squat} 
            onChange={(e) => setState({ ...state, squat: e.target.value })}
          />
        </div>

        <div className="form-group">
          <label>Bench 1RM (kg)</label>
          <input 
            type="number" 
            min="0"
            value={state.bench} 
            onChange={(e) => setState({ ...state, bench: e.target.value })}
          />
        </div>

        <div className="form-group">
          <label>Deadlift 1RM (kg)</label>
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
          Back
        </button>
        <button className="btn btn-primary" onClick={nextStep}>
          Review Profile
        </button>
      </div>
    </div>
  );
};

export default StepStats;
