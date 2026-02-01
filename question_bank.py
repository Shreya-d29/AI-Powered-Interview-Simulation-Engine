from typing import List, Optional
from models import Question, Difficulty

QUESTION_BANK: List[Question] = [
    # PYTHON & BACKEND
    Question(
        id="py_01", skill="Python", difficulty=Difficulty.EASY,
        question_text="Describe the difference between Python's list and dictionary data structures and their use cases.",
        expected_keywords=["order", "key-value", "o(1)", "indexing", "hash table"],
        time_limit=45
    ),
    Question(
        id="py_02", skill="Python", difficulty=Difficulty.MEDIUM,
        question_text="What are decorators and how do they differ from simple higher-order functions?",
        expected_keywords=["wrapper", "@", "metadata", "function modification", "encapsulation"],
        time_limit=90
    ),
    Question(
        id="py_03", skill="Python", difficulty=Difficulty.HARD,
        question_text="Explain Python's memory management, including reference counting and garbage collection for cyclic references.",
        expected_keywords=["refcount", "generational gc", "cycle detector", "mem-leak", "slots"],
        time_limit=150
    ),
    # SYSTEM DESIGN
    Question(
        id="sd_01", skill="System Design", difficulty=Difficulty.EASY,
        question_text="What is a Content Delivery Network (CDN) and how does it improve system latency?",
        expected_keywords=["edge location", "caching", "geographic", "static content", "low latency"],
        time_limit=60
    ),
    Question(
        id="sd_02", skill="System Design", difficulty=Difficulty.MEDIUM,
        question_text="Discuss the trade-offs between Vertical and Horizontal scaling in a high-traffic environment.",
        expected_keywords=["ram/cpu", "sharding", "statelessness", "load balancing", "single point of failure"],
        time_limit=120
    ),
    Question(
        id="sd_03", skill="System Design", difficulty=Difficulty.HARD,
        question_text="Design a distributed logging system that can handle 1 million events per second with high availability.",
        expected_keywords=["kafka", "eventual consistency", "sharding", "indexing", "retention policy", "heartbeat"],
        time_limit=180
    ),
    # DATA STRUCTURES
    Question(
        id="ds_01", skill="Data Structures", difficulty=Difficulty.EASY,
        question_text="Explain the 'Double Ended Queue' (deque) and its primary advantages over a standard list.",
        expected_keywords=["o(1) pop", "left", "right", "collections module", "thread safe"],
        time_limit=45
    ),
    Question(
        id="ds_02", skill="Data Structures", difficulty=Difficulty.MEDIUM,
        question_text="How does a Bloom Filter work and what are its performance trade-offs?",
        expected_keywords=["probabilistic", "false positive", "set membership", "hashing", "memory efficient"],
        time_limit=100
    ),
    Question(
        id="ds_03", skill="Data Structures", difficulty=Difficulty.HARD,
        question_text="Compare the time and space complexity of Dijkstra's vs A* search algorithms.",
        expected_keywords=["heuristic", "greedy", "shortest path", "manhattan distance", "priority queue"],
        time_limit=150
    ),
    # SECURITY & DATABASES
    Question(
        id="sec_01", skill="Security", difficulty=Difficulty.MEDIUM,
        question_text="What is SQL Injection and how can prepared statements prevent it?",
        expected_keywords=["parameterized queries", "input sanitization", "orm", "validation"],
        time_limit=60
    ),
    Question(
        id="db_01", skill="Databases", difficulty=Difficulty.HARD,
        question_text="Explain the CAP theorem and provide an example of a system that prioritizes AP over CP.",
        expected_keywords=["consistency", "availability", "partition tolerance", "cassandra", "dynamodb"],
        time_limit=120
    )
]

def get_questions_by_difficulty(difficulty: Difficulty, category: Optional[str] = None) -> List[Question]:
    filtered = [q for q in QUESTION_BANK if q.difficulty == difficulty]
    if category:
        filtered = [q for q in filtered if q.skill == category]
    return filtered
