from app.services.semantic_matcher import (
    calculate_semantic_similarity,
    semantic_skill_matching
)


print("\n==========================================")
print("       JOBSENSE AI - SEMANTIC AI")
print("==========================================\n")


# ============================================================
# BASIC SEMANTIC TEST
# ============================================================

text1 = "Machine Learning"

text2 = "Predictive modeling using data"


score = calculate_semantic_similarity(
    text1,
    text2
)


print("Semantic Similarity Test")
print("------------------------------------------")

print("Text 1:", text1)
print("Text 2:", text2)

print("Similarity:", score, "%")


# ============================================================
# SKILL MATCHING TEST
# ============================================================

resume_skills = [
    "Python",
    "Machine Learning",
    "SQL",
    "Pandas",
    "Deep Learning"
]


jd_skills = [
    "Python",
    "Predictive Modeling",
    "SQL",
    "Data Analysis",
    "Neural Networks"
]


result = semantic_skill_matching(
    resume_skills,
    jd_skills
)


print("\n==========================================")
print("       SKILL LEVEL SEMANTIC MATCH")
print("==========================================\n")


print("Semantic Score:")
print(result["semantic_score"], "%")


print("\nMatched Skills:")

for skill in result["matched_skills"]:

    print(
        f"✓ {skill['jd_skill']} "
        f"→ {skill['resume_skill']} "
        f"({skill['similarity']}%)"
    )


print("\nMissing Skills:")

for skill in result["missing_skills"]:

    print("✗", skill)


print("\n==========================================")