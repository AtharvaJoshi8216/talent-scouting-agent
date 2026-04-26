import json
import pandas as pd
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL
import re

client = OpenAI(api_key=OPENAI_API_KEY)


# 🔹 JD PARSER (FIXED + ROBUST)
def parse_jd(jd_text):
    prompt = f"""
    You are an expert recruiter.

    Extract structured info from this job description.

    Return ONLY valid JSON:

    {{
      "role": "string",
      "skills": ["skill1", "skill2"],
      "experience": number
    }}

    Job Description:
    {jd_text}
    """

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = res.choices[0].message.content.strip()

    # Clean markdown if present
    content = re.sub(r"```json|```", "", content).strip()

    try:
        return json.loads(content)
    except:
        print("Parsing failed:", content)
        return {"role": "Data Scientist", "skills": ["Python"], "experience": 2}


# 🔹 LOAD DATA
def load_candidates():
    with open("data.json", "r") as f:
        return json.load(f)


# 🔹 MATCH SCORE (UPGRADED)
def match_score(jd, cand):
    jd_skills = set([s.lower() for s in jd["skills"]])
    cand_skills = set([s.lower() for s in cand["skills"]])

    matched = jd_skills & cand_skills
    missing = jd_skills - cand_skills

    skill_score = (len(matched) / max(len(jd_skills), 1)) * 80
    exp_diff = abs(jd["experience"] - cand["experience"])
    exp_score = max(0, 20 - exp_diff * 3)

    total = skill_score + exp_score

    reason = {
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "experience_gap": exp_diff
    }

    return total, reason


# 🔹 CONVERSATION (REALISTIC)
def conversation(cand, jd):
    prompt = f"""
    You are {cand['name']}, a realistic job candidate.

    Profile:
    Skills: {cand['skills']}
    Experience: {cand['experience']} years
    Salary Expectation: {cand['expected_salary']}
    Personality: {cand['personality']}

    Recruiter asks:
    "Are you interested in {jd['role']} role?"

    Respond naturally:
    - Mention salary, growth, or role fit
    - Sound human
    - Max 2 lines
    """

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


# 🔹 INTEREST SCORE (YOUR UPDATED LOGIC)
def interest_score(text):
    text = text.lower()

    # 🔴 Strong negative signals
    if any(word in text for word in [
        "not interested",
        "not a fit",
        "different field",
        "not aligned",
        "not my area"
    ]):
        return 0

    # 🟡 Neutral / unsure
    elif any(word in text for word in [
        "depends",
        "maybe",
        "open to discuss"
    ]):
        return 50

    # 🟢 Strong positive
    elif any(word in text for word in [
        "very interested",
        "excited",
        "perfect fit"
    ]):
        return 100

    # 🟢 Default (moderate interest)
    else:
        return 70


# 🔹 MAIN PIPELINE
def run_pipeline(jd_text):
    logs = []

    logs.append("🔍 Parsing job description...")
    jd = parse_jd(jd_text)

    jd["skills"] = [
    s.replace("(Tableau or Power BI)", "")
     .replace("Tableau or Power BI", "Data Visualization")
     .strip()
    for s in jd["skills"]
    ]

    logs.append("👥 Loading candidates...")
    candidates = load_candidates()

    logs.append("⚖️ Matching & engaging candidates...")

    results = []

    for cand in candidates:
        m_score, reason = match_score(jd, cand)
        convo = conversation(cand, jd)
        i_score = interest_score(convo)

        final = 0.6 * m_score + 0.4 * i_score

        results.append({
            "name": cand["name"],
            "match": round(m_score, 2),
            "interest": i_score,
            "final": round(final, 2),
            "reason": reason,
            "conversation": convo
        })

    df = pd.DataFrame(results).sort_values(by="final", ascending=False)

    logs.append("📊 Ranking completed!")

    return jd, df, logs