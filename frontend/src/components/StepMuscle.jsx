import React from 'react';

const StepMuscle = ({ prevStep, startWorkout }) => {
  return (
    <div className="glass-card">
      <div style={{ marginBottom: '2rem', textAlign: 'center' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 600, color: '#0f172a' }}>
          Profile configured successfully!
        </h2>
        <p style={{ color: '#64748b', marginTop: '0.5rem' }}>
          ML pipeline is ready. Choose your first exercise.
        </p>
      </div>

      <h3 style={{ fontSize: '1.125rem', marginBottom: '1rem', color: '#0f172a' }}>
        Select Initial Muscle Group
      </h3>
      
      <div className="step-buttons">
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(15, "Bench Press (Barbell)", "Barbell")}
        >
          Chest (Bench Press)
        </button>
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(5, "Squat (Barbell)", "Barbell")}
        >
          Legs (Squat)
        </button>
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(720, "Deadlift (Barbell)", "Barbell")}
        >
          Back (Deadlift)
        </button>
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(1778, "Overhead Press (Barbell)", "Barbell")}
        >
          Shoulders (OHP)
        </button>
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(363, "Bicep Curl (Dumbbell)", "Dumbbell")}
        >
          Arms (Bicep Curl)
        </button>
        <button 
          className="btn muscle-btn"
          onClick={() => startWorkout(130, "Abs Crunch (Bodyweight)", "Bodyweight")}
        >
          Core (Abs Crunch)
        </button>
      </div>

      <div style={{ marginTop: '2rem', display: 'flex' }}>
        <button className="btn btn-outline" onClick={prevStep}>
          Back to Stats
        </button>
      </div>
    </div>
  );
};

export default StepMuscle;
