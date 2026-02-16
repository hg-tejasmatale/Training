import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# -----------------------------
# 1. Load Models
# -----------------------------
@st.cache_resource
def load_models():
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    llm = pipeline(
        "text-generation",
        model="distilgpt2",
        max_new_tokens=150
    )
    return embed_model, llm

embed_model, llm = load_models()

# -----------------------------
# 2. Knowledge Base (Documents)
# -----------------------------
docs = [
    "LangChain helps developers build applications using large language models.",
    "RAG improves LLM accuracy by retrieving relevant external information.",
    "Sentence embeddings capture semantic meaning of text.",
    "Transformers use attention mechanisms to process language.",
    "Vector databases store embeddings for fast similarity search."
]

doc_embeddings = embed_model.encode(docs)

# -----------------------------
# 3. Retriever Function
# -----------------------------
def retrieve(query, top_k=2):
    query_emb = embed_model.encode([query])[0]
    scores = np.dot(doc_embeddings, query_emb)
    top_indices = np.argsort(scores)[-top_k:][::-1]
    return [docs[i] for i in top_indices]

# -----------------------------
# 4. RAG Response Generator
# -----------------------------
def generate_answer(query):
    retrieved_docs = retrieve(query)
    context = "\n".join(retrieved_docs)

    prompt = f"""
You are an AI assistant.
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm(prompt)[0]["generated_text"]
    return response.split("Answer:")[-1].strip(), retrieved_docs

# -----------------------------
# 5. Streamlit UI
# -----------------------------
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

st.title("🤖 RAG Chatbot (GenAI + Deep Learning)")
st.write("Ask questions based on the internal knowledge base.")

user_query = st.text_input("Enter your question:")

if user_query:
    with st.spinner("Thinking..."):
        answer, sources = generate_answer(user_query)

    st.subheader("🧠 Answer")
    st.write(answer)

    st.subheader("📚 Retrieved Context")
    for src in sources:
        st.markdown(f"- {src}")
