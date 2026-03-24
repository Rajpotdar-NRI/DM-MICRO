def skill_gap(resume_skills, required_skills):

    # Prevent division by zero
    if len(required_skills) == 0:
        return [], [], 0

    resume_set = set(resume_skills)
    required_set = set(required_skills)

    matched = list(resume_set & required_set)

    missing = list(required_set - resume_set)

    score = (len(matched) / len(required_skills)) * 100

    return matched, missing, score