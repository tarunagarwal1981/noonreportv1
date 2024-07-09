import streamlit as st
import openai
from datetime import datetime
import pytz
import os
import random
import string

# Constants
PORTS = [
    "Singapore", "Rotterdam", "Shanghai", "Ningbo-Zhoushan", "Guangzhou Harbor", "Busan",
    "Qingdao", "Hong Kong", "Tianjin", "Port Klang", "Antwerp", "Dubai Ports", "Xiamen",
    "Kaohsiung", "Hamburg", "Los Angeles", "Tanjung Pelepas", "Laem Chabang", "New York-New Jersey",
    "Dalian", "Tanjung Priok", "Valencia", "Colombo", "Ho Chi Minh City", "Algeciras"
]

VESSEL_PREFIXES = ["MV", "SS", "MT", "MSC", "CMA CGM", "OOCL", "Maersk", "Evergreen", "Cosco", "NYK"]
VESSEL_NAMES = ["Horizon", "Voyager", "Pioneer", "Adventurer", "Explorer", "Discovery", "Navigator", "Endeavour", "Challenger", "Trailblazer"]

REPORT_TYPES = [
    "Arrival", "Departure", "Begin of offhire", "End of offhire", "Arrival STS",
    "Departure STS", "STS", "Begin canal passage", "End canal passage",
    "Begin of sea passage", "End of sea passage", "Begin Anchoring/Drifting",
    "End Anchoring/Drifting", "Noon (Position) - Sea passage", "Noon (Position) - Port",
    "Noon (Position) - River", "Noon (Position) - Stoppage", "ETA update",
    "Begin fuel change over", "End fuel change over", "Change destination (Deviation)",
    "Begin of deviation", "End of deviation", "Entering special area", "Leaving special area"
]

