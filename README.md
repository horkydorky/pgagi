# Talent Scout AI - Intelligent Hiring Assistant

## 1. Project Overview

Talent Scout AI is an intelligent chatbot which acts as a hiring assistant for "Talent Scout". The primary purpose of this app is to automate the initial candidate screening process.

The chatbot engages candidates in a structured conversation to gather name,email,contact-number and place of residence, identifies their technical skills, and asks relevant technical questions based on their declared tech stack. This project demonstrates advanced prompt engineering techniques, state management in a conversational AI, and the development of a clean, user-friendly interface using Streamlit and Google's Gemini 2.5 Pro model.

### Key Capabilities:
-   **Structured Information Gathering:** Collects candidate details like name, contact info, experience, and location in a natural, step-by-step manner.
-   **Dynamic Technical Questioning:** Generates 3-5 technical questions tailored specifically to the candidate's declared programming languages, frameworks, and tools.
-   **Robust Conversation Flow:** Handles complex scenarios such as users refusing to answer, asking to end the conversation, and speaking in multiple languages.
-   **Enhanced User Interface:** Features a custom-styled, branded interface with a professional sidebar, custom icons, and an improved chat experience.
-   **Data Recap:** Concludes the conversation by summarizing the collected contact information in a JSON foramt back to the user for confirmation.

## 2. Installation Instructions

steps to set up and run the application .

### Prerequisites
-   Python 3.8 or higher
-   `pip` 
-   Git

### Step-by-Step Setup

**1. Clone the Repository:**
```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

**2. Create and Activate a Virtual Environment:**
This isolates the project's dependencies from your system's Python installation.
-   **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
-   **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

**3. Install Required Libraries:**
Install all necessary packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

**4. Set Up Your API Key:**
The application requires a Google AI Studio API key to function.
-   Create a file named `.env` in the root directory of the project.
-   Add your API key to this file in the following format:
    ```env
    GOOGLE_API_KEY="your_actual_google_api_key_here"
    ```
-   **Note:** The `.gitignore` file is configured to prevent the `.env` file from being committed to the repository.

**5. Run the Application:**
Launch the Streamlit application with the following command:
```bash
streamlit run app.py
```
The application will open in a new tab in your default web browser.

## 3. Usage Guide

Once the application is running, interact with the chatbot as if you were a job candidate. The chatbot, "Scout," will guide you through the following steps:
1.  It will greet you and explain its purpose.
2.  It will ask for your personal and professional details one at a time.
3.  It will ask you to list your technical skills (e.g., "Python, React, PostgreSQL").
4.  Based on your skills, it will generate a set of technical questions.
5.  After you answer (or decline to answer), it will conclude the screening and recap your contact details.

You can also test its robustness by trying to end the conversation early or by switching languages.

## 4. Technical Details

-   **Programming Language:** Python
-   **Frontend Interface:** Streamlit
-   **Large Language Model (LLM):** Google Gemini Pro (`gemini-pro`) via the Google AI Studio API.
-   **Libraries Used:**
    -   `streamlit`: For building the web UI.
    -   `google-generativeai`: The official Google client library for the Gemini API.
    -   `python-dotenv`: For managing environment variables and API keys securely.

## 5. Prompt Design

The core logic of the chatbot is driven by a comprehensive `SYSTEM_PROMPT`. This prompt acts as a "constitution" for the AI, defining its persona, rules, and a multi-step conversational flow.

-   **State-Machine Approach:** The prompt is structured like a state machine, guiding the AI from `Greeting` -> `Information Gathering` -> `Tech Questions` -> `Answer Validation` -> `Conclusion`. This prevents the model from deviating from its purpose.
-   **Handling Edge Cases:** Specific rules were engineered to handle complex user interactions:
    -   **Answer Validation & Nudging:** A dedicated step was created to check if a user skipped technical questions. The AI is instructed to politely encourage them once before accepting their refusal and moving on.
    -   **Confirmation for Ending Conversation:** A two-step rule requires the AI to ask for confirmation before quitting, preventing accidental exits.
    -   **Post-Conclusion Handling:** The AI is explicitly told to remain active to answer follow-up questions after the main screening is complete, ensuring a coherent user experience.
    -   
## 6. Challenges & Solutions

 **Challenge:** The application frequently hit a `429 Rate Limit Error`.
1.    *   **Solution:** Investigation revealed the Google AI Studio free tier has a very low limit (2 requests/minute). The solution is to either wait for the quota to reset or, for a more robust solution, enable billing on the Google Cloud project to increase the limit to 60 requests/minute.

2.  **Challenge:** The API would sometimes return a generic error, especially with informal or multilingual input.
    *   **Solution:** This was traced to the API's default safety filters being overly cautious. By explicitly setting the `safety_settings` to `BLOCK_NONE` for all categories, these false positives were eliminated, making the chatbot much more reliable.

3.  **Challenge:** The chatbot's UI was basic and lacked a professional feel.
    *   **Solution:** Custom CSS was injected into the Streamlit app to apply a new font, a branded color scheme (light navy blue), custom chat bubble styles, and a professional sidebar. This significantly improved the user experience and met the "UI Enhancements" bonus criteria.
