import time
import random
from typing import List, Dict, Optional
from models import (
    InterviewStatus, Difficulty, Question, Response, 
    ScoreBreakdown, QuestionResult, InterviewResult,
    CandidateProfile, JobDescription, InterviewConfig
)
from question_bank import QUESTION_BANK, get_questions_by_difficulty

class InterviewEngine:
    def __init__(
        self, 
        candidate: CandidateProfile, 
        jd: JobDescription, 
        config: InterviewConfig
    ):
        self.candidate = candidate
        self.jd = jd
        self.config = config
        
        self.state = InterviewStatus.NOT_STARTED
        
        # FEATURE: Seniority-based entry difficulty
        if candidate.experience_level in ["Senior", "Lead"]:
            self.current_difficulty = Difficulty.MEDIUM
        else:
            self.current_difficulty = Difficulty.EASY
            
        self.history: List[QuestionResult] = []
        self.engine_logs: List[str] = [
            f"🚀 System initialized at {time.strftime('%H:%M:%S')}.",
            f"📌 Mode: STATEFUL_INTERVIEW_ENGINE",
            f"👤 Profile: {candidate.name} ({candidate.experience_level})",
            f"🎯 Target Skills: {', '.join(jd.required_skills)}",
            f"⚖️ Initial Difficulty: {self.current_difficulty.value.upper()}"
        ]
        self.current_question_index = 0
        self.consecutive_strong_answers = 0
        self.consecutive_weak_answers = 0
        self.total_score_sum = 0
        self.termination_reason = None
        
    def start_interview(self):
        self.state = InterviewStatus.IN_PROGRESS
        self.engine_logs.append(f"🏁 Interview Started. State transition: NOT_STARTED -> IN_PROGRESS")
        return self.next_question()

    def select_appropriate_questions(self) -> List[Question]:
        """FEATURE: Resume-to-JD Skill Alignment logic"""
        # Weighted skill list: Combine JD required skills and Candidate's resume skills
        relevant_skills = list(set(self.jd.required_skills) & set(self.candidate.skills))
        if not relevant_skills:
            relevant_skills = self.jd.required_skills
            
        available = [q for q in QUESTION_BANK if q.difficulty == self.current_difficulty]
        # Prioritize questions matching the overlapping skills
        prioritized = [q for q in available if q.skill in relevant_skills]
        
        return prioritized if prioritized else available

    def next_question(self) -> Optional[Question]:
        if self.state not in [InterviewStatus.IN_PROGRESS, InterviewStatus.ADAPTIVE_MODE]:
            return None
            
        prioritized = self.select_appropriate_questions()
        
        asked_ids = [r.question.id for r in self.history]
        remaining = [q for q in prioritized if q.id not in asked_ids]
        
        if not remaining:
            # Fallback to any random question of same difficulty if prioritized pool is exhausted
            fallback_pool = [q for q in QUESTION_BANK if q.difficulty == self.current_difficulty and q.id not in asked_ids]
            if not fallback_pool:
                return None
            return random.choice(fallback_pool)
            
        return random.choice(remaining)

    def process_response(self, question: Question, user_answer: str, time_taken: float):
        self.engine_logs.append(f"📥 Processing Response for Q{self.current_question_index + 1}...")
        
        # FEATURE: Deterministic Scoring (Explainable)
        score_breakdown = self._evaluate_response(question, user_answer, time_taken)
        feedback = self._generate_rule_based_feedback(score_breakdown, question, user_answer)
        
        result = QuestionResult(
            question=question,
            response=Response(
                question_id=question.id,
                answer=user_answer,
                time_taken=time_taken,
                is_timeout=time_taken > question.time_limit
            ),
            score=score_breakdown,
            state_at_time=self.state,
            difficulty_at_time=self.current_difficulty,
            feedback=feedback
        )
        
        self.history.append(result)
        self.total_score_sum += score_breakdown.overall
        self.current_question_index += 1
        
        # Decision Trace Logs
        self.engine_logs.append(f"✅ Q{self.current_question_index} Evaluated. Overall Score: {score_breakdown.overall:.1f}%")
        self.engine_logs.append(f"   [Accuracy: {score_breakdown.accuracy:.1f}, Relevance: {score_breakdown.relevance:.1f}, Clarity: {score_breakdown.clarity:.1f}, Time: {score_breakdown.time_efficiency:.1f}]")
        if score_breakdown.bonus > 0:
            self.engine_logs.append(f"   🌟 BONUS: +{score_breakdown.bonus:.1f}pts for high-speed accuracy!")
            
        # Adaptive Logic
        self._apply_adaptive_rules(score_breakdown.overall)
        
        # Check for Early Termination
        if self._should_terminate():
            self.state = InterviewStatus.EARLY_TERMINATED
            self.engine_logs.append(f"⛔ State transition: IN_PROGRESS -> EARLY_TERMINATED. Reason: {self.termination_reason}")
            return None
            
        if self.current_question_index >= self.config.max_questions:
            self.state = InterviewStatus.COMPLETED
            self.engine_logs.append(f"🏁 State transition: {self.state.value} -> COMPLETED")
            return None
            
        return self.next_question()

    def _evaluate_response(self, question: Question, answer: str, time_taken: float) -> ScoreBreakdown:
        # 1. Accuracy (40%) - Keyword matching + Contextual presence
        found_keywords = [kw for kw in question.expected_keywords if kw.lower() in answer.lower()]
        accuracy_score = (len(found_keywords) / len(question.expected_keywords)) * 100 if question.expected_keywords else 80
        
        # 2. Relevance (20%) - Based on response length and technical vocabulary
        words = answer.lower().split()
        relevance_score = min(100, (len(words) / 20) * 100) if len(words) > 0 else 0
        
        # 3. Clarity (20%) - Professionalisms vs Filler Words
        filler_words = ["basically", "um", "ah", "like", "actually", "just"]
        filler_count = sum(1 for word in words if word in filler_words)
        clarity_score = max(0, 100 - (filler_count * 10))
        
        # 4. Time Efficiency (20%) - Penalty for overtime, Bonus for speed
        if time_taken <= 5: # Guessing protection
            eff_score = 10
        elif time_taken <= question.time_limit * 0.4:
            eff_score = 100
        elif time_taken <= question.time_limit:
            eff_score = 100 - ((time_taken / question.time_limit) * 30)
        else:
            eff_score = max(0, 50 - ((time_taken - question.time_limit) * 2))
            
        # FEATURE: Fast + Correct Bonus
        bonus = 0.0
        if accuracy_score > 80 and time_taken < question.time_limit * 0.5:
            bonus = 5.0
            
        overall = (accuracy_score * 0.4) + (relevance_score * 0.2) + (clarity_score * 0.2) + (eff_score * 0.2) + bonus
        overall = min(100, overall)
        
        return ScoreBreakdown(
            accuracy=accuracy_score,
            relevance=relevance_score,
            clarity=clarity_score,
            time_efficiency=eff_score,
            overall=overall,
            bonus=bonus
        )

    def _generate_rule_based_feedback(self, score: ScoreBreakdown, q: Question, answer: str) -> str:
        """FEATURE: Explainable Feedback Generator"""
        if len(answer.strip()) == 0:
            return "Empty response detected. Zero points awarded for this section."
            
        feedbacks = []
        if score.accuracy < 50:
            feedbacks.append(f"Low technical accuracy. Missing key concepts like {', '.join(q.expected_keywords[:2])}.")
        else:
            feedbacks.append("Strong technical alignment with expected keywords.")
            
        if score.clarity < 70:
            feedbacks.append("Usage of filler words detected. Work on professional articulation.")
            
        if score.time_efficiency < 50:
            feedbacks.append("Response time was slow for this difficulty level.")
        elif score.bonus > 0:
            feedbacks.append("Excellent speed and accuracy streak!")
            
        return " ".join(feedbacks)

    def _apply_adaptive_rules(self, last_score: float):
        adj_score = last_score
        
        if adj_score >= 80:
            self.consecutive_strong_answers += 1
            self.consecutive_weak_answers = 0
        elif adj_score < 40:
            self.consecutive_weak_answers += 1
            self.consecutive_strong_answers = 0
        else:
            self.consecutive_strong_answers = 0
            self.consecutive_weak_answers = 0
            
        # Difficulty Step Up
        if self.consecutive_strong_answers >= 2:
            old_diff = self.current_difficulty.value
            if self.current_difficulty == Difficulty.EASY:
                self.current_difficulty = Difficulty.MEDIUM
            elif self.current_difficulty == Difficulty.MEDIUM:
                self.current_difficulty = Difficulty.HARD
            
            if old_diff != self.current_difficulty.value:
                self.engine_logs.append(f"📈 DECISION: Elevating difficulty to {self.current_difficulty.value.upper()} due to high performance streak.")
                self.consecutive_strong_answers = 0
                self.state = InterviewStatus.ADAPTIVE_MODE
            
        # Difficulty Step Down
        if self.consecutive_weak_answers >= 2:
            old_diff = self.current_difficulty.value
            if self.current_difficulty == Difficulty.HARD:
                self.current_difficulty = Difficulty.MEDIUM
            elif self.current_difficulty == Difficulty.MEDIUM:
                self.current_difficulty = Difficulty.EASY
            
            if old_diff != self.current_difficulty.value:
                self.engine_logs.append(f"📉 DECISION: Stabilizing difficulty to {self.current_difficulty.value.upper()} to better assess performance.")
                self.consecutive_weak_answers = 0

    def _should_terminate(self) -> bool:
        if self.consecutive_weak_answers >= self.config.early_termination_threshold_count:
            self.termination_reason = f"Consecutive failure threshold ({self.config.early_termination_threshold_count}) exceeded."
            return True
        if self.current_question_index >= 2:
            avg = self.total_score_sum / self.current_question_index
            if avg < self.config.min_score_threshold:
                self.termination_reason = f"Average score ({avg:.1f}%) dropped below minimum threshold of {self.config.min_score_threshold}%."
                return True
        return False

    def calculate_confidence_score(self) -> float:
        """FEATURE: Interview Confidence Score (Stability metric)"""
        if len(self.history) < 2:
            return 80.0
        scores = [r.score.overall for r in self.history]
        mean = sum(scores) / len(scores)
        variance = sum((x - mean) ** 2 for x in scores) / len(scores)
        std_dev = variance ** 0.5
        # Lower std_dev means higher stability
        confidence = max(0, 100 - (std_dev * 2))
        return confidence

    def generate_final_report(self) -> InterviewResult:
        final_score = (self.total_score_sum / self.current_question_index) if self.current_question_index > 0 else 0
        confidence = self.calculate_confidence_score()
        
        # Hiring Readiness Mapping
        if final_score >= 80:
            hiring_readiness = "Hire Ready 🚀"
            readiness_cat = "Strong"
        elif final_score >= 60:
            hiring_readiness = "Borderline ⚖️"
            readiness_cat = "Average"
        else:
            hiring_readiness = "Not Ready 🛑"
            readiness_cat = "Needs Improvement"
            
        skill_totals = {}
        skill_counts = {}
        for res in self.history:
            s = res.question.skill
            skill_totals[s] = skill_totals.get(s, 0) + res.score.overall
            skill_counts[s] = skill_counts.get(s, 0) + 1
            
        skill_breakdown = {s: skill_totals[s]/skill_counts[s] for s in skill_totals}
        
        return InterviewResult(
            final_score=final_score,
            hiring_readiness=hiring_readiness,
            readiness_category=readiness_cat,
            confidence_score=confidence,
            skill_breakdown=skill_breakdown,
            strengths=self._identify_strengths(),
            weaknesses=self._identify_weaknesses(),
            suggestions=self._generate_suggestions(readiness_cat),
            status=self.state,
            termination_reason=self.termination_reason,
            timeline=self.history
        )

    def _identify_strengths(self) -> List[str]:
        return list(set([res.question.skill for res in self.history if res.score.overall >= 75]))

    def _identify_weaknesses(self) -> List[str]:
        return list(set([res.question.skill for res in self.history if res.score.overall < 50]))

    def _generate_suggestions(self, cat: str) -> List[str]:
        if cat == "Strong":
            return ["Deepen architectural insight.", "Consistency is key—keep up the streak."]
        elif cat == "Average":
            return ["Improve response depth.", "Minimize filler words."]
        else:
            return ["Revise core fundamentals.", "Practice answering under time pressure."]
