# 🤖 AI Talent Scouting Agent

## 🚀 Overview

The AI Talent Scouting Agent is an intelligent recruitment assistant that automates the end-to-end hiring pipeline. It parses job descriptions, matches candidates based on skills and experience, simulates candidate engagement, and generates an explainable ranked shortlist.

Unlike traditional systems that rely only on keyword matching, this solution incorporates candidate intent and provides transparent, recruiter-like decision-making.

---

## 🧠 Key Features

* 📌 **Job Description Parsing**
  Converts unstructured job descriptions into structured data (role, skills, experience)

* 👥 **Candidate Matching Engine**
  Matches candidates based on skill overlap and experience alignment

* 💬 **AI Candidate Engagement**
  Simulates realistic conversations to evaluate candidate interest

* 📊 **Interest Scoring System**
  Classifies candidate intent (high, moderate, low) from responses

* 🏆 **Ranking & Recommendation**
  Combines match score and interest score to rank candidates

* 🔍 **Explainability**
  Shows matched skills, missing skills, and reasoning for each candidate

* ⚡ **AI Decision Pipeline**
  Displays step-by-step workflow of the agent

---

## 🏗️ Architecture

```
Job Description Input
        ↓
JD Parsing Agent (LLM)
        ↓
Candidate Dataset (JSON)
        ↓
Matching Engine (Skills + Experience)
        ↓
Engagement Agent (Conversation Simulation)
        ↓
Interest Scoring
        ↓
Ranking Engine
        ↓
Streamlit UI Dashboard
```

---

## ⚙️ Scoring Logic

Final Score is calculated as:

**Final Score = 0.6 × Match Score + 0.4 × Interest Score**

### Match Score:

* Skill Match (80%)
* Experience Alignment (20%)

### Interest Score:

* 100 → Highly Interested
* 70 → Moderately Interested
* 50 → Neutral
* 0 → Not Interested

---

## 🧪 Sample Input

```
Looking for a Data Analyst with SQL, Excel, and Data Visualization skills.
```

---

## 📊 Sample Output

* Ranked list of candidates
* Match scores and interest scores
* AI-generated candidate responses
* Hiring recommendations
* Explainable reasoning for each candidate

---

## 💻 Tech Stack

* Python
* Streamlit
* OpenAI API
* Pandas
* python-dotenv

---

## ⚙️ Setup & Installation

```bash
# Clone the repository
git clone https://github.com/your-username/talent-scouting-agent.git

# Navigate to project folder
cd talent-scouting-agent

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your API key
# OPENAI_API_KEY=your-api-key

# Generate dataset
python process_data.py

# Run the application
streamlit run app.py
```

---

## 🌐 Demo

👉 Demo Video: *(Add your link here)*
👉 GitHub Repository: *(This repository)*

---

## 💡 Key Highlights

* End-to-end recruitment automation
* Combines matching + engagement + ranking
* Realistic candidate simulation
* Explainable AI decisions
* Adapts dynamically to different job roles

---

## 🚀 Future Improvements

* Multi-agent orchestration
* Real-time resume ingestion
* Integration with hiring platforms
* Semantic skill matching
* Candidate memory & follow-ups

---

## 🏆 Conclusion

The AI Talent Scouting Agent demonstrates how intelligent systems can transform recruitment workflows by making them faster, smarter, and aligned with real-world hiring decisions.

---
