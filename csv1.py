import pandas as pd
import random
from faker import Faker

# Use Indian-style names (optional but better)
fake = Faker('en_IN')

# Job roles and required skills
roles = {
    "Data Analyst": ["python", "sql", "data analysis", "excel"],
    "Data Scientist": ["python", "machine learning", "sql", "data analysis"],
    "Software Engineer": ["java", "c++", "linux", "aws"],
    "Web Developer": ["html", "css", "javascript"],
    "System Administrator": ["linux", "aws", "python"],
    "AI Engineer": ["python", "machine learning", "c++", "aws"]
}

# Extra skills pool
extra_skills_pool = [
    "excel", "communication", "react", "django",
    "numpy", "pandas", "git", "linux", "aws",
    "tableau", "power bi"
]

data = []

for i in range(9999):
    role = random.choice(list(roles.keys()))
    req_skills = roles[role]

    # Match % between 27% and 94%
    match_ratio = random.uniform(0.27, 0.94)

    # Calculate matched skills
    num_match = max(1, int(match_ratio * len(req_skills)))
    matched_skills = random.sample(req_skills, num_match)

    # Add random extra skills
    extra_skills = random.sample(extra_skills_pool, random.randint(1, 3))

    # Combine skills
    final_skills = list(set(matched_skills + extra_skills))

    data.append({
        "candidate_id": 1000 + i,
        "candidate_name": fake.name(),
        "job_role": role,
        "education": random.choice(["B.Tech", "MCA", "B.Sc", "M.Tech"]),
        "experience_years": random.randint(0, 10),
        "resume_skills": ", ".join(final_skills)
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save CSV
df.to_csv("candidate_dataset_9999.csv", index=False)

print("✅ CSV generated successfully!")