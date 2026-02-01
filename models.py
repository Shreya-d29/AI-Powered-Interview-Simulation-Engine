from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class InterviewStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    ADAPTIVE_MODE = "ADAPTIVE_MODE"
    EARLY_TERMINATED = "EARLY_TERMINATED"
    COMPLETED = "COMPLETED"

class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Question(BaseModel):
    id: str
    skill: str
    difficulty: Difficulty
    question_text: str
    expected_keywords: List[str] = []
    time_limit: int = 60  # seconds

class CandidateProfile(BaseModel):
    name: str
    experience_level: str
    skills: List[str]

class JobDescription(BaseModel):
    role_type: str = "Tech"
    required_skills: List[str]
    difficulty_expectation: Difficulty

class InterviewConfig(BaseModel):
    max_questions: int = 5
    early_termination_threshold_count: int = 2
    min_score_threshold: float = 30.0
    ramp_rate: float = 1.0 # Multiplier for difficulty shifts

class Response(BaseModel):
    question_id: str
    answer: str
    time_taken: float
    is_timeout: bool = False

class ScoreBreakdown(BaseModel):
    accuracy: float
    relevance: float
    clarity: float
    time_efficiency: float
    overall: float
    bonus: float = 0.0

class QuestionResult(BaseModel):
    question: Question
    response: Response
    score: ScoreBreakdown
    state_at_time: InterviewStatus
    difficulty_at_time: Difficulty
    feedback: str

class InterviewResult(BaseModel):
    final_score: float
    hiring_readiness: str # "Hire Ready", "Borderline", "Not Ready"
    readiness_category: str # "Strong", "Average", "Needs Improvement"
    confidence_score: float # Consistency metric
    skill_breakdown: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    status: InterviewStatus
    termination_reason: Optional[str] = None
    timeline: List[QuestionResult] = []
