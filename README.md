<div align="center">
  <h1>Gym Brain</h1>
  <p><b>Two-Stage Recommender System for Fitness Workouts</b></p>
  
  <br />

  <p>
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React"/>
    <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" alt="Vite"/>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
    <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch"/>
    <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  </p>

  <br />

  <!-- PLACEHOLDER FOR VIDEO: Once you record a video, we will replace this image with:
  <video src="docs/demo.mp4" autoplay loop muted width="800" style="border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);"></video> -->
  
</div>

<hr/>

**Gym Brain** is a smart, AI-powered fitness assistant that generates highly personalized workout plans on the fly. It leverages a three-stage Machine Learning pipeline to analyze your profile, biological stats, and equipment availability to predict your optimal next exercise, including dynamic targets (weight, reps, or time).

<br />

## Key Features

- **Interactive Wizard UI**: Step-by-step workout initialization gathering biological stats, available equipment, and 1RM metrics.
- **Dynamic Contextual Predictions**: Generates target metrics formatted based on exercise type (e.g., rep ranges for hypertrophy vs strength).
- **Data Validation**: Real-time client-side and backend validation to prevent dirty or illogical inputs.
- **Workout Trajectory Engine**: Auto-scrollable session workspace with Undo and Restart features for seamless in-gym usage.

<br />

## How to Run Locally

1. **Clone the Repository**
```bash
git clone https://github.com/AMarikDS/gym-brain.git
cd gym-brain
```

2. **Start Services (Docker Compose)**
```bash
# Optional: If you are behind a corporate proxy, you must export it first:
# export HTTP_PROXY=... HTTPS_PROXY=...

docker compose up --build -d
```

3. **Access the App**
- **Web Interface:** [http://localhost:3001](http://localhost:3001)
- **API Documentation:** [http://localhost:8001/docs](http://localhost:8001/docs)

<br />

## Pipeline Architecture

This project follows a microservices architecture powered by a 3-stage Machine Learning pipeline optimized for low-latency inference.

### 1. Candidate Generation
- **Model**: TransformerRec (BERT architecture).
- **Format**: C++ TorchScript JIT (`.pt`).
- **Input**: Sequence of past exercise IDs.
- **Output**: Top-N potential next exercises scored by contextual relevance.

### 2. Reranking
- **Model**: CatBoost Ranker.
- **Format**: Native C++ CatBoost Binary (`.cbm`).
- **Input**: User profile and candidate exercises.
- **Output**: Re-ranked list of exercises sorted by personalized relevance score.

### 3. Target Regression
- **Model**: CatBoost Regressor.
- **Format**: Native C++ CatBoost Binary (`.cbm`).
- **Input**: Selected exercise and user profile.
- **Output**: Predicted optimal dynamic target (weight, reps, or time).

<br />

## BigTech & Highload Inference (Triton, TensorRT, JIT)

The project implements a **C++ TorchScript (JIT)** inference engine for the Transformer, simulating BigTech standards (e.g., Triton Inference Server).

### Why not pure PyTorch?
Standard PyTorch carries significant overhead due to the Python GIL (Global Interpreter Lock) and dynamic computation graphs. This is unacceptable for production-ready 1000+ RPS architectures. We compiled the PyTorch model into **TorchScript (JIT)**, allowing it to run entirely in a C++ environment (LibTorch) without Python overhead.

### Inference Technologies (Production Stack)
1. **TorchScript JIT (Implemented):** Compiles the model into a static graph for C++ or Rust execution. Speeds up inference on CPU/GPU and serves as a native backend for **NVIDIA Triton Inference Server**.
2. **ONNX Runtime:** Microsoft's universal C++ engine, often providing maximum CPU performance via aggressive graph optimization.
3. **TensorRT:** NVIDIA's proprietary engine. Optimizes weights for specific chip architectures (e.g., T4, A100) and quantizes to FP16/INT8 for maximum GPU FPS.
4. **Triton Inference Server & Kubernetes:** In BigTech, models aren't wrapped directly in FastAPI. Instead, they are deployed to Triton, which handles gRPC requests, dynamic batching, and 100% GPU utilization, orchestrated by K8s.

### Benchmark (1000 requests)
Our load testing demonstrated significant **Business Impact** from model compilation:
* **PyTorch (Python):** p99 Latency = `4.023 ms` | Mean = `2.556 ms`
* **C++ JIT (LibTorch):** p99 Latency = `2.546 ms` | Mean = `2.183 ms`

**Business Impact:** The C++ engine proved to be **1.6x faster** at the 99th percentile (p99). This radically reduces hardware resource consumption and guarantees stable response times during traffic spikes (highload).

<br />

## Project Structure

- `models/` - Machine learning weights and mappings.
- `backend/` - FastAPI application and ML inference service.
- `frontend/` - React SPA with Nginx reverse proxy.
- `notebooks/` - Jupyter notebooks for model training and data exploration.
