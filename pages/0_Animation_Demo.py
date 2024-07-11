import streamlit as st
import openai
from datetime import datetime
import pytz
import os
import random
import string


PORTS = [
    "Singapore", "Rotterdam", "Shanghai", "Ningbo-Zhoushan", "Guangzhou Harbor", "Busan",
    "Qingdao", "Hong Kong", "Tianjin", "Port Klang", "Antwerp", "Dubai Ports", "Xiamen",
    "Kaohsiung", "Hamburg", "Los Angeles", "Tanjung Pelepas", "Laem Chabang", "New York-New Jersey",
    "Dalian", "Tanjung Priok", "Valencia", "Colombo", "Ho Chi Minh City", "Algeciras"
]

VESSEL_PREFIXES = ["MV", "SS", "MT", "MSC", "CMA CGM", "OOCL", "Maersk", "Evergreen", "Cosco", "NYK"]
VESSEL_NAMES = ["Horizon", "Voyager", "Pioneer", "Adventurer", "Explorer", "Discovery", "Navigator", "Endeavour", "Challenger", "Trailblazer"]


# Set page config
st.set_page_config(layout="wide", page_title="AI-Enhanced Maritime Reporting System")

# Custom CSS for compact layout, history panel, and field prompts
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

# Define report types
REPORT_TYPES = [
    "Arrival", "Departure", "Begin of offhire", "End of offhire", "Arrival STS",
    "Departure STS", "STS", "Begin canal passage", "End canal passage",
    "Begin of sea passage", "End of sea passage", "Begin Anchoring/Drifting",
    "End Anchoring/Drifting", "Noon (Position) - Sea passage", "Noon (Position) - Port",
    "Noon (Position) - River", "Noon (Position) - Stoppage", "ETA update",
    "Begin fuel change over", "End fuel change over", "Change destination (Deviation)",
    "Begin of deviation", "End of deviation", "Entering special area", "Leaving special area"
]

