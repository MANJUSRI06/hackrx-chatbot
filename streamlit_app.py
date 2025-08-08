import streamlit as st
import requests

st.set_page_config(page_title="Policy QA Bot", layout="centered")
st.title("📝 Policy Chatbot")

# Only ask questions
questions = st.text_area("💬 Enter your questions (one per line)", height=150)

# Default PDF URL
PDF_URL = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"

if st.button("🔍 Ask the Bot") and questions.strip():
    payload = {
        "documents": PDF_URL,
        "questions": questions.strip().splitlines()
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/hackrx/run",
            headers={
                "Authorization": "Bearer d00beb2e99cc85dd8aad42430e5ab20b916e5df2abd096b8401a3eac074fcd35",
                "Content-Type": "application/json"
            },
            json=payload
        )

        if response.status_code == 200:
            st.success("✅ Answers")
            for q, a in zip(payload["questions"], response.json()["answers"]):
                st.markdown(f"**Q:** {q}\n\n> {a}")
        else:
            st.error(f"❌ Failed! Status code: {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.error("⚠️ Something went wrong!")
        st.exception(e)

elif not questions.strip():
    st.warning("✍️ Please enter at least one question.")
