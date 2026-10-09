from app.services.skill_normalizer import (
    extract_dynamic_skills,
    normalize_skill
)


print("\n==========================================")
print("       JOBSENSE AI - DYNAMIC SKILLS")
print("==========================================\n")


resume_text = """
I am a Data Science graduate with experience in
Python, ML, SQL, Pandas, NumPy and Scikit Learn.

I have built projects using TensorFlow and PyTorch.
I also worked with PowerBI, GitHub and REST APIs.

Currently learning Generative AI, LLM and RAG.
"""


skills = extract_dynamic_skills(resume_text)


print("Detected Skills:\n")

for skill in skills:
    print("✓", skill)


print("\nTotal Skills:", len(skills))


print("\n==========================================")
print("          ALIAS TEST")
print("==========================================\n")


test_skills = [
    "ML",
    "AI",
    "PowerBI",
    "sklearn",
    "nodejs",
    "genai",
    "rest api"
]


for skill in test_skills:

    print(
        f"{skill}  →  {normalize_skill(skill)}"
    )


print("\n==========================================")