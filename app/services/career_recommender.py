def recommend_careers(resume_skills, jd_skills):

    resume_skills = set(resume_skills)
    jd_skills = set(jd_skills)

    career_roles = {
        "Data Scientist": {
            "skills": {
                "Python",
                "SQL",
                "Machine Learning",
                "Data Science",
                "Pandas",
                "NumPy",
                "Scikit-learn"
            }
        },

        "Machine Learning Engineer": {
            "skills": {
                "Python",
                "Machine Learning",
                "Deep Learning",
                "Scikit-learn",
                "TensorFlow",
                "PyTorch",
                "Git"
            }
        },

        "AI/ML Developer": {
            "skills": {
                "Python",
                "Machine Learning",
                "Deep Learning",
                "Artificial Intelligence",
                "TensorFlow",
                "PyTorch",
                "Git"
            }
        },

        "Data Analyst": {
            "skills": {
                "Python",
                "SQL",
                "Pandas",
                "NumPy",
                "Power BI",
                "Tableau"
            }
        },

        "NLP Engineer": {
            "skills": {
                "Python",
                "NLP",
                "LLM",
                "Machine Learning",
                "Deep Learning"
            }
        },

        "Generative AI Engineer": {
            "skills": {
                "Python",
                "LLM",
                "Generative AI",
                "RAG",
                "FastAPI",
                "Git"
            }
        }
    }

    recommendations = []

    for role, data in career_roles.items():

        required_skills = data["skills"]

        matched_resume = resume_skills.intersection(required_skills)

        matched_jd = jd_skills.intersection(required_skills)

        score = (len(matched_resume) / len(required_skills)) * 100

        recommendations.append({
            "role": role,
            "score": round(score, 2),
            "matched_skills": sorted(matched_resume),
            "missing_skills": sorted(required_skills - resume_skills),
            "jd_relevance": len(matched_jd)
        })

    recommendations.sort(
        key=lambda x: (x["score"], x["jd_relevance"]),
        reverse=True
    )

    return recommendations