# Report structures and section fields (abbreviated for brevity)
REPORT_STRUCTURES = {report_type: ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"] for report_type in REPORT_TYPES}
REPORT_STRUCTURES["ETA update"] = ["Vessel Data", "Voyage Data", "Position"]

SECTION_FIELDS = {
    "Vessel Data": ["Vessel Name", "Vessel IMO"],
    "Voyage Data": ["Local Date", "Local Time", "UTC Offset", "Voyage ID", "Segment ID", "From Port", "To Port"],
    "Event Data": ["Event Type", "Time Elapsed (hours)", "Sailing Time (hours)", "Anchor Time (hours)", "DP Time (hours)", "Ice Time (hours)", "Maneuvering (hours)", "Loading/Unloading (hours)", "Drifting (hours)"],
    "Position": ["Latitude Degrees", "Latitude Minutes", "Latitude Direction", "Longitude Degrees", "Longitude Minutes", "Longitude Direction"],
    "Cargo": ["Cargo Weight (mt)"],
    "Fuel Consumption": {
        "Main Engine": ["ME LFO (mt)", "ME MGO (mt)", "ME LNG (mt)", "ME Other (mt)", "ME Other Fuel Type"],
        "Auxiliary Engines": ["AE LFO (mt)", "AE MGO (mt)", "AE LNG (mt)", "AE Other (mt)", "AE Other Fuel Type"],
        "Boilers": ["Boiler LFO (mt)", "Boiler MGO (mt)", "Boiler LNG (mt)", "Boiler Other (mt)", "Boiler Other Fuel Type"]
    },
    "ROB": ["LFO ROB (mt)", "MGO ROB (mt)", "LNG ROB (mt)", "Other ROB (mt)", "Other Fuel Type ROB", "Total Fuel ROB (mt)"],
    "Fuel Allocation": {
        "Cargo Heating": ["Cargo Heating LFO (mt)", "Cargo Heating MGO (mt)", "Cargo Heating LNG (mt)", "Cargo Heating Other (mt)", "Cargo Heating Other Fuel Type"],
        "Dynamic Positioning (DP)": ["DP LFO (mt)", "DP MGO (mt)", "DP LNG (mt)", "DP Other (mt)", "DP Other Fuel Type"]
    },
    "Machinery": {
        "Main Engine": ["ME Load (kW)", "ME Load Percentage (%)", "ME Speed (RPM)", "ME Propeller Pitch (m)", "ME Propeller Pitch Ratio", "ME Shaft Generator Power (kW)", "ME Charge Air Inlet Temp (°C)", "ME Scav. Air Pressure (bar)", "ME SFOC (g/kWh)", "ME SFOC ISO Corrected (g/kWh)"],
        "Auxiliary Engines": {
            "Auxiliary Engine 1": ["AE1 Load (kW)", "AE1 Charge Air Inlet Temp (°C)", "AE1 Charge Air Pressure (bar)", "AE1 SFOC (g/kWh)", "AE1 SFOC ISO Corrected (g/kWh)"],
            "Auxiliary Engine 2": ["AE2 Load (kW)", "AE2 Charge Air Inlet Temp (°C)", "AE2 Charge Air Pressure (bar)", "AE2 SFOC (g/kWh)", "AE2 SFOC ISO Corrected (g/kWh)"],
            "Auxiliary Engine 3": ["AE3 Load (kW)", "AE3 Charge Air Inlet Temp (°C)", "AE3 Charge Air Pressure (bar)", "AE3 SFOC (g/kWh)", "AE3 SFOC ISO Corrected (g/kWh)"]
        }
    },
    "Weather": {
        "Wind": ["Wind Direction (degrees)", "Wind Speed (knots)", "Wind Force (Beaufort)"],
        "Sea State": ["Sea State Direction (degrees)", "Sea State Force (Douglas scale)", "Sea State Period (seconds)"],
        "Swell": ["Swell Direction (degrees)", "Swell Height (meters)", "Swell Period (seconds)"],
        "Current": ["Current Direction (degrees)", "Current Speed (knots)"],
        "Temperature": ["Air Temperature (°C)", "Sea Temperature (°C)"]
    },
    "Draft": {
        "Actual": ["Actual Forward Draft (m)", "Actual Aft Draft (m)", "Displacement (mt)", "Water Depth (m)"]
    }
}

# Set page config
st.set_page_config(layout="wide", page_title="AI-Enhanced Maritime Reporting System")

# Custom CSS
st.markdown("""
<style>
    .reportSection { padding-right: 1rem; }
    .chatSection { padding-left: 1rem; border-left: 1px solid #e0e0e0; }
    .stButton > button { width: 100%; }
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 100%; }
    h1, h2, h3 { margin-top: 0; font-size: 1.5em; line-height: 1.3; padding: 0.5rem 0; }
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
    .history-panel {
        background-color: #f1f1f1;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        max-width: 300px;
    }
    .history-panel h3 {
        margin-top: 0;
        margin-bottom: 10px;
    }
    .history-select {
        margin-bottom: 5px;
    }
    .field-prompt {
        font-size: 0.8em;
        color: #666;
        margin-bottom: 2px;
    }
    .small-warning {
        font-size: 8px;
        color: #b20000;
        background-color: #ffe5e5;
        border-radius: 5px;
        padding: 5px;
    }
    .info-message {
        font-size: 12px;
        color: #0066cc;
        background-color: #e6f2ff;
        padding: 5px;
        border-radius: 3px;
        margin-top: 5px;
        margin-bottom: 10px;
        display: inline-block;
    }
    .chat-container {
        height: 400px;
        overflow-y: auto;
        border: 1px solid #ddd;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    .user-message {
        background-color: #e6f2ff;
        padding: 5px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .assistant-message {
        background-color: #f0f0f0;
        padding: 5px;
        margin: 5px 0;
        border-radius: 5px;
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

# Helper functions
def generate_random_position():
    lat_deg = random.randint(0, 89)
    lat_min = round(random.uniform(0, 59.99), 2)
    lat_dir = random.choice(['N', 'S'])
    lon_deg = random.randint(0, 179)
    lon_min = round(random.uniform(0, 59.99), 2)
    lon_dir = random.choice(['E', 'W'])
    return lat_deg, lat_min, lat_dir, lon_deg, lon_min, lon_dir

def generate_random_consumption():
    me_lfo = round(random.uniform(20, 25), 1)
    ae_lfo = round(random.uniform(2, 3), 1)
    return me_lfo, ae_lfo

def generate_random_vessel_name():
    return f"{random.choice(VESSEL_PREFIXES)} {random.choice(VESSEL_NAMES)}"

def generate_random_imo():
    return ''.join(random.choices(string.digits, k=7))

def get_field_prompt(field):
    prompts = {
        "Vessel Name": "What's the name of the vessel?",
        "Vessel IMO": "What's the IMO number of the vessel?",
        "Local Date": "What's the local date for this report?",
        "Local Time": "What's the local time for this report?",
        "UTC Offset": "What's the UTC offset for the current location?",
        "From Port": "What's the departure port?",
        "To Port": "What's the destination port?",
        "Voyage ID": "What's the Voyage ID for this trip?",
        "Segment ID": "What's the Segment ID for this part of the voyage?",
        "Event Type": "What type of event is this report for?",
        "Latitude Degrees": "What's the latitude in degrees?",
        "Latitude Minutes": "What's the latitude in minutes?",
        "Latitude Direction": "Is the latitude North or South?",
        "Longitude Degrees": "What's the longitude in degrees?",
        "Longitude Minutes": "What's the longitude in minutes?",
        "Longitude Direction": "Is the longitude East or West?",
        "ME LFO (mt)": "How much LFO did the Main Engine consume (in metric tons)?",
        "ME MGO (mt)": "How much MGO did the Main Engine consume (in metric tons)?",
        "ME LNG (mt)": "How much LNG did the Main Engine consume (in metric tons)?",
        "ME Other (mt)": "How much of other fuel types did the Main Engine consume (in metric tons)?",
        "AE LFO (mt)": "How much LFO did the Auxiliary Engines consume (in metric tons)?",
        "AE MGO (mt)": "How much MGO did the Auxiliary Engines consume (in metric tons)?",
        "AE LNG (mt)": "How much LNG did the Auxiliary Engines consume (in metric tons)?",
        "AE Other (mt)": "How much of other fuel types did the Auxiliary Engines consume (in metric tons)?",
    }
    return prompts.get(field, f"Please provide the value for {field}:")

def create_fields(fields, prefix, report_type):
    cols = st.columns(4)
    me_total_consumption = 0
    ae_total_consumption = 0
    me_fields_processed = False
    ae_fields_processed = False
    boiler_message_shown = False
    position_fields_processed = 0
    
    if "consumption" not in st.session_state:
        st.session_state.consumption = generate_random_consumption()
    me_lfo, ae_lfo = st.session_state.consumption
    
    lat_deg, lat_min, lat_dir, lon_deg, lon_min, lon_dir = generate_random_position()
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")
    utc_offset = datetime.now(pytz.timezone('UTC')).astimezone().strftime('%z')
    from_port = random.choice(PORTS)
    to_port = random.choice([p for p in PORTS if p != from_port])
    voyage_type = random.choice(['L', 'B'])
    voyage_id = f"{random.randint(10, 99)}{voyage_type}"
    segment_id = str(random.randint(1, 5))
    vessel_name = generate_random_vessel_name()
    imo_number = generate_random_imo()
    
    for i, field in enumerate(fields):
        with cols[i % 4]:
            field_key = f"{prefix}_{field.lower().replace(' ', '_')}"
            
            if field_key in st.session_state.get('chatbot_filled_fields', {}):
                value = st.session_state['chatbot_filled_fields'][field_key]
            else:
                if field == "Vessel Name":
                    value = vessel_name
                elif field == "Vessel IMO":
                    value = imo_number
                elif field == "Local Date":
                    value = datetime.strptime(current_date, "%Y-%m-%d")
                elif field == "Local Time":
                    value = datetime.strptime(current_time, "%H:%M").time()
                elif field == "UTC Offset":
                    value = utc_offset
                elif field == "From Port":
                    value = from_port
                elif field == "To Port":
                    value = to_port
                elif field == "Voyage ID":
                    value = voyage_id
                elif field == "Segment ID":
                    value = segment_id
                elif field == "Event Type":
                    value = report_type
                elif field == "Latitude Degrees":
                    value = lat_deg
                elif field == "Latitude Minutes":
                    value = lat_min
                elif field == "Latitude Direction":
                    value = lat_dir
                elif field == "Longitude Degrees":
                    value = lon_deg
                elif field == "Longitude Minutes":
                    value = lon_min
                elif field == "Longitude Direction":
                    value = lon_dir
                elif field == "ME LFO (mt)":
                    value = me_lfo
                elif field == "AE LFO (mt)":
                    value = ae_lfo
                else:
                    value = None

            if isinstance(value, datetime):
                st.date_input(field, value=value, key=field_key)
            elif isinstance(value, datetime.time):
                st.time_input(field, value=value, key=field_key)
            elif field in ["Latitude Direction", "Longitude Direction"]:
                st.selectbox(field, options=["N", "S"] if "Latitude" in field else ["E", "W"], index=["N", "S", "E", "W"].index(value), key=field_key)
            elif field in ["From Port", "To Port"]:
                st.selectbox(field, options=PORTS, index=PORTS.index(value), key=field_key)
            elif any(unit in field for unit in ["(%)", "(mt)", "(kW)", "(°C)", "(bar)", "(g/kWh)", "(knots)", "(meters)", "(seconds)", "(degrees)"]):
                st.number_input(field, value=value if value is not None else 0.0, key=field_key)
            elif "Direction" in field and "degrees" not in field:
                st.selectbox(field, options=["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=field_key)
            else:
                st.text_input(field, value=value if value is not None else "", key=field_key)

            if field in ["ME LFO (mt)", "ME MGO (mt)", "ME LNG (mt)", "ME Other (mt)"]:
                me_total_consumption += float(value or 0)
                if field == "ME Other (mt)" and not me_fields_processed:
                    if me_total_consumption > 25:
                        st.markdown('<p class="info-message">Total ME consumption exceeds expected consumption of 25.</p>', unsafe_allow_html=True)
                    st.markdown('<p class="info-message">MFM figures since last report</p>', unsafe_allow_html=True)
                    me_fields_processed = True
            elif field in ["AE LFO (mt)", "AE MGO (mt)", "AE LNG (mt)", "AE Other (mt)"]:
                ae_total_consumption += float(value or 0)
                if field == "AE Other (mt)" and not ae_fields_processed:
                    if ae_total_consumption > 3:
                        st.markdown('<p class="info-message">Total AE consumption exceeds expected consumption of 3.</p>', unsafe_allow_html=True)
                    st.markdown('<p class="info-message">MFM figures since last report</p>', unsafe_allow_html=True)
                    ae_fields_processed = True

            if field == "Longitude Direction":
                position_fields_processed += 1
                if position_fields_processed == 6:
                    st.markdown('<p class="info-message">Current AIS position</p>', unsafe_allow_html=True)

    if me_total_consumption > 15 and not boiler_message_shown:
        st.markdown('<p class="info-message">Since Main Engine is running at more than 50% load, Boiler consumption is expected to be zero.</p>', unsafe_allow_html=True)

def create_form(report_type):
    st.header(f"New {report_type}")
    
    report_structure = REPORT_STRUCTURES.get(report_type, [])
    
    if not report_structure:
        st.error(f"No structure defined for report type: {report_type}")
        return False
    
    for section in report_structure:
        with st.expander(section, expanded=False):
            st.subheader(section)
            fields = SECTION_FIELDS.get(section, {})
            
            if isinstance(fields, dict):
                for subsection, subfields in fields.items():
                    st.subheader(subsection)
                    create_fields(subfields, f"{report_type}_{section}_{subsection}", report_type)
            elif isinstance(fields, list):
                create_fields(fields, f"{report_type}_{section}", report_type)
            else:
                st.error(f"Unexpected field type for section {section}: {type(fields)}")

    if st.button("Submit Report"):
        if validate_report(report_type):
            st.success(f"{report_type} submitted successfully!")
            return True
        else:
            st.error("Please correct the errors in the report before submitting.")
    return False

def validate_report(report_type):
    # Placeholder for validation logic
    return True

def create_collapsible_history_panel():
    with st.expander("Report History (for testing)", expanded=False):
        st.markdown('<div class="history-panel">', unsafe_allow_html=True)
        st.markdown("<h3>Recent Reports</h3>", unsafe_allow_html=True)
        
        if "report_history" not in st.session_state:
            st.session_state.report_history = []

        history = st.session_state.report_history + ["None"] * (4 - len(st.session_state.report_history))

        updated_history = []
        for i in range(4):
            selected_report = st.selectbox(
                f"Report {i+1}:",
                ["None"] + REPORT_TYPES,
                key=f"history_{i}",
                index=REPORT_TYPES.index(history[i]) + 1 if history[i] in REPORT_TYPES else 0
            )
            updated_history.append(selected_report)

        st.session_state.report_history = [report for report in updated_history if report != "None"]

        st.markdown('</div>', unsafe_allow_html=True)

def get_ai_response(user_input, last_reports):
    current_time = datetime.now(pytz.utc).strftime("%H:%M:%S")
    
    context = f"""
    The current UTC time is {current_time}. 
    The last reports submitted were: {' -> '.join(last_reports)}
    
    Please provide guidance based on this context and the user's input.
    Remember to only suggest reports from the provided list that make logical sense given the previous reports and maritime operations.
    Use your knowledge as an experienced seafarer to ensure the suggested reports follow a realistic sequence of events.
    """
    
    messages = [
        {"role": "system", "content": "You are an AI assistant for an advanced maritime reporting system, with the knowledge and experience of a seasoned maritime seafarer."},
        {"role": "system", "content": context},
        {"role": "user", "content": user_input}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"I'm sorry, but I encountered an error while processing your request: {str(e)}. Please try again later."

def create_chatbot(last_reports):
    st.header("AI Assistant")
    
    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Create a container for the chat messages
    chat_container = st.container()
    
    # Create an empty element to update with chat messages
    chat_placeholder = st.empty()
    
    # Display chat messages
    with chat_placeholder.container():
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">You: {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">AI: {message["content"]}</div>', unsafe_allow_html=True)
    
    # User input
    user_input = st.text_input("Type your message here:", key="user_input")
    if st.button("Send") or user_input:
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            if hasattr(st.session_state, 'current_report_type') and st.session_state.current_report_type:
                response = fill_form_fields(user_input, st.session_state.current_report_type)
            else:
                response = get_ai_response(user_input, last_reports)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Clear the input box
            st.session_state.user_input = ""
            
            # Update the chat display
            with chat_placeholder.container():
                for message in st.session_state.messages:
                    if message["role"] == "user":
                        st.markdown(f'<div class="user-message">You: {message["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="assistant-message">AI: {message["content"]}</div>', unsafe_allow_html=True)
                        
def fill_form_fields(user_input, report_type):
    report_structure = REPORT_STRUCTURES.get(report_type, [])
    all_fields = []
    for section in report_structure:
        fields = SECTION_FIELDS.get(section, {})
        if isinstance(fields, dict):
            for subsection, subfields in fields.items():
                all_fields.extend(subfields)
        elif isinstance(fields, list):
            all_fields.extend(fields)
    
    filled_fields = []
    invalid_fields = []
    
    for field in all_fields:
        field_key = f"{report_type}_{field.lower().replace(' ', '_')}"
        if field_key not in st.session_state.chatbot_filled_fields:
            if field.lower() in user_input.lower():
                value = user_input.lower().split(field.lower())[-1].strip()
                if validate_field_value(field, value):
                    st.session_state.chatbot_filled_fields[field_key] = value
                    filled_fields.append(field)
                else:
                    invalid_fields.append(field)
    
    if filled_fields:
        response = f"I've filled in the following fields: {', '.join(filled_fields)}. "
        if invalid_fields:
            response += f"However, the values for {', '.join(invalid_fields)} seem to be invalid. Please provide valid values for these fields. "
        response += "What's the next field you'd like to fill?"
    elif invalid_fields:
        response = f"The values for {', '.join(invalid_fields)} seem to be invalid. Please provide valid values for these fields."
    else:
        for field in all_fields:
            field_key = f"{report_type}_{field.lower().replace(' ', '_')}"
            if field_key not in st.session_state.chatbot_filled_fields:
                return get_field_prompt(field)
        response = "Great! All fields for this report have been filled. You can now submit the report or make any final adjustments."
    
    return response

def validate_field_value(field, value):
    if "Date" in field:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    elif "Time" in field:
        try:
            datetime.strptime(value, "%H:%M")
            return True
        except ValueError:
            return False
    elif any(unit in field for unit in ["(mt)", "(kW)", "(°C)", "(bar)", "(g/kWh)", "(knots)", "(meters)"]):
        try:
            float(value)
            return True
        except ValueError:
            return False
    elif "Direction" in field:
        return value.upper() in ["N", "S", "E", "W", "NE", "SE", "SW", "NW"]
    elif "Port" in field:
        return value in PORTS
    else:
        return True

def is_valid_report_sequence(last_reports, new_report):
    if not last_reports:
        return True
    
    last_report = last_reports[-1]
    
    sequence_rules = {
        "Arrival STS": ["Departure STS"],
        "Begin of offhire": ["End of offhire"],
        "Begin fuel change over": ["End fuel change over"],
        "Begin canal passage": ["End canal passage"],
        "Begin Anchoring/Drifting": ["End Anchoring/Drifting"],
        "Begin of deviation": ["End of deviation"],
        "Departure": ["Begin of sea passage", "Noon (Position) - Sea passage"],
        "Departure STS": ["Begin of sea passage", "Noon (Position) - Sea passage"],
        "End Anchoring/Drifting": ["Begin of sea passage", "Noon (Position) - Sea passage"],
    }
    
    if last_report in sequence_rules:
        return new_report in sequence_rules[last_report] or new_report.startswith("Noon")
    
    if new_report.startswith("Noon"):
        return True
    
    return new_report not in [item for sublist in sequence_rules.values() for item in sublist]

def main():
    st.title("OptiLog - AI-Enhanced Maritime Reporting System")
    
    if "report_history" not in st.session_state:
        st.session_state.report_history = []
    
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.markdown('<div class="reportSection">', unsafe_allow_html=True)
        if 'current_report_type' in st.session_state:
            create_form(st.session_state.current_report_type)
        else:
            st.write("Please use the AI Assistant to initiate a report.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        create_collapsible_history_panel()
        st.markdown('<div class="chatSection">', unsafe_allow_html=True)
        create_chatbot(st.session_state.report_history)
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.current_report_type = None
            st.session_state.report_history = []
            if 'chatbot_filled_fields' in st.session_state:
                del st.session_state.chatbot_filled_fields
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
