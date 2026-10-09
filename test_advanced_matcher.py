from app.services.matcher import calculate_match


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


result = calculate_match(
    resume_skills,
    jd_skills
)


print("\n==========================================")
print("       JOBSENSE AI - ADVANCED MATCH")
print("==========================================\n")


print("Final Match Score:")
print(result["match_score"], "%")


print("\nKeyword Score:")
print(result["keyword_score"], "%")


print("\nSemantic Score:")
print(result["semantic_score"], "%")


print("\nExact Matched Skills:")

for skill in result["matched_skills"]:
    print("✓", skill)


print("\nSemantic Matched Skills:")

for skill in result["semantic_matched_skills"]:
    print(
        f"✓ {skill['jd_skill']} "
        f"→ {skill['resume_skill']} "
        f"({skill['similarity']}%)"
    )


print("\nMissing Skills:")

for skill in result["semantic_missing_skills"]:
    print("✗", skill)


print("\n==========================================")