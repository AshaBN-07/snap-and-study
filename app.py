import streamlit as st
from google import genai
from google.genai import types
import time

st.set_page_config(
    page_title="Snap & Study",
    page_icon="📚"
)

st.title("📚 Snap & Study")
st.write(
    "Upload your notes, question, or PDF and get a simple AI explanation."
)

uploaded_file = st.file_uploader(
    "📂 Upload your study file",
    type=["jpg", "jpeg", "png", "pdf"]
)

if uploaded_file:

    file_bytes = uploaded_file.getvalue()

    # Image preview
    if uploaded_file.type.startswith("image/"):
        st.image(
            uploaded_file,
            caption="Your uploaded image"
        )

    # PDF information
    elif uploaded_file.type == "application/pdf":
        st.success("📄 PDF uploaded successfully!")
        st.write("File:", uploaded_file.name)
        st.write(
            "Size:",
            f"{uploaded_file.size / (1024 * 1024):.2f} MB"
        )

    # Explain button
    if st.button("✨ Explain", type="primary"):

        try:
            # Get API key from Streamlit Secrets
            api_key = st.secrets["GEMINI_API_KEY"]

            client = genai.Client(
                api_key=api_key
            )

            # File type
            mime_type = uploaded_file.type

            # Prompt
            prompt = """
Explain this study material in very simple words.

Give:

1. Simple Explanation
2. Key Concepts
3. Important Points
4. Steps to Understand
5. Short Summary

Use beginner-friendly language.
"""

            with st.spinner("🤖 AI is reading your study material..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        types.Part.from_bytes(
                            data=file_bytes,
                            mime_type=mime_type
                        ),
                        prompt
                    ]
                )

            # Display answer
            st.subheader("📖 Explanation")

            if response.text:
                st.write(response.text)
            else:
                st.warning("⚠️ Gemini did not return an explanation.")

        except KeyError:
            st.error("❌ GEMINI_API_KEY is missing.")

            st.info(
                "Go to Streamlit → Manage app → Settings → Secrets "
                "and add your Gemini API key."
            )

        except Exception as e:

            error_text = str(e)

            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

                st.error("⏳ Gemini API quota exceeded.")

                st.warning(
                    "Your Gemini free-tier request limit has been reached. "
                    "Please wait and try again later."
                )

                st.info(
                    "⚠️ Do not keep pressing Explain repeatedly. "
                    "That can trigger the rate limit again."
                )

            else:
                st.error("❌ Something went wrong.")
                st.code(error_text)