import streamlit as st
from agents import run_pipeline

st.set_page_config(page_title="Talent Scouting Agent", layout="wide")

# 🎨 HEADER
st.markdown("""
# 🤖 Talent Scouting Agent
### 🚀 AI-powered recruitment assistant
""")

# 📥 INPUT SECTION
st.markdown("### 📥 Enter Job Description")
jd = st.text_area("", height=150, placeholder="Paste job description here...")

# 🚀 RUN BUTTON
if st.button("🚀 Run Agent"):

    jd_data, df, logs = run_pipeline(jd)

    # 🧠 AGENT THINKING
    st.markdown("## 🧠 Agent Workflow")
    cols = st.columns(len(logs))
    for i, log in enumerate(logs):
        cols[i].info(log)

    st.divider()

    # 📌 PARSED JD + SUMMARY SIDE BY SIDE
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 📌 Parsed Job Description")
        st.json(jd_data)

    with col2:
        st.markdown("## 📊 Summary")
        st.metric("Total Candidates", len(df))
        st.metric("Top Score", df["final"].max())
        st.metric("Avg Score", round(df["final"].mean(), 2))

    st.divider()

    # 🏆 TOP CANDIDATES (CARDS STYLE)
    st.markdown("## 🏆 Top Candidates")

    top_3 = df.head(3)
    cols = st.columns(3)

    for i, (_, row) in enumerate(top_3.iterrows()):
        with cols[i]:
            if row["final"] > 75:
                st.success(f"""
### {row['name']}
**Final Score:** {row['final']}
Match: {row['match']} | Interest: {row['interest']}
""")
            elif row["final"] > 60:
                st.warning(f"""
### {row['name']}
**Final Score:** {row['final']}
Match: {row['match']} | Interest: {row['interest']}
""")
            else:
                st.error(f"""
### {row['name']}
**Final Score:** {row['final']}
Match: {row['match']} | Interest: {row['interest']}
""")

    st.divider()

    # 📊 FULL TABLE
    st.markdown("## 📊 All Candidates")
    st.dataframe(df[["name", "match", "interest", "final"]], use_container_width=True)

    st.divider()

    # 💬 DETAILED INSIGHTS
    st.markdown("## 💬 Candidate Insights")

    for _, row in df.iterrows():
        with st.expander(f"{row['name']} (Score: {row['final']})"):

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🧠 Match Analysis")
                st.json(row["reason"])

            with col2:
                st.markdown("### 💬 Candidate Response")
                st.write(row["conversation"])

            st.markdown("---")

            st.markdown(f"""
💡 **Insight:**  
Matches **{len(row['reason']['matched_skills'])} key skills** and shows  
**{'high' if row['interest'] > 80 else 'moderate' if row['interest'] > 50 else 'low'} interest**
""")

            # 🎯 FINAL DECISION
            if row["final"] > 75:
                st.success("✅ Strong Hire Recommendation")
            elif row["final"] > 60:
                st.warning("⚖️ Consider Further Evaluation")
            else:
                st.error("❌ Not a Good Fit")