import streamlit as st
import requests

# ======================================
# Backend URL
# ======================================
BACKEND_URL = "https://ai-resume-assistant-g16j.onrender.com"

# ======================================
# Page Configuration
# ======================================
st.set_page_config(
    page_title="AI Resume Assistant",
    page_icon="📄",
    layout="wide"
)

# ======================================
# Custom CSS
# ======================================
st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

section[data-testid="stSidebar"]{
    width:280px;
}

</style>
""", unsafe_allow_html=True)

# ======================================
# Session State
# ======================================
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ======================================
# Header
# ======================================
st.title("AI Resume Assistant")

st.caption(
    "Analyze your resume using Retrieval-Augmented Generation (RAG) and OpenAI."
)

# ======================================
# Sidebar
# ======================================
with st.sidebar:

    st.header("Resume Upload")

    uploaded_file = st.file_uploader(
        "Choose Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file:

        if st.button("Upload Resume", use_container_width=True):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            with st.spinner("Uploading resume..."):

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/upload",
                        files=files
                    )

                    if response.status_code == 200:

                        st.session_state.uploaded = True
                        st.success("Resume uploaded successfully.")

                    else:

                        st.error("Upload failed.")

                except:

                    st.error("Backend server is not running.")

    st.divider()

    st.subheader("Resume Status")

    if st.session_state.uploaded:

        st.success("Resume uploaded successfully")

    else:

        st.warning("No resume uploaded")

    st.divider()

    st.subheader("About")

    st.info(
        """
This application uses Retrieval-Augmented Generation (RAG)
to answer questions based only on the uploaded resume.
"""
    )

    st.divider()

    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ======================================
# Main Area
# ======================================

st.subheader("Ask Questions About Your Resume")

question = st.text_input(
    "Enter your question",
    placeholder="Example: Summarize my resume"
)

ask = st.button(
    "Ask AI",
    use_container_width=True
)

# ======================================
# Ask AI
# ======================================

if ask:

    if not st.session_state.uploaded:

        st.warning("Please upload your resume first.")

    elif question.strip() == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("Analyzing your resume..."):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={
                        "question": question
                    }
                )

                if response.status_code == 200:

                    answer = response.json()["answer"]

                    st.session_state.chat_history.append(
                        {
                            "question": question,
                            "answer": answer
                        }
                    )

                else:

                    st.error("Unable to generate a response.")

            except:

                st.error("Backend server is not running.")

# ======================================
# Conversation
# ======================================

if st.session_state.chat_history:

    st.divider()

    st.header("Conversation")

    for chat in reversed(st.session_state.chat_history):

       with st.container(border=True):

        st.markdown(f"**Question**")

        st.write(chat["question"])

        st.divider()

        st.markdown("**Answer**")

        st.markdown(chat["answer"])

        st.write("")

# ======================================
# Footer
# ======================================

st.divider()

st.caption(
    "Powered by FastAPI • LangChain • OpenAI • FAISS • Streamlit"
)