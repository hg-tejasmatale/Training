import os
import textwrap
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# ---------------------------
# Setup
# ---------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Quiz Generator (Gemini)", page_icon="🧠", layout="centered")

st.title("🧠 Theory Exam Quiz Generator")
st.caption("Powered by Google Gemini · Build MCQ quizzes in seconds")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    model_name = st.selectbox(
        "Model",
        ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash-thinking-exp"],
        index=1
    )
    num_questions = st.slider("Number of questions", min_value=5, max_value=20, value=5, step=1)
    show_answers = st.toggle("Show answers in output", value=True)
    st.markdown("---")
    st.info("Set your `GOOGLE_API_KEY` in a `.env` file.")

# Validate API key
if not API_KEY:
    st.error("Missing GOOGLE_API_KEY. Add it to your `.env` file and restart the app.")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name)

# Prompt template
PROMPT_TEMPLATE = textwrap.dedent("""\
    You are a teacher. Create a theory exam quiz on the topic: "{topic}".

    Requirements:
    - Exactly {num_qs} questions.
    - Each question on a new line, numbered (e.g., "1. ...").
    - For each question, include 4 options labeled A), B), C), D).
    - Only ONE option must be correct.
    - After the options, write: "Answer: <letter>" (e.g., Answer: B)
    - No extra commentary.
    - End with the token <END>
""")

# UI inputs
topic = st.text_input("Topic", value="Python", help="Enter any subject or niche (e.g., OOP in Python, Databases, Cloud basics).")

col1, col2 = st.columns([1, 1])
with col1:
    generate_btn = st.button("🚀 Generate Quiz", use_container_width=True)
with col2:
    clear_btn = st.button("🧹 Clear Output", use_container_width=True)

if clear_btn:
    st.session_state.pop("quiz_text", None)
    st.rerun()

# Generation
if generate_btn:
    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    prompt = PROMPT_TEMPLATE.format(topic=topic.strip(), num_qs=num_questions)

    with st.spinner("Generating quiz..."):
        try:
            resp = model.generate_content(prompt)
            text = (resp.text or "").strip()

            if not text:
                st.error("The model returned empty text. Try again.")
                st.stop()

            # Ensure <END> exists; if not, append
            if "<END>" not in text:
                text += "\n<END>"

            # Optionally remove answers in display (but keep a copy)
            display_text = text
            if not show_answers:
                # Remove lines that start with "Answer:"
                lines = [ln for ln in text.splitlines() if not ln.strip().lower().startswith("answer:")]
                display_text = "\n".join(lines)

            st.session_state["quiz_text"] = text
            st.session_state["quiz_text_display"] = display_text

        except Exception as e:
            st.error(f"Error while generating: {e}")
            st.stop()

# Output area
if "quiz_text_display" in st.session_state:
    st.subheader("📝 Generated Quiz")
    st.code(st.session_state["quiz_text_display"], language="markdown")

    # Download buttons
    colA, colB = st.columns(2)
    with colA:
        st.download_button(
            label="⬇️ Download (TXT)",
            data=st.session_state["quiz_text_display"],
            file_name=f"{topic.replace(' ', '_')}_quiz.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with colB:
        st.download_button(
            label="⬇️ Download (Full with Answers)",
            data=st.session_state["quiz_text"],
            file_name=f"{topic.replace(' ', '_')}_quiz_with_answers.txt",
            mime="text/plain",
            use_container_width=True,
        )

# Footer help
st.markdown("---")
with st.expander("❓ Tips & Notes"):
    st.markdown(
        """
        - If questions are not perfectly formatted, click **Generate** again—the model is probabilistic.
        - You can toggle answers visibility using the sidebar.
        - For tighter control, adjust the prompt to include specific sub-topics or cognitive levels (e.g., "Bloom's taxonomy: Understand/Apply").
        """
    )