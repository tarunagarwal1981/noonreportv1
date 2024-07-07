import streamlit as st
import openai
from datetime import datetime, time
import pytz
import json
import os
import re

# Set page config
st.set_page_config(layout="wide", page_title="AI-Enhanced Maritime Reporting System")

# Custom CSS for compact layout and collapsible panel
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
    .collapsible {
        background-color: #f1f1f1;
        color: #444;
        cursor: pointer;
        padding: 18px;
        width: 100%;
        border: none;
        text-align: left;
        outline: none;
        font-size: 15px;
    }
    .active, .collapsible:hover {
        background-color: #ccc;
    }
    .content {
        padding: 0 18px;
        display: none;
        overflow: hidden;
        background-color: #f1f1f1;
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
You are an AI assistant for an advanced maritime reporting system. Your role is to guide users through creating various types of maritime reports, ensuring compliance with industry standards and regulations.

Key features:
1. Error reduction and data completion assistance
2. Insights generation based on reported data
3. Streamlined reporting process
4. Enhanced accuracy in maritime operational reporting

When suggesting follow-up reports, consider the history of the last 3-4 reports. Here's an example of how to use this history:

Example:
Last 4 reports: COSP Report -> Arrival Anchor Report -> Begin Fuel Changeover Report -> Noon at Anchor Report

Based on this history:
1. An EOSP Report is still pending after the COSP Report.
2. Since the vessel is anchored, possible next reports include:
   - Noon at Anchor Report (if it's approaching noon)
   - Departure Anchor Report (if the vessel is preparing to leave)
3. An End Fuel Changeover Report is expected to follow the Begin Fuel Changeover Report.

Use this context to provide intelligent suggestions for the next possible reports, reminders of pending reports, and any relevant operational insights.

When responding, provide a concise list of possible next reports, any pending reports that should be completed, and brief operational reminders if relevant.
"""

def get_ai_response(user_input, last_reports):
    current_time = datetime.now(pytz.utc).strftime("%H:%M:%S")
    
    context = f"""
    The current UTC time is {current_time}. 
    The last reports submitted were: {' -> '.join(last_reports)}
    
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
            max_tokens=200,
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

def create_collapsible_history_panel():
    st.markdown("""
    <button class="collapsible">Report History</button>
    <div class="content">
    """, unsafe_allow_html=True)
    
    if "report_history" not in st.session_state:
        st.session_state.report_history = ["None"] * 4

    for i in range(4):
        st.session_state.report_history[i] = st.selectbox(
            f"Report {i+1}:",
            ["None"] + REPORT_TYPES,
            key=f"history_{i}",
            index=REPORT_TYPES.index(st.session_state.report_history[i]) + 1 if st.session_state.report_history[i] in REPORT_TYPES else 0
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Add JavaScript to make the collapsible work
    st.markdown("""
    <script>
    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      });
    }
    </script>
    """, unsafe_allow_html=True)

def create_chatbot(last_reports):
    st.header("AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I assist you with your maritime reporting?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_ai_response(prompt, last_reports)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Check if a specific report type is mentioned
        for report_type in REPORT_TYPES:
            if report_type.lower() in prompt.lower():
                if report_type in FOLLOW_UP_REPORTS.get(last_reports[-1], REPORT_TYPES):
                    st.session_state.current_report_type = report_type
                    st.session_state.show_form = True
                else:
                    st.warning(f"{report_type} is not a valid follow-up report for {last_reports[-1]}. Please choose from: {', '.join(FOLLOW_UP_REPORTS.get(last_reports[-1], REPORT_TYPES))}")
                break
        
        st.experimental_rerun()

def main():
    st.title("AI-Enhanced Maritime Reporting System")
    
    create_collapsible_history_panel()
    
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
        create_chatbot([report for report in st.session_state.report_history if report != "None"])
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.show_form = False
            st.session_state.current_report_type = None
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
