import streamlit as st
from pypdf import PdfReader
from docx import Document
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Documentation Generator",
    page_icon="📚"
)

st.title("📚 AI-Powered Documentation Generator")
st.write("Create software project documentation easily.")

st.divider()

st.header("📝 Project Details")

project_name = st.text_input("Project Name")

description = st.text_area("Project Description")

language = st.text_input("Programming Language")

features = st.text_area("Main Features")

st.header("📂 Upload Document")

uploaded_file = st.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf", "docx"]
)

document_text = ""

if uploaded_file is not None:

    if uploaded_file.name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                document_text += text + "\n"

    elif uploaded_file.name.endswith(".docx"):

        doc = Document(uploaded_file)

        for paragraph in doc.paragraphs:
            document_text += paragraph.text + "\n"

    st.success("Document uploaded successfully!")


class ProjectData(BaseModel):
    name: str
    description: str
    language: str
    features: str


if st.button("🚀 Generate Documentation"):

    if project_name == "" or description == "" or language == "":
        st.warning("Please fill Project Name, Description and Programming Language.")

    else:

        project = ProjectData(
            name=project_name,
            description=description,
            language=language,
            features=features
        )

        st.success("✅ Documentation generated!")

        st.subheader("📄 Generated Documentation")

        st.markdown("# " + project.name)

        st.markdown("## 1. Project Overview")
        st.write(project.description)

        st.markdown("## 2. Programming Language")
        st.write(project.language)

        st.markdown("## 3. Main Features")
        st.write(project.features)

        st.markdown("## 4. Uploaded Document")

        if document_text:
            st.write(document_text[:3000])
        else:
            st.write("No document was uploaded.")

        st.markdown("## 5. Installation")

        st.code(
            "pip install -r requirements.txt",
            language="bash"
        )

        st.markdown("## 6. How to Run")

        st.code(
            "streamlit run app.py",
            language="bash"
        )

        st.markdown("## 7. Future Enhancements")

        st.write("- AI-based documentation generation")
        st.write("- Automatic README generation")
        st.write("- Code analysis")
        st.write("- API documentation")

        st.markdown("## 8. Conclusion")

        st.write(
            "This application helps developers create "
            "software project documentation quickly."
        )

        documentation = (
            "# " + project.name + "\n\n"
            "## 1. Project Overview\n\n"
            + project.description + "\n\n"
            "## 2. Programming Language\n\n"
            + project.language + "\n\n"
            "## 3. Main Features\n\n"
            + project.features + "\n\n"
            "## 4. Uploaded Document\n\n"
            + (document_text[:3000] if document_text else "No document uploaded.")
        )

        st.download_button(
            "⬇️ Download Documentation",
            documentation,
            file_name="documentation.md",
            mime="text/markdown"
        )