import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Prompt Engineering Playground", layout="centered")

st.write("Streamlit is working ✅")

# Read Groq API key from environment
api_key = os.getenv("GROQ_API_KEY")
demo_mode = False
client = None

if api_key and api_key.strip():
    try:
        client = Groq(api_key=api_key)
        st.success("✅ Groq API key loaded")
    except Exception:
        st.warning("⚠️ Groq API key invalid — running in demo mode")
        demo_mode = True
else:
    st.warning("No GROQ_API_KEY found — running in demo mode")
    demo_mode = True

st.title("🧠 Prompt Engineering Playground")
st.write("Explore different prompting techniques using Generative AI")

prompt_type = st.selectbox(
    "Choose Prompt Technique",
    ["Zero-shot Prompting", "Few-shot Prompting", "Chain-of-Thought Prompting", "Role-based Prompting"]
)

user_input = st.text_area("Enter your question or task:")

def generate_prompt(prompt_type, user_input):
    if prompt_type == "Zero-shot Prompting":
        return user_input
    elif prompt_type == "Few-shot Prompting":
        return f"""Q: What is AI?
A: Artificial Intelligence is the simulation of human intelligence.

Q: What is Machine Learning?
A: Machine Learning is a subset of AI.

Q: {user_input}
A:"""
    elif prompt_type == "Chain-of-Thought Prompting":
        return f"{user_input}\nLet's think step by step."
    elif prompt_type == "Role-based Prompting":
        return f"You are an expert computer science professor. Answer clearly:\n{user_input}"

if st.button("Generate Response"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        prompt = generate_prompt(prompt_type, user_input)
        if demo_mode or client is None:
            st.info("📝 Demo Mode — no API request made")
            st.success("Demo response: " + (prompt[:200] + "..." if len(prompt) > 200 else prompt))
        else:
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.subheader("AI Response:")
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error(f"API Error: {str(e)}")
