from utils.pdf_reader import extract_text_from_pdf
from app.agents.resume_agent import analyze_resume


resume_text = extract_text_from_pdf("resume.pdf")

print("\n===== EXTRACTED RESUME TEXT =====")
print(resume_text[:3000])
print("=================================")

result = analyze_resume(resume_text)

print("\n===== JOBSENSE AI - RESUME ANALYSIS =====")

print("\nSkills Found:")
for skill in result["skills"]:
    print("-", skill)

print("\nTotal Skills:", len(result["skills"]))

print("\n==========================================")