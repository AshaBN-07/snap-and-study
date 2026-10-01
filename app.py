import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Snap & Study",
    page_icon="📚"
)

st.title("📚 Snap & Study")
st.write("Upload your notes or question and get a simple AI explanation.")

uploaded_file = st.file_uploader(
    "📷 Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    st.image(uploaded_file, caption="Your uploaded image")

    if st.button("✨ Explain"):
        try:
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

            image_bytes = uploaded_file.getvalue()

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=uploaded_file.type
                    ),
                    """Explain this study image in very simple words.
Give:
1. Simple explanation
2. Key concepts
3. Important points
4. Steps to understand it
"""
                ]
            )

            st.subheader("📖 Explanation")
            st.write(response.text)

        except Exception as e:
            st.error("Something went wrong. Please check your API key.")