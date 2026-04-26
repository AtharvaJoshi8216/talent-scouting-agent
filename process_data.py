import pandas as pd
import random
import json

print("Loading dataset...")
df = pd.read_csv("resume_dataset_2.csv")

# Select required columns
df = df[["Name", "Years_Experience", "Job_Role", "Skills"]]

# Drop missing values
df = df.dropna()

# Clean skills
df["Skills"] = df["Skills"].apply(
    lambda x: [s.strip() for s in str(x).split(",")]
)

# Convert experience
df["Years_Experience"] = pd.to_numeric(df["Years_Experience"], errors="coerce")
df = df.dropna(subset=["Years_Experience"])
df["Years_Experience"] = df["Years_Experience"].astype(int)

# Select 30 candidates
df = df.sample(50, random_state=42)
df = df.drop_duplicates(subset=["Skills"])
df = df.head(30)

# Add synthetic fields
locations = ["Pune", "Bangalore", "Mumbai", "Hyderabad"]
salaries = ["6 LPA", "8 LPA", "10 LPA", "12 LPA"]
notice = ["15 days", "30 days", "60 days"]
personalities = [
    "growth-focused",
    "prefers stability",
    "open to startups",
    "seeks high salary"
]

df["location"] = df["Name"].apply(lambda _: random.choice(locations))
df["expected_salary"] = df["Name"].apply(lambda _: random.choice(salaries))
df["notice_period"] = df["Name"].apply(lambda _: random.choice(notice))
df["personality"] = df["Name"].apply(lambda _: random.choice(personalities))

# Convert to JSON
candidates = []

for _, row in df.iterrows():
    candidates.append({
        "name": row["Name"],
        "skills": row["Skills"],
        "experience": row["Years_Experience"],
        "role": row["Job_Role"],
        "location": row["location"],
        "expected_salary": row["expected_salary"],
        "notice_period": row["notice_period"],
        "personality": row["personality"]
    })

# Save
with open("data.json", "w") as f:
    json.dump(candidates, f, indent=2)

print("✅ data.json created!")