import streamlit as st
import openai
from datetime import datetime, time
import pytz
import json
import os
import re

# Set page config
st.set_page_config(layout="wide", page_title="AI-Enhanced Maritime Reporting System")

# Custom CSS for compact layout
st.markdown("""
<style>
    .reportSection { padding-right: 1rem; }
    .chatSection { padding-left: 1rem; border-left: 1px solid #e0e0e0; }
    .stButton > button { width: 100%; }
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100%; }
    h1, h2, h3 { margin-top: 0; font-size: 1.2em; }
    .stAlert { margin-top: 1rem; }
    .stNumberInput, .stTextInput, .stSelectbox { 
        padding-bottom: 0.5rem !important; 
    }
    .stNumberInput input, .stTextInput input, .stSelectbox select {
        padding: 0.3rem !important;
        font-size: 0.9em !important;
    }
    .stExpander { 
        border: none !important; 
        box-shadow: none !important;
        margin-bottom: 0.5rem !important;
    }
    .last-report-dropdown {
        font-size: 0.8em;
        margin-bottom: 1rem;
    }
    .last-report-dropdown > div > div > div {
        padding: 0.2rem 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Set up OpenAI API key
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("OpenAI API key not found. Please set it in Streamlit secrets or as an environment variable.")
    st.stop()

# Define report types and their sequences
REPORT_TYPES = [
    "Noon Sea Report", "End of Sea Passage (EOSP) Report", "Anchor Arrival / Finish with Engine (FWE) Report",
    "Noon Port / Anchor Report", "Anchor Departure / Standby Engine (SBE) Report",
    "Berth Arrival / Finish with Engine (FWE) Report", "Berth Departure / Standby Engine (SBE) Report",
    "Commencement of Sea Passage (COSP) Report", "Begin Offhire Report", "End Offhire Report",
    "Arrival STS Report", "Departure STS Report", "Begin Canal Passage Report", "End Canal Passage Report",
    "Noon at River Passage Report", "Noon Stoppage Report", "Begin Fuel Changeover Report",
    "End Fuel Changeover Report", "Bunkering Report"
]

FOLLOW_UP_REPORTS = {
    "Noon Sea Report": ["Noon Sea Report", "End of Sea Passage (EOSP) Report", "Begin Fuel Changeover Report", "End Fuel Changeover Report"],
    "End of Sea Passage (EOSP) Report": ["Anchor Arrival / Finish with Engine (FWE) Report", "Berth Arrival / Finish with Engine (FWE) Report", "Begin Anchoring/Drifting"],
    "Anchor Arrival / Finish with Engine (FWE) Report": ["Noon Port / Anchor Report", "Anchor Departure / Standby Engine (SBE) Report", "Begin Fuel Changeover Report", "End Fuel Changeover Report"],
    "Noon Port / Anchor Report": ["Noon Port / Anchor Report", "Anchor Departure / Standby Engine (SBE) Report", "Begin Fuel Changeover Report", "End Fuel Changeover Report"],
    "Anchor Departure / Standby Engine (SBE) Report": ["Commencement of Sea Passage (COSP) Report", "Berth Arrival / Finish with Engine (FWE) Report"],
    "Berth Arrival / Finish with Engine (FWE) Report": ["Noon Port / Anchor Report", "Berth Departure / Standby Engine (SBE) Report", "Begin Fuel Changeover Report", "End Fuel Changeover Report"],
    "Berth Departure / Standby Engine (SBE) Report": ["Commencement of Sea Passage (COSP) Report", "Anchor Arrival / Finish with Engine (FWE) Report"],
    "Commencement of Sea Passage (COSP) Report": ["Noon Sea Report", "End of Sea Passage (EOSP) Report"],
    "Begin Offhire Report": ["End Offhire Report"],
    "End Offhire Report": ["Begin Offhire Report"],
    "Arrival STS Report": ["Departure STS Report", "Begin Fuel Changeover Report", "End Fuel Changeover Report"],
    "Departure STS Report": ["Commencement of Sea Passage (COSP) Report"],
    "Begin Canal Passage Report": ["End Canal Passage Report"],
    "End Canal Passage Report": ["Commencement of Sea Passage (COSP) Report", "Berth Arrival / Finish with Engine (FWE) Report"],
    "Noon at River Passage Report": ["Noon at River Passage Report", "End Canal Passage Report"],
    "Noon Stoppage Report": ["Noon Stoppage Report", "Commencement of Sea Passage (COSP) Report"],
    "Begin Fuel Changeover Report": ["End Fuel Changeover Report"],
    "End Fuel Changeover Report": ["Begin Fuel Changeover Report"],
    "Bunkering Report": ["Bunkering Report", "End Fuel Changeover Report"]
}

REMINDERS = {
    "Begin Fuel Changeover Report": "Remember to submit an End Fuel Changeover Report when the changeover is complete.",
    "Commencement of Sea Passage (COSP) Report": "Don't forget to submit regular Noon Sea Reports and an End of Sea Passage (EOSP) Report when appropriate.",
    "Anchor Arrival / Finish with Engine (FWE) Report": "Remember to submit Noon Port / Anchor Reports daily while at anchor.",
    "Begin Canal Passage Report": "Don't forget to submit an End Canal Passage Report when the canal passage is complete.",
    "Begin Offhire Report": "Remember to submit an End Offhire Report when the offhire period is over.",
}

# Prepare the training data as a string
TRAINING_DATA = """
You are an AI assistant for an advanced maritime reporting system. Your role is to guide users through creating various types of maritime reports, ensuring compliance with industry standards and regulations. The system aims to revolutionize the noon reporting process while adhering to the following:

- Standardised Vessel Dataset (SVD) Version 1.0 for Noon Reports
- IMO Data Collection System (DCS) requirements
- EU Monitoring, Reporting and Verification (MRV) scheme
- Relevant ISO standards
- IMO Compendium on Facilitation and Electronic Business

Key features:
1. Error reduction and data completion assistance
2. Insights generation based on reported data
3. Streamlined reporting process
4. Enhanced accuracy in maritime operational reporting

For each report type, provide guidance on required fields, remind users of pending reports, and suggest appropriate follow-up reports. Always maintain a professional and helpful tone, and be prepared to explain industry standards and regulations when asked.

Report Types and Specific Guidelines:

1. Noon Sea Report:
   - Conditions: After Commencement of Sea Passage (COSP) or when at sea; check for ice conditions and safety of the ship.
   - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

2. End of Sea Passage (EOSP) Report:
   - Conditions: After sea passage ends.
   - Reminder: "After completing the EOSP report, please remember to fill an Arrival report (Anchor, Port, or STS) when the vessel arrives."

3. Anchor Arrival / Finish with Engine (FWE) Report:
   - Conditions: Upon arrival at anchorage or for maneuvering.
   - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

4. Noon Port / Anchor Report:
   - Conditions: At 12:00 LT when at berth or anchorage; include anchorage hours if at anchorage.
   - Fields: Include 'Anchorage_hours_Hrs'.
   - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

5. Anchor Departure / Standby Engine (SBE) Report:
   - Conditions: When departing from anchorage.
   - Reminder: "After completing the Departure report, please remember to fill a Commencement of Sea Passage (COSP) report when the sea passage starts."

6. Berth Arrival / Finish with Engine (FWE) Report:
   - Conditions: Upon arrival at berth for cargo operations or for maneuvering.
   - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

7. Berth Departure / Standby Engine (SBE) Report:
   - Conditions: When departing from berth after cargo operations.
   - Reminder: "After completing the Departure report, please remember to fill a Commencement of Sea Passage (COSP) report when the sea passage starts."

8. Commencement of Sea Passage (COSP) Report:
   - Conditions: When the sea passage starts or for maneuvering.
   - Reminder: "After completing the COSP report, please remember to fill an End of Sea Passage (EOSP) report when the sea passage ends."

9. Begin Offhire Report:
   - Conditions: When the offhire period starts.
   - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

10. End Offhire Report:
    - Conditions: When the offhire period ends.
    - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

11. Arrival STS Report:
    - Conditions: When arriving for a Ship-to-Ship transfer.
    - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

12. Departure STS Report:
    - Conditions: When departing from a Ship-to-Ship transfer.
    - Reminder: "After completing the Departure report, please remember to fill a Commencement of Sea Passage (COSP) report when the sea passage starts."

13. Begin Canal Passage Report:
    - Conditions: When beginning a canal passage.
    - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

14. End Canal Passage Report:
    - Conditions: When ending a canal passage.
    - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

15. Noon at River Passage Report:
    - Conditions: At 12:00 LT when at a river passage.
    - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

16. Noon Stoppage Report:
    - Conditions: When stopped between Commencement of Sea Passage (COSP) and End of Sea Passage (EOSP).
    - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

17. Begin Fuel Changeover Report:
    - Conditions: When beginning a fuel changeover.
    - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

18. End Fuel Changeover Report:
    - Conditions: When ending a fuel changeover.
    - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

19. Bunkering Report:
    - Conditions: Whenever the vessel is bunkering.
    - Reminder: "You have not yet filled an End/Departure report for the last Begin/Arrival event. Please remember to complete it when appropriate."

For each report, provide appropriate follow-up report suggestions based on the current operational context of the vessel.

Always be prepared to explain industry standards, regulations, and best practices related to maritime reporting when asked.
"""

def get_ai_response(user_input, last_report):
    current_time = datetime.now(pytz.utc).strftime("%H:%M:%S")
    
    # Get valid follow-up reports
    valid_reports = FOLLOW_UP_REPORTS.get(last_report, REPORT_TYPES)
    
    # Get any reminders
    reminder = REMINDERS.get(last_report, "")
    
    context = f"""
    The current UTC time is {current_time}. 
    The last report submitted was: {last_report}
    Valid follow-up reports: {', '.join(valid_reports)}
    Reminder: {reminder}
    
    Please provide guidance based on this context and the user's input.
    """
    
    messages = [
        {"role": "system", "content": TRAINING_DATA},
        {"role": "system", "content": context},
        {"role": "user", "content": user_input}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"I'm sorry, but I encountered an error while processing your request: {str(e)}. Please try again later."

def create_form(report_type):
    st.header(f"New {report_type}")
    
    # Add form fields based on the report type
    # This is a placeholder and should be expanded based on specific requirements for each report type
    with st.expander("Vessel Data", expanded=True):
        st.text_input("Vessel Name", key="vessel_name")
        st.text_input("IMO Number", key="imo_number")

    with st.expander("Report Details", expanded=True):
        st.date_input("Report Date", key="report_date")
        st.time_input("Report Time (UTC)", key="report_time")

    with st.expander("Position", expanded=True):
        st.number_input("Latitude", min_value=-90.0, max_value=90.0, key="latitude")
        st.number_input("Longitude", min_value=-180.0, max_value=180.0, key="longitude")

    # Add more expandable sections for other report details

    if st.button("Submit Report"):
        st.success(f"{report_type} submitted successfully!")
        return True
    return False

def create_chatbot(last_report):
    st.header("AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I assist you with your maritime reporting?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_ai_response(prompt, last_report)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Check if a specific report type is mentioned
        for report_type in REPORT_TYPES:
            if report_type.lower() in prompt.lower():
                if report_type in FOLLOW_UP_REPORTS.get(last_report, REPORT_TYPES):
                    st.session_state.current_report_type = report_type
                    st.session_state.show_form = True
                else:
                    st.warning(f"{report_type} is not a valid follow-up report for {last_report}. Please choose from: {', '.join(FOLLOW_UP_REPORTS.get(last_report, REPORT_TYPES))}")
                break
        
        st.experimental_rerun()

def main():
    st.title("AI-Enhanced Maritime Reporting System")
    
    col1, col2 = st.columns([0.6, 0.4])

    with col1:
        st.markdown('<div class="reportSection">', unsafe_allow_html=True)
        if 'show_form' in st.session_state and st.session_state.show_form:
            if create_form(st.session_state.current_report_type):
                st.session_state.show_form = False
                st.experimental_rerun()
        else:
            st.write("Please use the AI Assistant to initiate a report.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chatSection">', unsafe_allow_html=True)
        
        # Add the dropdown for last submitted report at the top of the chatbot section
        st.markdown('<div class="last-report-dropdown">', unsafe_allow_html=True)
        last_report = st.selectbox(
            "Last submitted report:",
            ["None"] + REPORT_TYPES,
            key="last_report_select",
            help="Select the last submitted report for context (for testing purposes)"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        create_chatbot(last_report)
        
        if st.button("Clear Report"):
            st.session_state.messages = []
            st.session_state.show_form = False
            st.session_state.current_report_type = None
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
