# app.py

import streamlit as st
import google.generativeai as genai
import json
import os 
from dotenv import load_dotenv
load_dotenv()
def load_css():
    st.markdown("""<style>
            /* --- GENERAL & FONT STYLING --- */
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
            html, body, [class*="st-"], [class*="css-"] {
                font-family: 'Roboto', sans-serif;
            }

            /* --- CHAT BUBBLE STYLING --- */
            [data-testid="stChatMessage"] {
                border-radius: 20px;
                padding: 1rem 1.25rem;
                margin-bottom: 1rem;
            }
            [data-testid="stChatMessage"]:has(span[data-testid="chatAvatarIcon-user"]) {
                background-color: #F0F2F6; /* Light grey for user */
            }
            [data-testid="stChatMessage"]:has(span[data-testid="chatAvatarIcon-assistant"]) {
                background-color: #E0F7FA; /* Light teal for assistant */
            }
            
            /* --- SIDEBAR STYLING --- */
            [data-testid="stSidebar"] {
                background-color: #4A6B8A; /* Light Navy Blue */
            }
            
            [data-testid="stSidebar"] h1 {
                 color: #001f3f; /* Dark Navy Blue */
            }
            
            [data-testid="stSidebar"] [data-testid="stInfo"] div {
                color: white;
            }
            
            [data-testid="stSidebar"] [data-testid="stSuccess"] {
                color: white;
            }
            [data-testid="stSidebar"] [data-testid="stSuccess"] a {
                color: #E0E0E0;
            }

        </style>
        
    """, unsafe_allow_html=True)

# Prompt engineering
#System prompt

SYSTEM_PROMPT = """
You are 'Scout', an intelligent, polite, and professional AI hiring assistant for the recruitment agency 'Talent Scout'.
Your primary purpose is to conduct an initial screening of candidates for technology roles.
You must adhere strictly to the following conversational flow and rules. Do not deviate.
**Conversational Flow:**
1.  **Greeting:** Start by greeting the candidate warmly, introducing yourself and 'Talent Scout', and briefly explaining the purpose of the chat.
2.  **Information Gathering:** Collect the following pieces of information one by one. Do not ask for them all at once.
    - Full Name
    - Email Address
    - Phone Number
    - Years of Professional Experience
    - Desired Position(s)
    - Current Location
3.  **Tech Stack Declaration:** After gathering all personal information, ask the candidate to list their primary tech stack,frameworks,databses and other relevant technical skills.
4.  **Technical Question Generation:**
    - Once the candidate provides their tech stack, acknowledge it.
    - Then, based on the technologies they listed, generate exactly 5 relevant technical questions and present them to the candidate.
---
5.  **Answer Validation & Nudging:**
    - After the candidate provides their response to the technical questions, you must check their answer.
    - **Scenario A (User refuses or skips questions):** If the user's response indicates they did not answer some or all of the questions (e.g., they say "no", "I don't know", or only answer one question), you must politely encourage them.
        - Use a phrase like: **"Thank you for your response. To help us get a complete picture of your skills, it's important to attempt all the questions. Could you please try to answer the remaining ones? It will help us better understand your profile for the next steps in the interview process."**
        - **If they refuse again** (e.g., "I only know these", "I don't want to answer the others"), you must accept their decision gracefully. Respond with: **"Understood. Thank you, we will proceed with the information you've provided."** Then, immediately move to Step 6.
    - **Scenario B (User answers all questions):** If the user provides answers to all the questions, simply thank them and move directly to Step 6.
---
6.  **Final Conclusion & Data Recap:**
    - This is the final step of the screening. Thank the candidate for their time.
    - Inform them that a human recruiter will review their details.
    - **Crucially, you MUST then list the contact details you have collected during the conversation to confirm them with the user.**
    - Use this exact format for the recap:
        "A human recruiter will review your profile and will reach out to you using the following contact details you've provided:"
        - **Full Name:** [The name the user provided]
        - **Email:** [The email the user provided]
        - **Phone Number:** [The phone number the user provided]
    - After listing the details, conclude the main process by saying "Thank you again, and have a great day. Goodbye!"
---
**Rules & Constraints:**
- **Stay on Topic:** You are a hiring assistant. Do not engage in conversations unrelated to the job screening process.
- **Confirmation for Ending Conversation:** If a user types "exit", "quit", or "bye" mid-conversation, you must ask for confirmation ("Are you sure you want to end the screening process?") before closing the chat.
- **Multilingual Handling:** If the candidate speaks in a language other than English, continue the conversation in that language.
- **Post-Conclusion Handling:** After you have delivered your concluding message (Step 6), the main screening is over. However, **you must remain active to answer any follow-up questions** the candidate might have about the process (e.g., "When will I hear back?", "What are the next steps?"). Maintain the context and answer these questions helpfully. Do not re-start the screening."""

# Streamlit UI
st.set_page_config(page_title="_Talent Scout AI_", page_icon="✨", layout="centered")

load_css()

with st.sidebar:
    st.title("_Talent Scout_")
    st.info(
        "Welcome to Talent Scout, a premier recruitment agency specializing in "
        "technology placements. Our AI assistant, Scout, will guide you "
        "through the initial screening process."
    )

#Main chat interface
st.title("TALENT SCOUT")
st.write("They say AI is the future of recruitment.😉")

#API configuration as well as model configuration with try-except for error handling
try:
   
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Google API key not found. Please create a .env file and add GOOGLE_API_KEY='your_key'.")
        st.stop()
    
    genai.configure(api_key=api_key)
    MODEL_NAME = "gemini-2.5-pro"
except Exception as e:
    st.error(f"Failed to configure Google AI: {e}")
    st.stop()

# Data handling and summary generation for user input
def summarize_and_display_data(chat_history):
    st.info("Conversation complete. Generating candidate summary...", icon="💫")
    summary_prompt = f"""
    Based on the following conversation history, extract the candidate's information into a structured JSON object.
    The JSON object should have these exact keys: "FullName", "email", "phone", "years_of_Experience", "desired_Positions", "current_Location", "tech_Stacks".
    If a piece of information is missing, use "Not provided".

    Conversation History:
    {chat_history}
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(summary_prompt)
        json_string = response.text.strip().replace("```json", "").replace("```", "")
        candidate_data = json.loads(json_string)
        st.success("Candidate Data Extracted Successfully!")
        st.json(candidate_data)
        st.balloons()
    except Exception as e:
        st.error(f"Could not parse candidate data. Please review manually.")
        st.text_area("Full Conversation Log", value=str(chat_history), height=300)

# Session state initialization
if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT,
        safety_settings={
            'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
            'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
        }
    )
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []
    initial_greeting = "Hello! I'm Scout, your AI hiring assistant from Talent Scout. Let's begin, what is your full name?"
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input handling
if prompt := st.chat_input("Your response..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = st.session_state.chat.send_message(prompt, stream=True)
            for chunk in stream:
                if hasattr(chunk, 'text'):
                    full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = "I encountered an error."
            message_placeholder.markdown(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Checking if conversation has ended.Looking for keywords-thankyou,have a great day
    end_keywords = ["thank you for your time", "recruiter will be in touch", "have a great day", "goodbye"]
    if any(keyword in full_response.lower() for keyword in end_keywords):
        summarize_and_display_data(st.session_state.chat.history)