from app.agents.jd_agent import analyze_job_description


jd_text = """
We are looking for a Data Scientist with strong Python and SQL skills.
The candidate should have experience in Machine Learning, Pandas, NumPy,
Scikit-learn, Power BI and Git.
Knowledge of Deep Learning and NLP is a plus.
"""


result = analyze_job_description(jd_text)


print("\n===== JOBSENSE AI - JOB DESCRIPTION ANALYSIS =====")

print("\nRequired Skills:")

for skill in result["required_skills"]:
    print("-", skill)

print("\nTotal Required Skills:", len(result["required_skills"]))

print("\n===================================================")