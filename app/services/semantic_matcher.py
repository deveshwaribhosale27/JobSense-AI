from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# LOAD SEMANTIC MODEL
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# ============================================================
# THRESHOLDS
# ============================================================

STRONG_MATCH_THRESHOLD = 0.65
WEAK_MATCH_THRESHOLD = 0.50


# ============================================================
# BASIC SEMANTIC SIMILARITY
# ============================================================

def calculate_semantic_similarity(text1, text2):
    """
    Calculate semantic similarity between two texts.

    Returns:
        Score between 0 and 100
    """

    if not text1 or not text2:
        return 0.0

    embeddings = model.encode(
        [text1, text2],
        normalize_embeddings=True
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    score = max(
        0,
        min(100, similarity * 100)
    )

    return round(score, 2)


# ============================================================
# SEMANTIC SKILL MATCHING
# ============================================================

def semantic_skill_matching(
    resume_skills,
    jd_skills
):
    """
    Compare JD skills against resume skills.

    Categories:

    >= 65%  → Strong Match
    50-64%  → Weak/Related Match
    < 50%   → Missing
    """

    if not resume_skills or not jd_skills:

        return {
            "matched_skills": [],
            "weak_matches": [],
            "missing_skills": [],
            "skill_matches": [],
            "semantic_score": 0.0
        }

    # ========================================================
    # CREATE EMBEDDINGS
    # ========================================================

    resume_embeddings = model.encode(
        resume_skills,
        normalize_embeddings=True
    )

    jd_embeddings = model.encode(
        jd_skills,
        normalize_embeddings=True
    )

    # ========================================================
    # SIMILARITY MATRIX
    # ========================================================

    similarity_matrix = cosine_similarity(
        jd_embeddings,
        resume_embeddings
    )

    matched_skills = []
    weak_matches = []
    missing_skills = []
    skill_matches = []

    strong_scores = []

    # ========================================================
    # CHECK EACH JD SKILL
    # ========================================================

    for i, jd_skill in enumerate(jd_skills):

        best_index = similarity_matrix[i].argmax()

        best_score = similarity_matrix[i][best_index]

        best_resume_skill = resume_skills[best_index]

        similarity_percentage = round(
            max(
                0,
                min(
                    100,
                    best_score * 100
                )
            ),
            2
        )

        # Store complete comparison
        skill_matches.append({
            "jd_skill": jd_skill,
            "resume_skill": best_resume_skill,
            "similarity": similarity_percentage
        })

        # ====================================================
        # STRONG MATCH
        # ====================================================

        if best_score >= STRONG_MATCH_THRESHOLD:

            matched_skills.append({
                "jd_skill": jd_skill,
                "resume_skill": best_resume_skill,
                "similarity": similarity_percentage
            })

            strong_scores.append(best_score)

        # ====================================================
        # WEAK / RELATED MATCH
        # ====================================================

        elif best_score >= WEAK_MATCH_THRESHOLD:

            weak_matches.append({
                "jd_skill": jd_skill,
                "resume_skill": best_resume_skill,
                "similarity": similarity_percentage
            })

        # ====================================================
        # MISSING
        # ====================================================

        else:

            missing_skills.append(jd_skill)

    # ========================================================
    # SEMANTIC SCORE
    # ========================================================

    if len(jd_skills) == 0:

        semantic_score = 0

    else:

        # Strong matches get full contribution.
        # Weak matches get partial contribution.

        total_score = 0

        for item in skill_matches:

            similarity = item["similarity"]

            if similarity >= 65:

                contribution = 100

            elif similarity >= 50:

                contribution = 50

            else:

                contribution = 0

            total_score += contribution

        semantic_score = (
            total_score / len(jd_skills)
        )

    return {

        "matched_skills":
            matched_skills,

        "weak_matches":
            weak_matches,

        "missing_skills":
            missing_skills,

        "skill_matches":
            skill_matches,

        "semantic_score":
            round(semantic_score, 2)
    }