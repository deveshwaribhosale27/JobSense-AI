def analyze_skill_gap(missing_skills):
    high_priority = []
    medium_priority = []

    high_priority_skills = {
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Data Science",
        "NLP",
        "LLM",
        "Generative AI",
        "RAG",
        "Python",
        "SQL",
    }

    for skill in missing_skills:
        if skill in high_priority_skills:
            high_priority.append(skill)
        else:
            medium_priority.append(skill)

    return {
        "high_priority": high_priority,
        "medium_priority": medium_priority
    }