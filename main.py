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


def extract_text_from_pdf(file_stream):
    pdf_reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text


if analyze_button and uploaded_file:
    try:
        file_stream = io.BytesIO(uploaded_file.read())
        file_content = extract_text_from_pdf(file_stream)

        if not file_content.strip():
            st.error("The uploaded file is empty or could not be read. Please upload a valid PDF file.")
            st.stop()

        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}
        
        Resume content:
        {file_content}
        
        Please provide your analysis in a clear, structured format with specific recommendations."""

        client = OpenAI(api_key=OpenAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        st.markdown("### Analysis Results")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occurred while processing the resume: {str(e)}")
