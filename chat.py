import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ✅ Set the page config at the very top
st.set_page_config(page_title="👮 Bengaluru Police Well-being Chatbot", layout="wide")

# Load environment variables
load_dotenv()

# Get the API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("API key not found. Please check your .env file or set the environment variable.")
    st.stop()

# Initialize Gemini model with API key
genai.configure(api_key=api_key)

# ✅ System prompt handling
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are a well-being officer for the Bengaluru Police. "
        "Your goal is to provide mental health support, stress management advice, "
        "and helpful resources to the officers."
    )

# ✅ Sidebar for setting system prompt
st.sidebar.subheader("📝 System Prompt")
new_prompt = st.sidebar.text_area(
    "Set the system prompt:",
    value=st.session_state.system_prompt,
    height=150,
)

# Update system prompt if changed
if new_prompt != st.session_state.system_prompt:
    st.session_state.system_prompt = new_prompt

# Initialize the model with the system prompt
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=st.session_state.system_prompt
)

def get_response(user_input):
    try:
        response = model.generate_content(user_input).text
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# ✅ Main app interface
st.title("👮 Bengaluru Police Well-being Chatbot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message...")
if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get model response
    response = get_response(user_input)
    
    # Display model response
    with st.chat_message("assistant"):
        st.markdown(response)
        
    # Save model response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
