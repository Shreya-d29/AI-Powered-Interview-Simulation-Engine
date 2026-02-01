<<<<<<< HEAD
# AI-Powered-Interview-Simulation-Engine
=======
# Hack2Hire Elite: The Ultimate AI Interview Engine 🏆

Hack2Hire Elite is a production-grade, stateful interview evaluation engine designed for high-stakes technical assessments and hackathon-winning demos. It moves away from "black-box" LLM guessing and delivers a **Deterministic Decision Core** where every score, state change, and penalty is traceable, reproducible, and explainable.

---

## 🚀 Key Features (Jury Checkpoints)

### 🧠 1. Explicit State Machine
The engine strictly manages interview states:
- `NOT_STARTED` -> `IN_PROGRESS` -> `ADAPTIVE_MODE` -> `EARLY_TERMINATED` or `COMPLETED`.
- Every transition is logic-driven and recorded in the **Decision Trace**.

### ⚖️ 2. Deterministic Scoring Engine
No randomness. No black-box ML. Scores are calculated using a transparent formula:
- **Accuracy (40%)**: Verified via keyword density and technical depth.
- **Relevance (20%)**: Technical vocabulary and context alignment.
- **Clarity (20%)**: Professionalism and **Filler Word Detection** (filters "um", "like", "basically").
- **Time Efficiency (20%)**: Response time modeling with **Warning Zone** alerts (<10s).

### 📈 3. Adaptive Difficulty & Seniority
- **Entry Logic**: Senior/Lead profiles start at higher difficulty levels automatically.
- **Ramp Logic**: Consecutive strong answers elevate difficulty; weak answers stabilize or reduce it to find the candidate's true ceiling.

### 🔍 4. Decision Trace & Transparency
A dedicated "Live Engine Internals" log records every internal decision. This proves "AI Reasoning" by showing why difficulty changed or why an interview was terminated early.

### 👔 5. Elite Career Dashboard
- **Hiring Readiness**: Professional mapping (Hire Ready, Borderline, Not Ready).
- **Engine Confidence Score**: A consistency metric measuring candidate stability.
- **Skill Radar**: Multi-dimensional analysis of performance across different technical domains.
- **Chronological Timeline**: Step-by-step history of questions, scores, and feedback.

---

## 🛠️ Tech Stack

- **Core Engine**: Python 3.x
- **Schema & Validation**: Pydantic
- **Frontend**: Streamlit (Glassmorphism 2.0 Aesthetic)
- **Data Visualization**: Plotly (Gauge, Radar, and Timeline charts)

---

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Hackfire
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

---

## 🧠 Decision Logic (For Judges)

### Adaptive Thresholds
- **Promotion**: 2 consecutive scores > 80% -> Difficulty ↑
- **Demotion**: 2 consecutive scores < 40% -> Difficulty ↓
- **Early Termination**:
    - Average Score < 35% (Configurable)
    - 2 consecutive failures (<20% score)

### Time Modeling
- **Bonus**: +5.0pts for Accuracy > 80% and Time < 50% of limit.
- **Penalty**: -2.0% per second exceeded beyond the limit.

---

## 🛡️ Edge Case Handling
- **Filler Word Detection**: Penalizes non-professional linguistic fillers.
- **Empty Answers**: Detected and scored as 0 with specific feedback.
- **Fast Guessing**: Protection against "too fast" responses with low keyword density.

---
**Hack2Hire Elite** - *Engineering Intelligence for the Next Generation of Hiring.* 🚀
>>>>>>> 0165c7f (Initial commit: Hack2Hire Elite AI Interview Engine)
