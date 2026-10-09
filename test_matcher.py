from app.agents.resume_agent import analyze_resume
from app.agents.jd_agent import analyze_job_description
from app.services.matcher import calculate_match
from utils.pdf_reader import extract_text_from_pdf
from app.services.skill_gap import analyze_skill_gap
from app.services.career_recommender import recommend_careers

# Resume PDF read
resume_text = extract_text_from_pdf("resume.pdf")

# Resume analysis
resume_data = analyze_resume(resume_text)


# Sample Job Description
jd_text = """
We are looking for a Data Scientist with strong Python and SQL skills.
The candidate should have experience in Machine Learning, Pandas, NumPy,
Scikit-learn, Power BI and Git.
Knowledge of Deep Learning and NLP is a plus.
"""

# JD analysis
jd_data = analyze_job_description(jd_text)


# Calculate match
match_result = calculate_match(
    resume_data["skills"],
    jd_data["required_skills"]
)
skill_gap = analyze_skill_gap(
    match_result["missing_skills"]
)
career_recommendations = recommend_careers(
    resume_data["skills"],
    jd_data["required_skills"]
)
print("\n===== JOBSENSE AI - SKILL MATCHING =====")

print("\nResume Skills:")
for skill in resume_data["skills"]:
    print("-", skill)

print("\nJD Required Skills:")
for skill in jd_data["required_skills"]:
    print("-", skill)

print("\nMatch Score:", match_result["match_score"], "%")

print("\nMatched Skills:")
for skill in match_result["matched_skills"]:
    print("✓", skill)

print("\nMissing Skills:")
for skill in match_result["missing_skills"]:
    print("✗", skill)

print("\n========================================")
print("\nHigh Priority Skills:")
for skill in skill_gap["high_priority"]:
    print("🔴", skill)

print("\nMedium Priority Skills:")
for skill in skill_gap["medium_priority"]:
    print("🟡", skill)

    print("\n===== CAREER RECOMMENDATIONS =====")

for index, recommendation in enumerate(career_recommendations, start=1):
    print(
        f"{index}. {recommendation['role']} "
        f"→ {recommendation['score']}%"
    )

print("\n==================================")