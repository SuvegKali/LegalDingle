import os
import streamlit as st
from pypdf import PdfReader
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page setup
st.set_page_config(page_title="Migrant Worker Rights Assistant", page_icon="⚖️")
st.title("⚖️ India Migrant Worker Legal Assistant")
st.caption("Ask questions about labor laws, wages, legal rights, and working conditions.")

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Please add your GEMINI_API_KEY to the .env file or Streamlit secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Extract text from local PDF document
@st.cache_data
def load_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

# Load legal text
pdf_path = "migrant_law.pdf"
if not os.path.exists(pdf_path):
    st.error(f"Missing legal document: Please place '{pdf_path}' in your project directory.")
    st.stop()

legal_context = load_pdf_text(pdf_path)

# Define system prompt for legal grounding and language adaptivity
system_instruction = f"""
You are an empathetic, plain-language legal assistant designed to help migrant workers in India understand their rights.
Base your answers strictly on the legal document text provided below.

Rules:
1. Simplify legal terminology into short, practical advice.
2. Automatically detect and respond in the language used by the user (e.g., Hindi, Bengali, Odia, Tamil, English, etc.).
3. If a user asks a question not addressed in the legal document, state clearly: "This document does not provide specific details on that topic."

--- LEGAL DOCUMENT CONTEXT ---
{legal_context}
"""

# Manage conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process user input
if prompt := st.chat_input("Ask about minimum wage, working hours, safety, or legal aid..."):
    # Save & display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Analyzing legal document..."):
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2,
                )
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})