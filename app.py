import os

import streamlit as st
from pypdf import PdfReader
from docx import Document
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai


# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "GEMINI_API_KEY is not configured. "
        "Please add it to your .env file."
    )
    st.stop()

client = genai.Client(api_key=api_key)


# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Documentation Generator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI-Powered Documentation Generator")
st.write("Create software project documentation using Gemini AI.")
st.divider()


# -----------------------------
# Project Details
# -----------------------------
st.header("📝 Project Details")

project_name = st.text_input("Project Name")

description = st.text_area("Project Description")

language = st.text_input("Programming Language")

features = st.text_area("Main Features")


# -----------------------------
# Upload Document
# -----------------------------
st.header("📂 Upload Document")

uploaded_file = st.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf", "docx"]
)

document_text = ""

if uploaded_file is not None:

    if uploaded_file.name.lower().endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                document_text += text + "\n"

    elif uploaded_file.name.lower().endswith(".docx"):

        doc = Document(uploaded_file)

        for paragraph in doc.paragraphs:
            document_text += paragraph.text + "\n"

    st.success("✅ Document uploaded successfully!")


# -----------------------------
# Pydantic Model
# -----------------------------
class ProjectData(BaseModel):
    name: str
    description: str
    language: str
    features: str


# -----------------------------
# Generate Documentation
# -----------------------------
if st.button("🚀 Generate Documentation"):

    if project_name == "" or description == "" or language == "":
        st.warning(
            "Please fill Project Name, Description and Programming Language."
        )

    else:

        project = ProjectData(
            name=project_name,
            description=description,
            language=language,
            features=features
        )

        # -----------------------------
        # Create AI Prompt
        # -----------------------------
        prompt = f"""
You are a professional software documentation writer.

Create clear and professional documentation for the following project.

Project Name:
{project.name}

Project Description:
{project.description}

Programming Language:
{project.language}

Main Features:
{project.features}

Uploaded Document:
{document_text[:5000] if document_text else "No document uploaded."}

Create documentation with these sections:

# Project Name

## 1. Project Overview

## 2. Programming Language

## 3. Main Features

## 4. Uploaded Document

## 5. Installation

## 6. How to Run

## 7. Future Enhancements

## 8. Conclusion

Make the documentation simple, clear, and suitable for a college software project.
"""

        # -----------------------------
        # Call Gemini AI
        # -----------------------------
        try:

            with st.spinner("🤖 Gemini is generating documentation..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                documentation = response.text

            st.success("✅ Documentation generated successfully!")

            # -----------------------------
            # Display Documentation
            # -----------------------------
            st.subheader("📄 Generated Documentation")

            st.markdown(documentation)

            # -----------------------------
            # Download Documentation
            # -----------------------------
            st.download_button(
                "⬇️ Download Documentation",
                documentation,
                file_name="documentation.md",
                mime="text/markdown"
            )

        except Exception as e:

            st.error("❌ Error while generating documentation.")
            st.write(str(e))