from utils.pdf_reader import extract_text_from_pdf
from app.agents.resume_agent import analyze_resume
from app.agents.jd_agent import analyze_job_description
from app.services.ats_analyzer import calculate_ats_score


resume_text = extract_text_from_pdf(
    "resume.pdf"
)

resume_data = analyze_resume(
    resume_text
)

jd_text = """
We are looking for a Junior Full Stack Developer.

Required Skills:
HTML, CSS, JavaScript, React, Node.js,
Express.js, Python, MySQL, MongoDB,
Git, REST API, PHP.
"""

jd_data = analyze_job_description(
    jd_text
)

ats_result = calculate_ats_score(
    resume_text,
    resume_data["skills"],
    jd_data["required_skills"]
)

print("\n======================================")
print("       JOBSENSE AI - ATS ANALYSIS")
print("======================================")

print(
    f"\nATS Score: "
    f"{ats_result['ats_score']}%"
)

print(
    f"Skill Score: "
    f"{ats_result['skill_score']}%"
)

print(
    f"Completeness Score: "
    f"{ats_result['completeness_score']}%"
)

print(
    f"Keyword Score: "
    f"{ats_result['keyword_score']}%"
)

print(
    f"Length Score: "
    f"{ats_result['length_score']}%"
)

print(
    f"Resume Words: "
    f"{ats_result['word_count']}"
)

print("\n======================================")