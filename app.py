import streamlit as st
import google.genai as genai
from google.genai import types
st.set_page_config(
    page_title="Snap & Study",
    page_icon="📚"
)

st.title("📚 Snap & Study")
st.write("Upload your notes, question, or PDF and get a simple AI explanation.")

uploaded_file = st.file_uploader(
    "📂 Upload your study file",
    type=["jpg", "jpeg", "png", "pdf"]
)

if uploaded_file:
    file_bytes = uploaded_file.getvalue()

    # Show image preview
    if uploaded_file.type.startswith("image/"):
        st.image(uploaded_file, caption="Your uploaded image")

    # Show PDF information
    elif uploaded_file.type == "application/pdf":
        st.success("📄 PDF uploaded successfully!")
        st.write("File:", uploaded_file.name)
        st.write("Size:", f"{uploaded_file.size / (1024 * 1024):.2f} MB")

    if st.button("✨ Explain"):
        try:
            client = genai.Client(
                api_key=st.secrets["GEMINI_API_KEY"]
            )

            if uploaded_file.type == "application/pdf":
                mime_type = "application/pdf"
            else:
                mime_type = uploaded_file.type

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[
                    types.Part.from_bytes(
                        data=file_bytes,
                        mime_type=mime_type
                    ),
                    """
                    Explain this study material in very simple words.

                    Give:
                    1. Simple Explanation
                    2. Key Concepts
                    3. Important Points
                    4. Steps to Understand
                    5. Short Summary

                    Use beginner-friendly language.
                    """
                ]
            )

            st.subheader("📖 Explanation")
            st.write(response.text)

        except Exception as e:
            st.error("Something went wrong.")
            st.write(str(e))