import React from 'react';
import { Trash2, RotateCcw, Undo2, Loader2 } from 'lucide-react';

const StepWorkspace = ({ state, resetWorkout, undoLastExercise, addExercise }) => {
  return (
    <div className="glass-card" style={{ marginBottom: '2rem' }}>
      <div className="workspace-grid">
        {/* Left Column: Trajectory */}
        <div>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>Current Trajectory</h2>
          
          <div className="glass-card-sm">
            <div className="trajectory-list">
              {state.history_names.map((name, index) => {
                const isLast = index === state.history_names.length - 1;
                return (
                  <div key={index} className="trajectory-item">
                    <span style={{ fontWeight: 500 }}>
                      <span style={{ color: '#64748b', marginRight: '0.5rem' }}>{index + 1}.</span>
                      {name}
                    </span>
                    {isLast && (
                      <button 
                        className="btn btn-ghost-danger" 
                        style={{ padding: '0.25rem' }}
                        onClick={undoLastExercise}
                        title="Undo this exercise"
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
            <div className="ai-prediction">
              <div className="ai-prediction-label">AI Target Prediction</div>
              <div className="ai-prediction-value">{state.current_prediction}</div>
            </div>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginTop: '1.5rem' }}>
            <button className="btn btn-outline" onClick={undoLastExercise} style={{ width: '100%' }}>
              <Undo2 size={18} /> Undo Last Action
            </button>
            <button className="btn btn-danger" onClick={resetWorkout} style={{ width: '100%' }}>
              <RotateCcw size={18} /> Restart Session
            </button>
          </div>
        </div>

        {/* Right Column: Recommendations */}
        <div style={{ paddingLeft: '2rem', borderLeft: '1px solid #e2e8f0' }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>AI Next Step Generation</h2>
          
          {state.is_loading ? (
            <div style={{ display: 'flex', justifyContent: 'center', padding: '3rem' }}>
              <Loader2 className="spinner" size={40} color="#0ea5e9" />
            </div>
          ) : (
            <div className="recommendation-list">
              {state.recommendations.map((rec, i) => (
                <div 
                  key={i} 
                  className="recommendation-card"
                  onClick={() => addExercise(rec.exercise_id, rec.exercise_name, rec.equipment)}
                >
                  <span style={{ fontSize: '1.125rem', fontWeight: 600 }}>{rec.exercise_name}</span>
                  <span className="badge">{rec.equipment}</span>
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
