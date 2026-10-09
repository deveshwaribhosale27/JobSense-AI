import re

SKILL_LIST = [
    "Python",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Science",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "NLP",
    "LLM",
    "Generative AI",
    "RAG",
    "FastAPI",
    "Streamlit",
    "Flask",
    "REST API",
    "Git",
    "GitHub",
    "Docker",
    "Power BI",
    "Tableau",
    "Matplotlib",
    "Plotly",
    "SHAP",
    "LIME",
]


def extract_skills(resume_text):
    found_skills = []

    text = resume_text.lower()

    for skill in SKILL_LIST:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def analyze_resume(resume_text):
    skills = extract_skills(resume_text)

    resume_data = {
        "resume_text": resume_text,
        "skills": skills,
        "education": [],
        "projects": [],
        "experience": []
    }

    return resume_data