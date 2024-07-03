import streamlit as st
import pandas as pd
from datetime import datetime, time
import random
import string

# [Keep the existing imports and CSS styles]

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

def get_chatbot_response(last_report, user_input):
    if user_input == "I want to create a report":
        response = f"Your last report was '{last_report}'. "
        
        if last_report in REQUIRED_FOLLOW_UPS:
            response += f"Remember that you may need to complete the '{REQUIRED_FOLLOW_UPS[last_report]}' report. "
        
        if last_report in FOLLOW_UP_REPORTS:
            options = ", ".join(FOLLOW_UP_REPORTS[last_report])
            response += f"You can create one of the following reports: {options}. "
        else:
            options = ", ".join(ALL_REPORT_TYPES)
            response += f"You can create any of the following reports: {options}. "
        
        response += "Which report would you like to create?"
        return response
    elif user_input == "I want to see the last voyage reports list":
        return "Here is a placeholder for the last voyage reports list. In a real implementation, this would fetch and display the actual list of recent reports."
    else:
        return "I'm sorry, I didn't understand that request. Would you like to create a report or see the last voyage reports list?"

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

def create_chatbot():
    st.header("AI Assistant")
    
    # Dropdown for selecting last report (for testing)
    last_report = st.selectbox("Select last report (for testing)", ALL_REPORT_TYPES, key="last_report")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display default options if no messages
    if not st.session_state.messages:
        st.button("I want to create a report", on_click=lambda: add_user_message("I want to create a report"))
        st.button("I want to see the last voyage reports list", on_click=lambda: add_user_message("I want to see the last voyage reports list"))

    # React to user input
    if prompt := st.chat_input("Type your message here"):
        add_user_message(prompt)

    # Generate and display chatbot response
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        response = get_chatbot_response(last_report, st.session_state.messages[-1]["content"])
        add_assistant_message(response)

def add_user_message(message):
    st.session_state.messages.append({"role": "user", "content": message})

def add_assistant_message(message):
    st.session_state.messages.append({"role": "assistant", "content": message})

if __name__ == "__main__":
    main()
