import streamlit as st
import pandas as pd
from datetime import datetime, time
import random
import string
import re

# Set page config
st.set_page_config(layout="wide", page_title="Maritime Reporting System")

# Custom CSS (keep your existing styles)
st.markdown("""
<style>
    /* Your existing styles here */
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Define all possible report types
ALL_REPORT_TYPES = [
    "Arrival at Port", "Arrival at STS", "Departure from Port", "Departure from STS",
    "Noon at Port/STS", "Bunkering", "Off hire", "Begin Fuel Changeover",
    "End Fuel Changeover", "Begin of Offhire", "End of Offhire", "ArrivalSTS",
    "DepartureSTS", "Begin Canal Passage", "End Canal Passage",
    "Begin Anchoring/Drifting", "End Anchoring/Drifting", "Noon (Position) - River",
    "Noon (Position) - Stoppage", "Entering Special Area", "Leaving Special Area",
    "End of Sea Passage (EOSP)"
]

# Define the follow-up reports for each report type
FOLLOW_UP_REPORTS = {
    "Arrival at Port": ["Departure from Port", "Noon at Port/STS", "Bunkering", "Off hire", "Begin Fuel Changeover", "End Fuel Changeover"],
    "Arrival at STS": ["Departure from STS", "Noon at Port/STS", "Bunkering", "Off hire", "Begin Fuel Changeover", "End Fuel Changeover"],
    "Departure from Port": ["Noon at Port/STS", "Begin of Offhire", "End of Offhire", "ArrivalSTS", "DepartureSTS", "Begin Canal Passage", "End Canal Passage", "Begin Anchoring/Drifting", "End Anchoring/Drifting", "Noon (Position) - River", "Noon (Position) - Stoppage", "Begin Fuel Changeover", "End Fuel Changeover", "Entering Special Area", "Leaving Special Area"],
    "Departure from STS": ["Noon at Port/STS", "Begin of Offhire", "End of Offhire", "ArrivalSTS", "DepartureSTS", "Begin Canal Passage", "End Canal Passage", "Begin Anchoring/Drifting", "End Anchoring/Drifting", "Noon (Position) - River", "Noon (Position) - Stoppage", "Begin Fuel Changeover", "End Fuel Changeover", "Entering Special Area", "Leaving Special Area"],
    "End of Sea Passage (EOSP)": ["Noon at Port/STS", "Begin of Offhire", "End of Offhire", "ArrivalSTS", "DepartureSTS", "Begin Canal Passage", "End Canal Passage", "Begin Anchoring/Drifting", "End Anchoring/Drifting", "Noon (Position) - River", "Noon (Position) - Stoppage", "Begin Fuel Changeover", "End Fuel Changeover", "Entering Special Area", "Leaving Special Area"]
}

# Define reports that require a specific follow-up
REQUIRED_FOLLOW_UPS = {
    "Begin Fuel Changeover": "End Fuel Changeover",
    "Entering Special Area": "Leaving Special Area",
    "Begin of Offhire": "End of Offhire",
    "Begin Canal Passage": "End Canal Passage",
    "Begin Anchoring/Drifting": "End Anchoring/Drifting",
    "Arrival at Port": "Departure from Port",
    "Arrival at STS": "Departure from STS",
    "ArrivalSTS": "DepartureSTS"
}

# Simple tokenization function
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

# Simple stemming function
def simple_stem(word):
    suffixes = ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's']
    for suffix in suffixes:
        if word.endswith(suffix):
            return word[:-len(suffix)]
    return word

def preprocess_text(text):
    tokens = tokenize(text)
    return [simple_stem(token) for token in tokens]

def extract_intent(tokens):
    create_keywords = ['create', 'make', 'new', 'start']
    view_keywords = ['see', 'view', 'show', 'list']
    
    if any(word in tokens for word in create_keywords):
        return 'create_report'
    elif any(word in tokens for word in view_keywords):
        return 'view_reports'
    else:
        return 'unknown'

def extract_report_type(tokens):
    for report_type in ALL_REPORT_TYPES:
        if all(simple_stem(word) in tokens for word in tokenize(report_type.lower())):
            return report_type
    return None

def get_chatbot_response(last_report, user_input):
    tokens = preprocess_text(user_input)
    intent = extract_intent(tokens)
    report_type = extract_report_type(tokens)

    if intent == 'create_report':
        response = f"Your last report was '{last_report}'. "
        
        if report_type:
            response += f"You've indicated you want to create a {report_type} report. "
        else:
            response += "Which type of report would you like to create? "

        if last_report in REQUIRED_FOLLOW_UPS:
            response += f"Remember that you may need to complete the '{REQUIRED_FOLLOW_UPS[last_report]}' report. "
        
        if last_report in FOLLOW_UP_REPORTS:
            options = ", ".join(FOLLOW_UP_REPORTS[last_report])
            response += f"You can create one of the following reports: {options}. "
        else:
            options = ", ".join(ALL_REPORT_TYPES)
            response += f"You can create any of the following reports: {options}. "

    elif intent == 'view_reports':
        response = "Here is a placeholder for the last voyage reports list. In a real implementation, this would fetch and display the actual list of recent reports."
    else:
        response = "I'm not sure I understood that. Would you like to create a new report or view existing reports? You can say something like 'Create a new arrival report' or 'Show me the last voyage reports'."

    return response

def main():
    st.title("AI-Enhanced Maritime Reporting System")
    
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.markdown('<div class="reportSection">', unsafe_allow_html=True)
        create_form()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chatSection">', unsafe_allow_html=True)
        create_chatbot()
        st.markdown('</div>', unsafe_allow_html=True)

def create_form():
    # Your existing form code here (unchanged)
    pass

def clear_chat_history():
    st.session_state.messages = []

def create_chatbot():
    st.header("AI Assistant")
    
    # Dropdown for selecting last report (for testing)
    last_report = st.selectbox("Select last report (for testing)", ALL_REPORT_TYPES, key="last_report")

    # Clear Chat button
    if st.button("Clear Chat"):
        clear_chat_history()
        st.experimental_rerun()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("How can I assist you with your maritime reporting?"):
        add_user_message(prompt)
        response = get_chatbot_response(last_report, prompt)
        add_assistant_message(response)

def add_user_message(message):
    st.session_state.messages.append({"role": "user", "content": message})

def add_assistant_message(message):
    st.session_state.messages.append({"role": "assistant", "content": message})

if __name__ == "__main__":
    main()
