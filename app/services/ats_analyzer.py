import re


def calculate_ats_score(resume_text, resume_skills, jd_skills):
    """
    Calculate an ATS-style resume score based on:
    - Skill matching
    - Resume completeness
    - Keyword relevance
    - Resume length
    """

    resume_text_lower = resume_text.lower()

    # -----------------------------------
    # 1. Skill Match Score
    # -----------------------------------

    resume_skill_set = set(
        skill.lower() for skill in resume_skills
    )

    jd_skill_set = set(
        skill.lower() for skill in jd_skills
    )

    if jd_skill_set:
        matched_skills = resume_skill_set.intersection(
            jd_skill_set
        )

        skill_score = (
            len(matched_skills)
            / len(jd_skill_set)
        ) * 100
    else:
        skill_score = 0

    # -----------------------------------
    # 2. Important Section Score
    # -----------------------------------

    sections = {
        "education": [
            "education",
            "qualification",
            "academic"
        ],
        "experience": [
            "experience",
            "internship",
            "work experience",
            "employment"
        ],
        "projects": [
            "projects",
            "project"
        ],
        "skills": [
            "skills",
            "technical skills",
            "technical skill"
        ],
        "certifications": [
            "certification",
            "certifications",
            "certificate"
        ]
    }

    section_score = 0

    for keywords in sections.values():

        if any(
            keyword in resume_text_lower
            for keyword in keywords
        ):
            section_score += 1

    completeness_score = (
        section_score / len(sections)
    ) * 100

    # -----------------------------------
    # 3. Keyword Relevance
    # -----------------------------------

    keyword_matches = 0

    for skill in jd_skills:

        pattern = r"\b" + re.escape(
            skill.lower()
        ) + r"\b"

        if re.search(
            pattern,
            resume_text_lower
        ):
            keyword_matches += 1

    if jd_skills:
        keyword_score = (
            keyword_matches
            / len(jd_skills)
        ) * 100
    else:
        keyword_score = 0

    # -----------------------------------
    # 4. Resume Length
    # -----------------------------------

    word_count = len(
        resume_text.split()
    )

    if 200 <= word_count <= 1500:
        length_score = 100
    elif 100 <= word_count < 200:
        length_score = 70
    elif 1500 < word_count <= 2500:
        length_score = 80
    else:
        length_score = 50

    # -----------------------------------
    # 5. Final ATS Score
    # -----------------------------------

    final_score = (
        skill_score * 0.50
        + completeness_score * 0.20
        + keyword_score * 0.20
        + length_score * 0.10
    )

    return {
        "ats_score": round(final_score, 2),
        "skill_score": round(skill_score, 2),
        "completeness_score": round(
            completeness_score,
            2
        ),
        "keyword_score": round(
            keyword_score,
            2
        ),
        "length_score": round(
            length_score,
            2
        ),
        "word_count": word_count
    }