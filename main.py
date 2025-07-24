import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI resume analyzer", page_icon="📃", layout="centered")

st.title("AI Resume Analyzer 📃")
st.markdown("Upload your resume in PDF format to get insights and suggestions tailored to your career goals.")

OpenAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your resume (pdf)", type="pdf")
job_role = st.text_input("Enter the job role you are targeting (optional): ")

analyze_button = st.button("Analyze Resume")

if analyze_button: 
    st.write("Analyzing your resume... Please wait.")