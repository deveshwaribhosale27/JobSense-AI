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


def extract_jd_skills(jd_text):
    found_skills = []

    text = jd_text.lower()

    for skill in SKILL_LIST:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def analyze_job_description(jd_text):

    skills = extract_jd_skills(jd_text)

    jd_data = {
        "job_description": jd_text,
        "required_skills": skills
    }

    return jd_data