import streamlit as st
import smtplib
from email.mime.text import MIMEText
import google.genai as genai
from google.genai import types

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

    if uploaded_file.type.startswith("image/"):
        st.image(
            uploaded_file,
            caption="Your uploaded image"
        )

    elif uploaded_file.type == "application/pdf":
        st.success("📄 PDF uploaded successfully!")
        st.write("File:", uploaded_file.name)
        st.write(
            "Size:",
            f"{uploaded_file.size / (1024 * 1024):.2f} MB"
        )

    if st.button("✨ Explain"):

        try:
            client = genai.Client(
                api_key=st.secrets["GEMINI_API_KEY"]
            )

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[
                    types.Part.from_bytes(
                        data=file_bytes,
                        mime_type=uploaded_file.type
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

            explanation = response.text

            st.subheader("📖 Explanation")
            st.write(explanation)

            st.divider()

            st.subheader("📧 Send Explanation by Email")

            recipient_email = st.text_input(
                "Enter email address"
            )

            if st.button("📨 Send Email"):

                try:
                    sender_email = st.secrets["GMAIL_ADDRESS"]
                    app_password = st.secrets["GMAIL_APP_PASSWORD"]

                    message = MIMEText(
                        explanation,
                        "plain",
                        "utf-8"
                    )

                    message["Subject"] = (
                        "Snap & Study - AI Explanation"
                    )

                    message["From"] = sender_email
                    message["To"] = recipient_email

                    with smtplib.SMTP(
                        "smtp.gmail.com",
                        587
                    ) as server:

                        server.starttls()

                        server.login(
                            sender_email,
                            app_password
                        )

                        server.send_message(message)

                    st.success(
                        "✅ Explanation sent successfully!"
                    )

                except Exception as e:

                    st.error(
                        "❌ Email could not be sent."
                    )

                    st.write(str(e))

        except Exception as e:

            st.error(
                "❌ Something went wrong."
            )

            st.write(str(e))