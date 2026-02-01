import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from models import (
    CandidateProfile, JobDescription, InterviewConfig, 
    Difficulty, InterviewStatus
)
from engine import InterviewEngine

# --- PAGE CONFIG ---
st.set_page_config(page_title="Hack2Hire Elite - AI Interview Simulation", layout="wide", page_icon="👔")

# --- CUSTOM CSS (Elite Career Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #1e293b 0%, #0f172a 100%);
    }
    
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        letter-spacing: -2px;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 2.5rem;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        border: 1px solid rgba(96, 165, 250, 0.3);
    }
    
    .timeline-item {
        border-left: 2px solid #60a5fa;
        padding-left: 20px;
        margin-bottom: 20px;
        position: relative;
    }
    
    .timeline-dot {
        position: absolute;
        left: -6px;
        top: 0;
        width: 10px;
        height: 10px;
        background: #60a5fa;
        border-radius: 50%;
    }
    
    .log-container {
        font-family: 'JetBrains Mono', monospace;
        background: #020617;
        color: #10b981;
        padding: 1.5rem;
        border-radius: 16px;
        font-size: 0.85rem;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #1e293b;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
    }
    
    .engine-thinking {
        color: #60a5fa;
        font-weight: 600;
        letter-spacing: 1px;
        animation: blink 1.5s infinite;
    }
    
    @keyframes blink {
        0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; }
    }
    
    .timer-warning {
        color: #ef4444;
        animation: shake 0.5s infinite;
        font-weight: 800;
    }
    
    @keyframes shake {
        0% { transform: translateX(0); }
        25% { transform: translateX(2px); }
        50% { transform: translateX(0); }
        75% { transform: translateX(-2px); }
        100% { transform: translateX(0); }
    }
    
    .stat-badge {
        background: rgba(96, 165, 250, 0.1);
        color: #60a5fa;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'engine' not in st.session_state:
    st.session_state.engine = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'interview_finished' not in st.session_state:
    st.session_state.interview_finished = False

# --- HEADER SECTION ---
st.markdown('<h1 class="main-header">Hack2Hire Elite 💼</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; font-size: 1.2rem; font-weight: 500; margin-top: -10px;">Deterministic Executive Performance Engine</p>', unsafe_allow_html=True)

# --- SIDEBAR: CAREER SETTINGS ---
with st.sidebar:
    st.markdown("### 👨‍� Candidate Context")
    name = st.text_input("Candidate Name", "Alex Rivera")
    exp = st.selectbox("Seniority Level", ["Entry", "Mid-Level", "Senior", "Lead"])
    resume_skills = st.multiselect("Resume Key Skills", ["Python", "System Design", "Data Structures", "Cloud", "Java"], default=["Python", "System Design"])
    
    st.markdown("---")
    st.markdown("### 🏢 Job Specification")
    role = st.text_input("Target Role", "L6 Software Engineer")
    jd_skills = st.multiselect("Mandatory Skills (JD)", ["Python", "System Design", "Databases", "Security"], default=["Python", "System Design"])
    
    st.markdown("---")
    st.markdown("### ⚙️ Engine Parameters")
    with st.expander("Advanced Configuration"):
        max_q = st.slider("Max Q", 3, 10, 5)
        term_fail = st.slider("Strict Terminate (Fails)", 1, 3, 2)
        ramp_rate = st.select_slider("Ramp Rate", options=[0.5, 1.0, 1.5], value=1.0)
        min_threshold = st.slider("Min Avg Score (%)", 20, 50, 35)

    if st.button("🏁 Launch Simulation", use_container_width=True):
        candidate = CandidateProfile(name=name, experience_level=exp, skills=resume_skills)
        jd = JobDescription(role_type="Tech", required_skills=jd_skills, difficulty_expectation=Difficulty.MEDIUM)
        config = InterviewConfig(max_questions=max_q, early_termination_threshold_count=term_fail, min_score_threshold=min_threshold, ramp_rate=ramp_rate)
        
        st.session_state.engine = InterviewEngine(candidate, jd, config)
        st.session_state.interview_started = True
        st.session_state.interview_finished = False
        st.session_state.current_question = st.session_state.engine.start_interview()
        st.session_state.start_time = time.time()
        st.rerun()

# --- MAIN INTERFACE ---
if not st.session_state.interview_started:
    # Landing View
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown("""
        <div class="glass-card">
            <h2 style="color: #f472b6;">Why Deterministic? 🤔</h2>
            <p style="color: #94a3b8;">Unlike probabilistic LLMs that guess, Hack2Hire uses a <b>Decision Trace Engine</b>. Every score is a result of explicit rules and state transitions.</p>
            <div style="margin-top: 20px;">
                <span class="stat-badge">⚖️ Weighted Scoring</span>
                <span class="stat-badge">🔄 State Machine</span>
                <span class="stat-badge">📉 Adaptive Logic</span>
                <span class="stat-badge">📝 Traceable logs</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_r:
        st.markdown("""
        <div class="glass-card">
            <h2 style="color: #60a5fa;">The Judging Standard 🏆</h2>
            <ul style="color: #94a3b8; font-size: 0.95rem;">
                <li><b>Visibility:</b> See how the engine "thinks" in the Live Internals.</li>
                <li><b>Predictability:</b> Same answer always yields the same score.</li>
                <li><b>Complexity:</b> Handles seniority modeling and linguistic filler detection.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.interview_finished:
    # --- RESULT DASHBOARD ---
    result = st.session_state.engine.generate_final_report()
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"# {result.hiring_readiness}")
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        # Gauge for Score
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = result.final_score,
            title = {'text': "Readiness Score (%)"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#60a5fa"}}
        ))
        fig.update_layout(height=250, margin=dict(t=30, b=0, l=30, r=30), paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        # Confidence Metric
        st.markdown(f"### 🤝 Engine Confidence")
        st.metric("Score Consistency", f"{result.confidence_score:.1f}%")
        st.info("High consistency signals a stable candidate profile.")
        
    with c3:
        st.markdown(f"### 🚩 System Status")
        st.markdown(f"State: <span class='status-badge status-{result.status.value.lower().replace('_', '-')}'>{result.status}</span>", unsafe_allow_html=True)
        if result.termination_reason:
            st.error(f"🛑 Terminated: {result.termination_reason}")
            
    st.markdown("---")
    
    t1, t2 = st.tabs(["📊 Performance Matrix", "🧭 Chronological Timeline"])
    
    with t1:
        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown("### 🕸️ Skill Radar")
            df_radar = pd.DataFrame(list(result.skill_breakdown.items()), columns=['Skill', 'Score'])
            fig_r = px.line_polar(df_radar, r='Score', theta='Skill', line_close=True)
            fig_r.update_traces(fill='toself', line_color='#f472b6', marker=dict(size=8))
            fig_r.update_layout(paper_bgcolor='rgba(0,0,0,0)', polar=dict(bgcolor='rgba(0,0,0,0)'), font_color='white')
            st.plotly_chart(fig_r, use_container_width=True)
        with cc2:
            st.markdown("### 🏗️ Analysis")
            st.success("✅ **Strengths:** " + ", ".join(result.strengths if result.strengths else ["None detected"]))
            st.warning("⚠️ **Gaps:** " + ", ".join(result.weaknesses if result.weaknesses else ["None detected"]))
            st.markdown("#### � Next Steps")
            for s in result.suggestions: st.write(f"- {s}")
            
    with t2:
        st.markdown("### 📅 Interview Decision History")
        for i, res in enumerate(result.timeline):
            st.markdown(f"""
            <div class="timeline-item">
                <div class="timeline-dot"></div>
                <b>STEP {i+1}: {res.question.skill} ({res.difficulty_at_time.value.upper()})</b><br>
                <small style="color: #64748b;">Score: {res.score.overall:.1f}% | Time: {res.response.time_taken:.1f}s | State: {res.state_at_time}</small><br>
                <p style="margin-top: 5px; font-size: 0.9rem;">"{res.feedback}"</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 🔍 Root Cause / Decision Trace")
    log_html = "<br>".join(st.session_state.engine.engine_logs)
    st.markdown(f'<div class="log-container">{log_html}</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Reset System"):
        st.session_state.interview_started = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- LIVE INTERVIEW ---
    engine = st.session_state.engine
    q = st.session_state.current_question
    
    if q is None:
        st.session_state.interview_finished = True
        st.rerun()

    current_idx = engine.current_question_index + 1
    total_q = engine.config.max_questions
    
    col_p, col_st = st.columns([3, 1])
    with col_p:
        st.progress(engine.current_question_index / total_q)
    with col_st:
        st.markdown(f"<span class='stat-badge'>STEP {current_idx} OF {total_q}</span>", unsafe_allow_html=True)

    # Main Question UI
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: top;">
            <div>
                <span style="color: #60a5fa; font-weight: 800; text-transform: uppercase;">Category: {q.skill}</span>
                <h1 style="margin-top: 5px; font-size: 2.5rem;">{q.question_text}</h1>
            </div>
            <div style="text-align: right;">
                <span class='stat-badge'>{q.difficulty.value.upper()}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Form
    with st.form("answer_form", clear_on_submit=True):
        st.markdown("<p class='engine-thinking'>⚙️ ENGINE IS MONITORING ARTICULATION...</p>", unsafe_allow_html=True)
        ans = st.text_area("Candidate Response", placeholder="Provide a structured technical explanation...", height=300)
        cbtn, cmsg = st.columns([1, 3])
        with cbtn:
            submitted = st.form_submit_button("⏩ Submit Response")
        with cmsg:
            st.markdown(f"<p style='margin-top: 10px; color: #64748b;'>Engine state: <b>{engine.state.value}</b></p>", unsafe_allow_html=True)
            
        if submitted:
            time_spent = time.time() - st.session_state.start_time
            st.session_state.current_question = engine.process_response(q, ans, time_spent)
            st.session_state.start_time = time.time()
            if st.session_state.current_question is None:
                st.session_state.interview_finished = True
            st.rerun()

    # Dynamic Timer Logic
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, q.time_limit - elapsed)
    
    tc1, tc2 = st.columns([4, 1])
    with tc1:
        st.progress(min(1.0, elapsed/q.time_limit))
    with tc2:
        if remaining <= 10 and remaining > 0:
            st.markdown(f"<p class='timer-warning'>⚠️ {int(remaining)}s</p>", unsafe_allow_html=True)
        elif remaining == 0:
            st.markdown("<p class='timer-warning'>⏱️ TIME EXCEEDED</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color: #64748b; font-weight: 700;'>⏱️ {int(remaining)}s</p>", unsafe_allow_html=True)

    with st.expander("🛠️ Decision Trace (BETA)"):
        st.markdown('<p style="font-family: Courier; color: #10b981;">Engine internal logs are generated on every transition.</p>', unsafe_allow_html=True)
        log_h = "<br>".join(engine.engine_logs)
        st.markdown(f'<div class="log-container">{log_h}</div>', unsafe_allow_html=True)
        
    if st.button("⏹️ Manual Override / Terminate"):
        engine.state = InterviewStatus.EARLY_TERMINATED
        engine.termination_reason = "Overridden by supervisor."
        st.session_state.interview_finished = True
        st.rerun()
