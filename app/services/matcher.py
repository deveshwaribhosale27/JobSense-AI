from app.services.semantic_matcher import semantic_skill_matching


def calculate_match(resume_skills, jd_skills):
    """
    Calculate final job match using:

    1. Exact keyword matching
    2. Semantic skill matching

    Final score:
        40% Keyword Match
        60% Semantic Match
    """

    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    # ========================================================
    # 1. EXACT KEYWORD MATCH
    # ========================================================

    matched_skills = sorted(
        resume_set.intersection(jd_set)
    )

    missing_skills = sorted(
        jd_set - resume_set
    )

    if len(jd_set) == 0:
        keyword_score = 0
    else:
        keyword_score = (
            len(matched_skills)
            / len(jd_set)
        ) * 100

    # ========================================================
    # 2. SEMANTIC MATCH
    # ========================================================

    semantic_result = semantic_skill_matching(
        resume_skills,
        jd_skills
    )

    semantic_score = semantic_result[
        "semantic_score"
    ]

    # ========================================================
    # 3. FINAL MATCH SCORE
    # ========================================================

    final_score = (
        keyword_score * 0.40
        +
        semantic_score * 0.60
    )

    # ========================================================
    # 4. SEMANTIC MATCHED SKILLS
    # ========================================================

    semantic_matched = semantic_result[
        "matched_skills"
    ]

    semantic_missing = semantic_result[
        "missing_skills"
    ]

    return {

        # Final score
        "match_score": round(
            final_score,
            2
        ),

        # Exact keyword score
        "keyword_score": round(
            keyword_score,
            2
        ),

        # Semantic score
        "semantic_score": round(
            semantic_score,
            2
        ),

        # Exact matches
        "matched_skills": matched_skills,

        # Exact missing skills
        "missing_skills": missing_skills,

        # Semantic matches
        "semantic_matched_skills":
            semantic_matched,

        # Semantic missing
        "semantic_missing_skills":
            semantic_missing,

        # Detailed semantic comparison
        "skill_matches":
            semantic_result["skill_matches"]
    }