# Define report structures
REPORT_STRUCTURES = {report_type: ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"] for report_type in REPORT_TYPES}
REPORT_STRUCTURES["ETA update"] = ["Vessel Data", "Voyage Data", "Position"]

# Define section fields
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

# Define validation rules
VALIDATION_RULES = {
    "ME LFO (mt)": {"min": 0, "max": 25},
    "ME MGO (mt)": {"min": 0, "max": 25},
    "ME LNG (mt)": {"min": 0, "max": 25},
    "ME Other (mt)": {"min": 0, "max": 25},
    "AE LFO (mt)": {"min": 0, "max": 3},
    "AE MGO (mt)": {"min": 0, "max": 3},
    "AE LNG (mt)": {"min": 0, "max": 3},
    "AE Other (mt)": {"min": 0, "max": 3},
    "Boiler LFO (mt)": {"min": 0, "max": 4},
    "Boiler MGO (mt)": {"min": 0, "max": 4},
    "Boiler LNG (mt)": {"min": 0, "max": 4},
    "Boiler Other (mt)": {"min": 0, "max": 4},
}

# Prepare the training data as a string
TRAINING_DATA = f"""
You are an AI assistant for an advanced maritime reporting system, with the knowledge and experience of a seasoned maritime seafarer. Your role is to guide users through creating various types of maritime reports, ensuring compliance with industry standards and regulations while maintaining a logical sequence of events. 
Keep your responses as short and crisp and easy to understand as possible. While suggesting the reports just suggest the name of the reports not their explanations. If there is no Reports History allow user to start any report.
Valid report types: {', '.join(REPORT_TYPES)}

Key features:
1. Error reduction and data completion assistance
2. Insights generation based on reported data
3. Streamlined reporting process
4. Enhanced accuracy in maritime operational reporting

When suggesting follow-up reports, carefully consider the history of the last 3-4 reports and the logical sequence of maritime operations. Only suggest reports from the provided list that make sense given the current context and previous reports. For example:

1. An "Arrival STS" report must precede a "Departure STS" report.
2. "Begin of sea passage" should follow a departure-type report (e.g., "Departure", "Departure STS", "End Anchoring/Drifting").
3. "Noon" reports are regular and can follow most report types during a voyage.
4. "Begin" type reports (e.g., "Begin of offhire", "Begin fuel change over") must be followed by their corresponding "End" reports before suggesting unrelated reports.
5. If "Begin" report is not there then "End" report should not be suggested.

When a user agrees to create a specific report, inform them that the form will appear on the left side of the page with the relevant sections for that report type.

Provide concise and helpful guidance throughout the report creation process. If a user agrees to create a report, respond with "Agreed. The form for [REPORT TYPE] will now appear on the left side of the page."

Remember to provide appropriate reminders and follow-up suggestions based on the current report context and the logical sequence of maritime operations.
"""

def get_ai_response(user_input, last_reports, context):
    current_time = datetime.now(pytz.utc).strftime("%H:%M:%S")
    
    messages = [
        {"role": "system", "content": TRAINING_DATA},
        {"role": "system", "content": f"The current UTC time is {current_time}. The last reports submitted were: {' -> '.join(last_reports)}"},
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

def get_empty_fields(report_type, section):
    empty_fields = []
    fields = SECTION_FIELDS.get(section, {})
    
    if isinstance(fields, dict):
        for subsection, subfields in fields.items():
            for field in subfields:
                field_key = f"{report_type}_{section}_{subsection}_{field.lower().replace(' ', '_')}"
                if field_key not in st.session_state or not st.session_state[field_key]:
                    empty_fields.append(field)
    elif isinstance(fields, list):
        for field in fields:
            field_key = f"{report_type}_{section}_{field.lower().replace(' ', '_')}"
            if field_key not in st.session_state or not st.session_state[field_key]:
                empty_fields.append(field)
    
    return empty_fields

def update_field_value(report_type, section, field, value):
    fields = SECTION_FIELDS.get(section, {})
    
    if isinstance(fields, dict):
        for subsection, subfields in fields.items():
            if field in subfields:
                field_key = f"{report_type}_{section}_{subsection}_{field.lower().replace(' ', '_')}"
                st.session_state[field_key] = value
                return True
    elif isinstance(fields, list):
        if field in fields:
            field_key = f"{report_type}_{section}_{field.lower().replace(' ', '_')}"
            st.session_state[field_key] = value
            return True
    
    return False


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

def create_fields(fields, prefix, report_type):
    cols = st.columns(4)  # Create 4 columns
    me_total_consumption = 0
    ae_total_consumption = 0
    me_fields_processed = False
    ae_fields_processed = False
    boiler_message_shown = False
    position_fields_processed = 0
    
    if "consumption" not in st.session_state:
        st.session_state.consumption = generate_random_consumption()
    me_lfo, ae_lfo = st.session_state.consumption
    
    # Generate random position
    lat_deg, lat_min, lat_dir, lon_deg, lon_min, lon_dir = generate_random_position()
    
    # Get current date, time, and UTC offset
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")
    utc_offset = datetime.now(pytz.timezone('UTC')).astimezone().strftime('%z')
    
    # Generate random voyage and vessel data
    from_port = random.choice(PORTS)
    to_port = random.choice([p for p in PORTS if p != from_port])
    voyage_type = random.choice(['L', 'B'])
    voyage_id = f"{random.randint(10, 99)}{voyage_type}"
    segment_id = str(random.randint(1, 5))
    vessel_name = generate_random_vessel_name()
    imo_number = generate_random_imo()
    
    for i, field in enumerate(fields):
        with cols[i % 4]:  # This will cycle through the columns
            field_key = f"{prefix}_{field.lower().replace(' ', '_')}"
            
            if field == "Vessel Name":
                value = st.text_input(field, value=vessel_name, key=field_key)
            elif field == "Vessel IMO":
                value = st.text_input(field, value=imo_number, key=field_key)
            elif field == "Local Date":
                value = st.date_input(field, value=datetime.strptime(current_date, "%Y-%m-%d"), key=field_key)
            elif field == "Local Time":
                value = st.time_input(field, value=datetime.strptime(current_time, "%H:%M").time(), key=field_key)
            elif field == "UTC Offset":
                value = st.text_input(field, value=utc_offset, key=field_key)
            elif field == "From Port":
                value = st.selectbox(field, options=PORTS, index=PORTS.index(from_port), key=field_key)
            elif field == "To Port":
                value = st.selectbox(field, options=PORTS, index=PORTS.index(to_port), key=field_key)
            elif field == "Voyage ID":
                value = st.text_input(field, value=voyage_id, key=field_key)
            elif field == "Segment ID":
                value = st.text_input(field, value=segment_id, key=field_key)
            elif field == "Event Type":
                value = st.text_input(field, value=report_type, key=field_key)
            elif field == "Latitude Degrees":
                value = st.number_input(field, value=lat_deg, min_value=0, max_value=89, key=field_key)
                position_fields_processed += 1
            elif field == "Latitude Minutes":
                value = st.number_input(field, value=lat_min, min_value=0.0, max_value=59.99, format="%.2f", key=field_key)
                position_fields_processed += 1
            elif field == "Latitude Direction":
                value = st.selectbox(field, options=["N", "S"], index=["N", "S"].index(lat_dir), key=field_key)
                position_fields_processed += 1
            elif field == "Longitude Degrees":
                value = st.number_input(field, value=lon_deg, min_value=0, max_value=179, key=field_key)
                position_fields_processed += 1
            elif field == "Longitude Minutes":
                value = st.number_input(field, value=lon_min, min_value=0.0, max_value=59.99, format="%.2f", key=field_key)
                position_fields_processed += 1
            elif field == "Longitude Direction":
                value = st.selectbox(field, options=["E", "W"], index=["E", "W"].index(lon_dir), key=field_key)
                position_fields_processed += 1
                
                # Display AIS position message after all position fields have been processed
                if position_fields_processed == 6:
                    st.markdown('<p class="info-message">Current AIS position</p>', unsafe_allow_html=True)
            
            elif field in ["ME LFO (mt)", "ME MGO (mt)", "ME LNG (mt)", "ME Other (mt)"]:
                if field == "ME LFO (mt)":
                    value = st.number_input(field, value=me_lfo, min_value=0.0, max_value=25.0, step=0.1, key=field_key)
                else:
                    value = st.number_input(field, min_value=0.0, max_value=25.0, step=0.1, key=field_key)
                
                me_total_consumption += value
                
                if field == "ME Other (mt)" and not me_fields_processed:
                    if me_total_consumption > 25:
                        st.markdown('<p class="info-message">Total ME consumption exceeds expected consumption of 25.</p>', unsafe_allow_html=True)
                    st.markdown('<p class="info-message">MFM figures since last report</p>', unsafe_allow_html=True)
                    me_fields_processed = True
            elif field in ["AE LFO (mt)", "AE MGO (mt)", "AE LNG (mt)", "AE Other (mt)"]:
                if field == "AE LFO (mt)":
                    value = st.number_input(field, value=ae_lfo, min_value=0.0, max_value=3.0, step=0.1, key=field_key)
                else:
                    value = st.number_input(field, min_value=0.0, max_value=3.0, step=0.1, key=field_key)
                
                ae_total_consumption += value
                
                if field == "AE Other (mt)" and not ae_fields_processed:
                    if ae_total_consumption > 3:
                        st.markdown('<p class="info-message">Total AE consumption exceeds expected consumption of 3.</p>', unsafe_allow_html=True)
                    st.markdown('<p class="info-message">MFM figures since last report</p>', unsafe_allow_html=True)
                    ae_fields_processed = True
            elif field.startswith("Boiler"):
                value = st.number_input(field, min_value=0.0, max_value=4.0, step=0.1, key=field_key)
                
                # Display Boiler consumption message if ME total consumption > 15
                if me_total_consumption > 15 and not boiler_message_shown:
                    st.markdown('<p class="info-message">Since Main Engine is running at more than 50% load, Boiler consumption is expected to be zero.</p>', unsafe_allow_html=True)
                    boiler_message_shown = True
            elif field in VALIDATION_RULES:
                min_val, max_val = VALIDATION_RULES[field]["min"], VALIDATION_RULES[field]["max"]
                value = st.number_input(field, min_value=min_val, max_value=max_val, key=field_key)
                
                # Only show the warning if the value exceeds the maximum
                if value > max_val:
                    st.markdown(f'<p class="small-warning">Value must be less than or equal to {max_val}</p>', unsafe_allow_html=True)
            elif any(unit in field for unit in ["(%)", "(mt)", "(kW)", "(°C)", "(bar)", "(g/kWh)", "(knots)", "(meters)", "(seconds)", "(degrees)"]):
                value = st.number_input(field, key=field_key)
            elif "Direction" in field and "degrees" not in field:
                value = st.selectbox(field, options=["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=field_key)
            else:
                value = st.text_input(field, key=field_key)

    # Check if we need to display the Boiler message after all fields have been processed
    if me_total_consumption > 15 and not boiler_message_shown:
        st.markdown('<p class="info-message">Since Main Engine is running at more than 50% load, Boiler consumption is expected to be zero.</p>', unsafe_allow_html=True)

def get_next_section(report_type, current_section):
    sections = REPORT_STRUCTURES[report_type]
    current_index = sections.index(current_section)
    if current_index < len(sections) - 1:
        return sections[current_index + 1]
    return None

def create_form(report_type):
    st.header(f"New {report_type}")
    
    report_structure = REPORT_STRUCTURES.get(report_type, [])
    
    if not report_structure:
        st.error(f"No structure defined for report type: {report_type}")
        return False
    
    for section in report_structure:
        with st.expander(section, expanded=(section == st.session_state.current_section)):
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
            st.session_state.current_report_type = None
            st.session_state.current_section = None
            st.session_state.current_field = None
            return True
        else:
            st.error("Please correct the errors in the report before submitting.")
    return False
    
def validate_report(report_type):
    # Validation logic here
    # For example, checking if all required fields are filled and if the data is consistent (e.g., ROB calculations)
    # Placeholder for ROB validation
    fuel_types = ["LFO", "MGO", "LNG", "Other"]
    total_rob = 0
    for fuel in fuel_types:
        rob_key = f"{report_type}_ROB_{fuel.lower()}_rob_(mt)"
        if rob_key in st.session_state:
            total_rob += st.session_state[rob_key]
    
    calculated_total = total_rob
    reported_total_key = f"{report_type}_ROB_total_fuel_rob_(mt)"
    if reported_total_key in st.session_state:
        reported_total = st.session_state[reported_total_key]
        if abs(calculated_total - reported_total) > 0.1:  # Allow for small rounding differences
            st.warning(f"Total Fuel ROB ({reported_total}) doesn't match the sum of individual fuel ROBs ({calculated_total})")
            return False
    
    return True  # If all validations pass

def create_collapsible_history_panel():
    with st.expander("Report History (for testing)", expanded=False):
        st.markdown('<div class="history-panel">', unsafe_allow_html=True)
        st.markdown("<h3>Recent Reports</h3>", unsafe_allow_html=True)
        
        if "report_history" not in st.session_state:
            st.session_state.report_history = []

        # Ensure we always have 4 slots for history, filling with "None" if needed
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

        # Update session state outside of the loop
        st.session_state.report_history = [report for report in updated_history if report != "None"]

        st.markdown('</div>', unsafe_allow_html=True)

def get_next_logical_report(last_report):
    sequence_rules = {
        "Arrival": ["Departure", "Begin of offhire"],
        "Departure": ["Arrival", "Begin of sea passage", "Noon (Position) - Sea passage"],
        "Begin of offhire": ["End of offhire"],
        "End of offhire": ["Departure", "Begin of sea passage"],
        "Arrival STS": ["Departure STS"],
        "Departure STS": ["Arrival", "Begin of sea passage", "Noon (Position) - Sea passage"],
        "Begin of sea passage": ["Noon (Position) - Sea passage", "End of sea passage"],
        "End of sea passage": ["Arrival", "Noon (Position) - Port"],
        "Begin Anchoring/Drifting": ["End Anchoring/Drifting", "Noon (Position) - Stoppage"],
        "End Anchoring/Drifting": ["Departure", "Begin of sea passage"],
        "Noon (Position) - Sea passage": ["Noon (Position) - Sea passage", "End of sea passage", "Arrival"],
        "Noon (Position) - Port": ["Departure", "Noon (Position) - Port"],
        "Noon (Position) - River": ["Noon (Position) - River", "Arrival"],
        "Noon (Position) - Stoppage": ["End Anchoring/Drifting", "Noon (Position) - Stoppage"],
        "Begin fuel change over": ["End fuel change over"],
        "End fuel change over": ["Noon (Position) - Sea passage"],
        "Begin of deviation": ["End of deviation"],
        "End of deviation": ["Noon (Position) - Sea passage", "Arrival"],
        "Entering special area": ["Leaving special area"],
        "Leaving special area": ["Noon (Position) - Sea passage"]
    }
    return sequence_rules.get(last_report, ["Noon (Position) - Sea passage"])

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_report_type" not in st.session_state:
        st.session_state.current_report_type = None
    if "current_section" not in st.session_state:
        st.session_state.current_section = None
    if "current_field" not in st.session_state:
        st.session_state.current_field = None
    if "show_form" not in st.session_state:
        st.session_state.show_form = False
    if "report_history" not in st.session_state:
        st.session_state.report_history = []
    if "form_filling_mode" not in st.session_state:
        st.session_state.form_filling_mode = False


def create_chatbot(last_reports):
    st.header("AI Assistant")
    
    initialize_session_state()

    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("How can I assist you with your maritime reporting?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            if st.session_state.form_filling_mode:
                response = handle_form_filling(prompt, last_reports)
            else:
                response = handle_report_selection(prompt, last_reports)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.experimental_rerun()

def handle_form_filling(prompt, last_reports):
    context = f"We are currently filling out the {st.session_state.current_report_type} report, in the {st.session_state.current_section} section. The current field being discussed is {st.session_state.current_field}."
    response = get_ai_response(prompt, last_reports, context)
    
    if st.session_state.current_field:
        if "leave this field empty" in prompt.lower():
            st.session_state.current_field = None
        else:
            update_field_value(st.session_state.current_report_type, st.session_state.current_section, st.session_state.current_field, prompt)
            st.session_state.current_field = None
    
    empty_fields = get_empty_fields(st.session_state.current_report_type, st.session_state.current_section)
    if not empty_fields:
        st.session_state.current_section = get_next_section(st.session_state.current_report_type, st.session_state.current_section)
        if st.session_state.current_section:
            response += f"\n\nThis section is now complete. Let's move on to the {st.session_state.current_section} section."
        else:
            response += "\n\nAll sections are complete. You can now submit the report."
            st.session_state.form_filling_mode = False
    elif not st.session_state.current_field:
        st.session_state.current_field = empty_fields[0]
        response += f"\n\nLet's fill in the {st.session_state.current_field} field. What value should we use?"
    
    return response

def handle_report_selection(prompt, last_reports):
    if "new report" in prompt.lower():
        if st.session_state.report_history:
            last_report = st.session_state.report_history[-1]
            next_reports = get_next_logical_report(last_report)
            return f"Based on your last report ({last_report}), the next logical report(s) could be: {', '.join(next_reports)}. Which one would you like to create?"
        else:
            return "Since there is no recent report history, you can start with any report. What type of report would you like to create?"
    elif any(report_type.lower() in prompt.lower() for report_type in REPORT_TYPES):
        for report_type in REPORT_TYPES:
            if report_type.lower() in prompt.lower():
                st.session_state.current_report_type = report_type
                st.session_state.show_form = True
                st.session_state.current_section = REPORT_STRUCTURES[report_type][0]
                st.session_state.form_filling_mode = True
                return f"Agreed. The form for {report_type} will now appear on the left side of the page. Let's start filling out the {st.session_state.current_section} section."
    else:
        return get_ai_response(prompt, last_reports, "We are in the process of selecting a report type.")
        
def is_valid_report_sequence(last_reports, new_report):
    if not last_reports:
        return True
    
    last_report = last_reports[-1]
    
    # Define rules for report sequences
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
    
    # Check if the new report is valid based on the last report
    if last_report in sequence_rules:
        return new_report in sequence_rules[last_report] or new_report.startswith("Noon")
    
    # Allow "Noon" reports after most report types
    if new_report.startswith("Noon"):
        return True
    
    # For reports not explicitly defined in rules, allow them if they're not breaking any sequence
    return new_report not in [item for sublist in sequence_rules.values() for item in sublist]

def main():
    st.title("OptiLog - AI-Enhanced Maritime Reporting System")
    
    initialize_session_state()
    
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.markdown('<div class="reportSection">', unsafe_allow_html=True)
        if st.session_state.current_report_type:
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
            st.session_state.current_section = None
            st.session_state.current_field = None
            st.session_state.show_form = False
            st.session_state.report_history = []
            st.session_state.form_filling_mode = False
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
