import streamlit as st
import pandas as pd
from collections import Counter
import re

# 1. PAGE SETUP
st.set_page_config(page_title="AI Job Search Agent", page_icon="🎯", layout="wide")

# 2. HELPER FUNCTIONS
def extract_keywords(text):
    # Simple NLP: Remove symbols and get words longer than 3 chars
    words = re.findall(r'\w+', text.lower())
    # Filter out common "stop words"
    stop_words = {'the', 'and', 'with', 'from', 'this', 'that', 'your', 'will'}
    return [w for w in words if len(w) > 3 and w not in stop_words]

# 3. INTERFACE
st.title("🎯 AI Job Search & ATS Optimization Agent")
st.markdown("### Match your profile to remote job descriptions in seconds.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Your Resume / Profile")
    resume_text = st.text_area("Paste your LinkedIn 'About' or Resume text here:", height=300, placeholder="Paste here...")

with col2:
    st.subheader("📋 Job Description")
    job_text = st.text_area("Paste the Remote Job Description here:", height=300, placeholder="Paste here...")

# 4. ANALYSIS LOGIC
if st.button("🚀 Analyze Match Score"):
    if resume_text and job_text:
        with st.spinner("Agent is analyzing keywords and ATS compatibility..."):
            
            resume_keywords = set(extract_keywords(resume_text))
            job_keywords = set(extract_keywords(job_text))
            
            # Find matches and misses
            matched = resume_keywords.intersection(job_keywords)
            missing = job_keywords - resume_keywords
            
            # Calculate Score
            score = int((len(matched) / len(job_keywords)) * 100) if job_keywords else 0
            
            # Display Results
            st.divider()
            st.metric(label="ATS Match Score", value=f"{score}%")
            
            if score < 70:
                st.warning("⚠️ Warning: Your match score is low. Consider adding the missing keywords below.")
            else:
                st.success("✅ Strong Match! You are ready to apply with the DM template.")

            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.write("### ✅ Matched Keywords")
                st.write(", ".join(list(matched)[:15]))
            
            with res_col2:
                st.write("### ❌ Missing Keywords")
                st.write(", ".join(list(missing)[:15]))
                
            # 5. ACTIONABLE ADVICE
            st.info(f"**Agent Tip:** Update your 'Skills' section with: **{', '.join(list(missing)[:5])}** before submitting.")
    else:
        st.error("Please paste both your resume and the job description to begin.")
