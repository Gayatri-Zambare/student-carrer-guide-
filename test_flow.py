import httpx
import json

client = httpx.Client(base_url="http://127.0.0.1:8000")

print("=== 1. HEALTH CHECK ===")
res = client.get("/health")
assert res.status_code == 200
print("Backend is Healthy:", res.json())

print("\n=== 2. SEEDED STUDENT LOGIN ===")
res = client.post("/auth/login", json={"email": "student@aicareerguide.com", "password": "Student@123"})
assert res.status_code == 200, res.text
st_token = res.json()["access_token"]
st_headers = {"Authorization": f"Bearer {st_token}"}
print("Student Logged In:", res.json()["user"]["name"])

print("\n=== 3. STUDENT PROFILE & DASHBOARD ===")
res = client.get("/student/profile", headers=st_headers)
assert res.status_code == 200
profile = res.json()
print("Profile Stream:", profile["stream"], "| Completion:", profile["completion_percentage"], "% | Marks:", profile["overall_percentage"])

print("\n=== 4. RECOMMENDATIONS & EXPLAINABLE AI ===")
res = client.get("/recommendations", headers=st_headers)
assert res.status_code == 200
rec_data = res.json()
print("Traits:", rec_data["traits"])
print("Top 3 Matches:")
for r in rec_data["recommendations"][:3]:
    print(f"  - {r['career_name']} ({r['compatibility_score']} pct match)")
    print(f"    Why: {r['explanation']}")
    print(f"    Matched Factors: {r['matched_factors'][:2]}")
    print(f"    Skill Gaps: {r['skills_to_improve'][:2]}")

print("\n=== 5. CAREER EXPLORER ===")
res = client.get("/careers?category=Technology")
assert res.status_code == 200
tech_careers = res.json()
print(f"Found {len(tech_careers)} Technology Careers:")
for c in tech_careers[:3]:
    roadmap = json.loads(c["roadmap"]) if isinstance(c["roadmap"], str) else c["roadmap"]
    print(f"  - {c['name']} (Roadmap stages: {len(roadmap)})")

print("\n=== 6. AI CAREER ASSISTANT ===")
res = client.post("/assistant/chat", headers=st_headers, json={"message": "What skills should I learn to become an AI/ML Engineer?"})
assert res.status_code == 200
chat_res = res.json()
print("AI Assistant Answer:")
print(" ", chat_res["reply"][:140] + "...")

print("\n=== 7. SEEDED ADMIN LOGIN & DASHBOARD ===")
res = client.post("/auth/login", json={"email": "admin@aicareerguide.com", "password": "Admin@123"})
assert res.status_code == 200
ad_token = res.json()["access_token"]
ad_headers = {"Authorization": f"Bearer {ad_token}"}
res = client.get("/admin/dashboard", headers=ad_headers)
assert res.status_code == 200
admin_data = res.json()
print("Admin Metrics:", {
    "total_students": admin_data["total_students"],
    "total_assessments": admin_data["total_assessments"],
    "total_careers": admin_data["total_careers"]
})

print("\n=== 8. NEW STUDENT REGISTRATION & ASSESSMENT SIMULATION ===")
new_student = {
    "name": "Priya Patel",
    "email": "priya.patel@test.edu",
    "password": "Password@123",
    "age": 20,
    "education_level": "Undergraduate",
    "current_class_year": "3rd Year",
    "stream": "Science"
}
reg_res = client.post("/auth/register", json=new_student)
if reg_res.status_code == 400: # Already registered from prior run
    login_res = client.post("/auth/login", json={"email": new_student["email"], "password": new_student["password"]})
    new_token = login_res.json()["access_token"]
else:
    new_token = reg_res.json()["access_token"]
new_headers = {"Authorization": f"Bearer {new_token}"}

# Get questions
q_res = client.get("/questions")
questions = q_res.json()
print(f"Loaded {len(questions)} Assessment Questions.")

# Submit assessment answers
sample_answers = []
for q in questions:
    if q["question_type"] == "rating":
        ans = 4
    elif q["question_type"] == "checkbox":
        ans = ["Mathematics", "Computer Science"]
    elif q["question_type"] == "single_choice":
        opts = q["options"]
        ans = opts[0] if opts else "Solving logical problems"
    else:
        ans = "Technology"
    sample_answers.append({"question_id": q["id"], "answer": ans})

submit_res = client.post("/assessment/submit", headers=new_headers, json={"answers": sample_answers})
assert submit_res.status_code == 200
sub_data = submit_res.json()
print("New Student Assessment Completed! Top Recommendation:")
top_rec = sub_data["recommendations"][0]
print(f"  {top_rec['career_name']} - {top_rec['compatibility_score']}% Match")
print(f"  Explanation: {top_rec['explanation']}")

print("\n=== 9. FEEDBACK SYSTEM WORKFLOW ===")
fb_payload = {
    "satisfaction_rating": 5,
    "recommendation_relevance": "Very Relevant",
    "useful_features": ["Career Recommendations", "AI Career Analysis", "Skill Gap Analysis"],
    "confidence_rating": 5,
    "comments": "Great AI recommendation engine! Very clear guidance and skill gaps."
}
fb_res = client.post("/feedback", headers=new_headers, json=fb_payload)
print("Student Feedback Submission Status:", fb_res.status_code)
assert fb_res.status_code in [201, 400]

status_res = client.get("/feedback/status", headers=new_headers)
assert status_res.status_code == 200
print("Student Feedback Status Verified:", status_res.json()["has_submitted"])

admin_fb_res = client.get("/admin/feedbacks/summary", headers=ad_headers)
assert admin_fb_res.status_code == 200
summary = admin_fb_res.json()
print("Admin Feedback Summary Verified: Total Feedbacks =", summary["total_feedbacks"], "| Avg Satisfaction =", summary["average_satisfaction"])

print("\n=== ALL WORKFLOWS FULLY VERIFIED AND PASSING 100% ===")

