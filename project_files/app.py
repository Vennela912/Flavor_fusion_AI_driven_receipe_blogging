import streamlit as st
import google.generativeai as genai
import random
from dotenv import load_dotenv
import os

# -------------------------------------------------
# Load API Key
# -------------------------------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# -------------------------------------------------
# Generation Configuration
# -------------------------------------------------
generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config
)

# -------------------------------------------------
# ✨ MODERN STYLING
# -------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1f1c2c, #928dab);
        font-family: 'Segoe UI', sans-serif;
        color: white;
    }

    .main-heading {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 10px;
        background: linear-gradient(90deg, #ff9966, #ff5e62);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-heading {
        text-align: center;
        font-size: 20px;
        margin-bottom: 30px;
        color: #f1f1f1;
    }

    .joke-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
        font-style: italic;
        color: #ffd369;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .recipe-output {
        background: rgba(0, 0, 0, 0.4);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        margin-top: 10px;
        color: white;
        line-height: 1.6;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff512f, #dd2476);
        color: white;
        font-size: 18px;
        padding: 10px 25px;
        border-radius: 25px;
        border: none;
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(255, 81, 47, 0.6);
    }

    div.stTextInput > div > input,
    div.stNumberInput > div > input {
        background: rgba(255,255,255,0.15) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        padding: 8px !important;
    }

    div.stTextInput > label,
    div.stNumberInput > label {
        color: white !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Page Heading
# -------------------------------------------------
st.markdown(
    '<div class="main-heading">RecipeMaster: AI-Powered Recipe Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-heading">🤖 Hello! I’m RecipeMaster, your friendly AI chef. Let’s create something delicious!</div>',
    unsafe_allow_html=True
)

# -------------------------------------------------
# Joke Function
# -------------------------------------------------
def get_joke():
    jokes = [
        "Why don't programmers like nature? It has too many bugs.",
        "Why do Java developers wear glasses? Because they don't see sharp.",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "Why did the developer go broke? Because he used up all his cache.",
        "Why was the computer cold? It left its Windows open."
    ]
    return random.choice(jokes)

# -------------------------------------------------
# Recipe Generation Function
# -------------------------------------------------
def recipe_generation(user_input, word_count):

    st.markdown(
        f'<div class="joke-box">While I work on your recipe, here’s a joke for you:<br><b>{get_joke()}</b></div>',
        unsafe_allow_html=True
    )

    try:
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        f"Write a detailed recipe about {user_input} in approximately {word_count} words. Include title, ingredients, steps, and cooking tips."
                    ],
                }
            ]
        )

        response = chat_session.send_message(user_input)

        st.success("✅ Your recipe is ready!")

        st.markdown(
            f'<div class="recipe-output">{response.text}</div>',
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Error generating recipe: {e}")

# -------------------------------------------------
# Input Section
# -------------------------------------------------
user_input = st.text_input("Enter recipe topic")
word_count = st.number_input(
    "Enter word count",
    min_value=100,
    max_value=1000,
    value=300
)

if st.button("Generate Recipe"):
    if user_input:
        recipe_generation(user_input, word_count)
    else:
        st.warning("Please enter a recipe topic!")
