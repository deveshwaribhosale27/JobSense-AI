import re


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    # Programming
    "python": "Python",
    "python3": "Python",

    "javascript": "JavaScript",
    "js": "JavaScript",
    "ecmascript": "JavaScript",

    "typescript": "TypeScript",
    "ts": "TypeScript",

    "java": "Java",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "csharp": "C#",

    # Data
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongodb": "MongoDB",
    "mongo": "MongoDB",

    # Data Science
    "machine learning": "Machine Learning",
    "machine-learning": "Machine Learning",
    "ml": "Machine Learning",

    "deep learning": "Deep Learning",
    "deep-learning": "Deep Learning",
    "dl": "Deep Learning",

    "artificial intelligence": "Artificial Intelligence",
    "ai": "Artificial Intelligence",

    "data science": "Data Science",
    "data-science": "Data Science",

    "data analysis": "Data Analysis",
    "data analytics": "Data Analytics",

    # Python libraries
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",

    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "plotly": "Plotly",

    # Deep Learning frameworks
    "tensorflow": "TensorFlow",
    "keras": "Keras",
    "pytorch": "PyTorch",
    "torch": "PyTorch",

    # AI / GenAI
    "natural language processing": "NLP",
    "nlp": "NLP",

    "large language model": "LLM",
    "large language models": "LLM",
    "llm": "LLM",

    "generative ai": "Generative AI",
    "generative artificial intelligence": "Generative AI",
    "genai": "Generative AI",

    "retrieval augmented generation": "RAG",
    "retrieval-augmented generation": "RAG",
    "rag": "RAG",

    "prompt engineering": "Prompt Engineering",

    "computer vision": "Computer Vision",
    "cv": "Computer Vision",

    # Web / Backend
    "html": "HTML",
    "html5": "HTML",

    "css": "CSS",
    "css3": "CSS",

    "react": "React",
    "reactjs": "React",

    "node.js": "Node.js",
    "nodejs": "Node.js",
    "node js": "Node.js",

    "express": "Express.js",
    "express.js": "Express.js",

    "flask": "Flask",
    "django": "Django",

    "fastapi": "FastAPI",
    "fast api": "FastAPI",

    "rest api": "REST API",
    "rest apis": "REST API",
    "restful api": "REST API",
    "api development": "API Development",

    # Cloud / DevOps
    "aws": "AWS",
    "amazon web services": "AWS",

    "azure": "Azure",
    "microsoft azure": "Azure",

    "gcp": "Google Cloud",
    "google cloud": "Google Cloud",

    "docker": "Docker",
    "kubernetes": "Kubernetes",

    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",

    # Visualization / BI
    "power bi": "Power BI",
    "powerbi": "Power BI",

    "tableau": "Tableau",

    # Explainable AI
    "shap": "SHAP",
    "shapley": "SHAP",

    "lime": "LIME",

    # Databases
    "sql server": "SQL Server",
    "mssql": "SQL Server",

    "oracle": "Oracle",

    # Other
    "excel": "Excel",
    "microsoft excel": "Excel",
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):
    """
    Normalize text for better skill matching.
    """

    if not text:
        return ""

    text = text.lower()

    # Replace common separators
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("_", " ")

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# NORMALIZE SINGLE SKILL
# ============================================================

def normalize_skill(skill):
    """
    Convert aliases into standard skill names.
    """

    if not skill:
        return None

    normalized = normalize_text(skill)

    return SKILL_ALIASES.get(
        normalized,
        skill.strip()
    )


# ============================================================
# EXTRACT SKILLS FROM TEXT
# ============================================================

def extract_dynamic_skills(text):
    """
    Detect known skills and aliases from arbitrary text.

    This is more flexible than the old fixed SKILL_LIST approach.
    """

    normalized_text = normalize_text(text)

    found_skills = set()

    # Sort aliases by length so that
    # 'machine learning' is checked before 'learning'
    aliases = sorted(
        SKILL_ALIASES.keys(),
        key=len,
        reverse=True
    )

    for alias in aliases:

        # Special handling for symbols such as C++, C#
        if alias in {"c++", "c#"}:
            pattern = re.escape(alias)
        else:
            pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"

        if re.search(pattern, normalized_text):

            standard_skill = SKILL_ALIASES[alias]

            found_skills.add(standard_skill)

    return sorted(found_skills)


# ============================================================
# MERGE SKILLS
# ============================================================

def merge_skills(*skill_lists):
    """
    Merge multiple skill lists and remove duplicates.
    """

    merged = set()

    for skills in skill_lists:

        if not skills:
            continue

        for skill in skills:

            normalized = normalize_skill(skill)

            if normalized:
                merged.add(normalized)

    return sorted(merged)