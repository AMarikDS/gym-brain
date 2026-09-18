import React from 'react';
import Alert from './Alert';

const StepBio = ({ state, setState, nextStep, error }) => {
  return (
    <div className="glass-card">
      <h2 style={{ marginBottom: '1.5rem' }}>Step 1: Biological Profile</h2>
      
      <div className="form-grid">
        <div className="form-group">
          <label>Level</label>
          <select 
            value={state.level} 
            onChange={(e) => setState({ ...state, level: e.target.value })}
          >
            <option>Novice</option>
            <option>Beginner</option>
            <option>Intermediate</option>
            <option>Advanced</option>
          </select>
        </div>

        <div className="form-group">
          <label>Goal</label>
          <select 
            value={state.goal} 
            onChange={(e) => setState({ ...state, goal: e.target.value })}
          >
            <option>Bodybuilding</option>
            <option>Powerlifting</option>
            <option>Powerbuilding</option>
            <option>Athletics</option>
            <option>General Fitness</option>
          </select>
        </div>

        <div className="form-group">
          <label>Sex</label>
          <select 
            value={state.sex} 
            onChange={(e) => setState({ ...state, sex: e.target.value })}
          >
            <option>Male</option>
            <option>Female</option>
          </select>
        </div>

        <div className="form-group">
          <label>Age</label>
          <input 
            type="number" 
            min="10" 
            max="120"
            value={state.age} 
            onChange={(e) => setState({ ...state, age: e.target.value })}
          />
        </div>

        <div className="form-group full-width">
          <label>Bodyweight (kg)</label>
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
          Next Step
        </button>
      </div>
    </div>
  );
};

export default StepBio;
