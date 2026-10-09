
import re


def generate_ats_suggestions(
    resume_text,
    resume_skills,
    jd_skills,
    ats_result
):
    suggestions = []

    resume_lower = resume_text.lower()
    resume_skill_set = {
        skill.lower() for skill in resume_skills
    }

    jd_skill_set = {
        skill.lower() for skill in jd_skills
    }

    # 1. Missing job-specific skills
    missing_skills = sorted(
        jd_skill_set - resume_skill_set
    )

    if missing_skills:
        suggestions.append({
            "priority": "High",
            "title": "Add relevant job skills",
            "message": (
                "Your resume does not list these detected "
                "job-description skills: "
                + ", ".join(missing_skills[:8])
                + ". Add them only if you genuinely have "
                "the skills or relevant experience."
            )
        })
    else:
        suggestions.append({
            "priority": "Good",
            "title": "Detected skills coverage",
            "message": (
                "All detected job skills are present in "
                "your extracted resume skill list. "
                "Verify that your resume gives evidence "
                "for each skill."
            )
        })

    # 2. Resume section checks
    sections = {
        "Education": [
            "education",
            "qualification",
            "academic"
        ],
        "Projects": [
            "projects",
            "project"
        ],
        "Technical Skills": [
            "skills",
            "technical skills",
            "technical skill"
        ],
        "Experience / Internship": [
            "experience",
            "internship",
            "work experience"
        ],
        "Certifications": [
            "certification",
            "certifications",
            "certificate"
        ]
    }

    missing_sections = []

    for section, keywords in sections.items():
        if not any(
            keyword in resume_lower
            for keyword in keywords
        ):
            missing_sections.append(section)

    if missing_sections:
        suggestions.append({
            "priority": "Medium",
            "title": "Review resume sections",
            "message": (
                "These sections were not detected by a "
                "simple text check: "
                + ", ".join(missing_sections)
                + ". Check your headings and add relevant "
                "sections where appropriate."
            )
        })
    else:
        suggestions.append({
            "priority": "Good",
            "title": "Resume section check",
            "message": (
                "Education, Projects, Skills, Experience "
                "and Certifications headings appear to be "
                "present in the extracted text."
            )
        })

    # 3. Resume length
    word_count = len(resume_text.split())

    if word_count < 200:
        suggestions.append({
            "priority": "Medium",
            "title": "Review resume content length",
            "message": (
                f"Only {word_count} words were extracted. "
                "Check whether your PDF text extraction "
                "is complete and whether important details "
                "are missing."
            )
        })

    elif word_count > 1000:
        suggestions.append({
            "priority": "Medium",
            "title": "Review resume length",
            "message": (
                f"{word_count} words were extracted. "
                "Remove repetition and keep details relevant "
                "to the target job."
            )
        })

    else:
        suggestions.append({
            "priority": "Good",
            "title": "Resume length check",
            "message": (
                f"{word_count} words were extracted. "
                "Review readability and relevance; word "
                "count alone cannot determine resume quality."
            )
        })

    # 4. ATS score feedback
    ats_score = ats_result.get("ats_score", 0)

    if ats_score < 50:
        suggestions.append({
            "priority": "High",
            "title": "Improve job relevance",
            "message": (
                "Review the target job requirements, "
                "relevant skills, project descriptions "
                "and resume section headings."
            )
        })

    elif ats_score < 75:
        suggestions.append({
            "priority": "Medium",
            "title": "Strengthen your resume",
            "message": (
                "Improve relevant keyword coverage and "
                "show where you applied each skill in "
                "projects, internships or work."
            )
        })

    else:
        suggestions.append({
            "priority": "Good",
            "title": "Keep evidence specific",
            "message": (
                "Continue tailoring your resume to the job. "
                "A high calculated score does not guarantee "
                "an ATS shortlist or interview."
            )
        })

    # 5. Check for measurable project evidence
    has_numbers = bool(
        re.search(r"\b\d+(?:\.\d+)?%?\b", resume_text)
    )

    if not has_numbers:
        suggestions.append({
            "priority": "Medium",
            "title": "Strengthen project descriptions",
            "message": (
                "Where accurate, include measurable results "
                "such as model accuracy, dataset size, "
                "processing time or project outcomes."
            )
        })

    return suggestions