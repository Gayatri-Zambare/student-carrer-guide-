# AI CareerGuide — Architecture & Explainable AI Specification

## 1. System Overview
**AI CareerGuide** is an intelligent student career guidance web platform built for the **Fundamentals of Artificial Intelligence (FAI)** mini-project demonstration. It replaces rigid questionnaire tools with a multi-factor cognitive, academic, and interest-based recommendation system that outputs explainable career matches, skill gaps, and stage-wise roadmaps.

---

## 2. Core Architecture

```
[ Frontend: React 18 + TypeScript + Tailwind CSS ]
                      │
           REST API (JSON / Bearer JWT)
                      ▼
[ Backend: FastAPI (Python 3.14) + SQLAlchemy ORM ]
                      │
   ┌──────────────────┴──────────────────┐
   ▼                                     ▼
[ SQLite Database ]        [ Explainable AI Engine ]
  • users                    • 5-Factor Weighted Scoring
  • student_profiles         • Radar Cognitive Trait Profiling
  • careers (20+)            • Skill Gap Extraction
  • questions (28)           • Explainable Match Rationale
  • assessments & answers    • Conversational Rule-Based Chatbot
  • recommendations
```

---

## 3. Explainable AI (XAI) Recommendation Methodology

The core recommendation algorithm evaluates career compatibility using a 5-dimension weighted multi-factor formula:

$$\text{Career Score} = (I \times 0.30) + (S \times 0.25) + (A \times 0.15) + (W \times 0.15) + (G \times 0.15)$$

Where:
* **$I$ (Interest Match - 30%)**: Calculates semantic overlap between student enjoyed activities, favorite subjects, problem solving types, and free-time passions with the career's domain requirements.
* **$S$ (Skill Match - 25%)**: Evaluates student self-reported ratings across 15 core skills (1 to 5 scale) against the career's prerequisite benchmark vector.
* **$A$ (Academic Match - 15%)**: Incorporates academic stream alignment (Science, Commerce, Arts/Humanities), overall percentage, and subject grade strengths.
* **$W$ (Work Style & Preferences - 15%)**: Assesses preferred team environment, problem-solving methods, learning new technology comfort, and public speaking comfort.
* **$G$ (Career Goals - 15%)**: Matches primary overarching aspirations (e.g. High technical expertise, Social impact, Entrepreneurship, Financial growth) with target industry sectors.

### Normalization and Scoring Range
Scores are normalized to a realistic distribution between **38% and 96.5%**, preventing hyper-simplistic 100% false guarantees while rewarding balanced profile strengths.

### Explainability Output
For every recommended career, the engine produces:
1. **Compatibility Score**: e.g., `88% Match`
2. **Transparent Rationale**: Natural language paragraph detailing the major contributing factors.
3. **Matched Factor Checkmarks**: Granular proof points (e.g. `✓ Enjoys solving logical problems`, `✓ High proficiency in Programming (4.5/5)`).
4. **Key Matching Skills**: Immediate strengths the student brings to this career.
5. **Skill Gap Analysis (Areas to Develop)**: Precise technical and soft skills where the student should focus their learning.
6. **Multi-Stage Roadmap**: Stage 1 Fundamentals &rarr; Stage 2 Applications &rarr; Stage 3 Advanced &rarr; Stage 4 Industry Readiness.

---

## 4. Database Schema

* `users`: `id`, `name`, `email`, `password_hash`, `role` (student/admin), `created_at`
* `student_profiles`: `id`, `user_id`, `age`, `education_level`, `stream`, `current_class_year`, `overall_percentage`, `math_marks`, `science_marks`, `cs_marks`, `english_marks`, `commerce_marks`, `career_goals`
* `skills`: `id`, `name`, `category`, `description`
* `student_skills`: `id`, `student_profile_id`, `skill_id`, `rating` (1-5)
* `questions`: `id`, `category`, `question_text`, `question_type`, `options`, `weight`, `field_key`
* `assessments`: `id`, `student_id`, `started_at`, `completed_at`, `status`, `total_score`, `profile_traits`
* `answers`: `id`, `assessment_id`, `question_id`, `answer_value`
* `careers`: `id`, `name`, `category`, `description`, `education_path`, `work_style`, `required_skills`, `recommended_subjects`, `related_interests`, `typical_responsibilities`, `beginner_skills`, `advanced_skills`, `roadmap`, `related_courses`, `related_job_roles`
* `recommendations`: `id`, `assessment_id`, `career_id`, `compatibility_score`, `explanation`, `matched_factors`, `skill_gaps`

---

## 5. Security & Principles
* **PBKDF2 Password Hashing**: Cryptographically salted 100,000-iteration hashing with zero external C-dependencies.
* **JWT Access Tokens**: Stateless Bearer tokens signed with HS256 algorithm.
* **Role-Based Authorization**: Separate student and administrative permissions for sensitive endpoints.
* **AI Principle Notice**: Strictly adheres to ethical AI principles — labels generated results as guidance and educational discovery rather than deterministic future predictions.
