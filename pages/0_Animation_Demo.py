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

VESSEL_TYPES = ["Oil Tanker", "LPG Tanker", "LNG Tanker"]

# Set page config
st.set_page_config(layout="wide", page_title="AI-Enhanced Maritime Reporting System")

# Custom CSS (unchanged)
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

# Define report types (unchanged)
REPORT_TYPES = [
    "Arrival", "Departure", "Begin of offhire", "End of offhire", "Arrival STS",
    "Departure STS", "STS", "Begin canal passage", "End canal passage",
    "Begin of sea passage", "End of sea passage", "Begin Anchoring/Drifting",
    "End Anchoring/Drifting", "Noon (Position) - Sea passage", "Noon (Position) - Port",
    "Noon (Position) - River", "Noon (Position) - Stoppage", "ETA update",
    "Begin fuel change over", "End fuel change over", "Change destination (Deviation)",
    "Begin of deviation", "End of deviation", "Entering special area", "Leaving special area"
]

# Define report structures (unchanged)
REPORT_STRUCTURES = {report_type: ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"] for report_type in REPORT_TYPES}
REPORT_STRUCTURES["ETA update"] = ["Vessel Data", "Voyage Data", "Position"]

# Define section fields (updated)
def get_section_fields(vessel_type):
    return {
        "Vessel Data": ["Vessel Name", "Vessel IMO"],
        "Voyage Data": ["Local Date", "Local Time", "UTC Offset", "Voyage ID", "Segment ID", "From Port", "To Port"],
        "Event Data": ["Event Type", "Time Elapsed (hours)", "Sailing Time (hours)", "Anchor Time (hours)", "Ice Time (hours)", "Maneuvering (hours)", "Loading/Unloading (hours)", "Drifting (hours)"] + (["DP Time (hours)"] if vessel_type != "Oil Tanker" else []),
        "Position": ["Latitude Degrees", "Latitude Minutes", "Latitude Direction", "Longitude Degrees", "Longitude Minutes", "Longitude Direction"],
        "Cargo": ["Cargo Volume (m3)"] if vessel_type in ["LPG Tanker", "LNG Tanker"] else ["Cargo Weight (mt)"],
        "Fuel Consumption": {
            "Main Engine": ["ME LFO (mt)", "ME MGO (mt)", "ME LNG (mt)", "ME Other (mt)", "ME Other Fuel Type"] + (["ME LPG Propane (mt)", "ME LPG Butane (mt)"] if vessel_type == "LPG Tanker" else []),
            "Auxiliary Engines": ["AE LFO (mt)", "AE MGO (mt)", "AE LNG (mt)", "AE Other (mt)", "AE Other Fuel Type"] + (["AE LPG Propane (mt)", "AE LPG Butane (mt)"] if vessel_type == "LPG Tanker" else []),
            "Boilers": ["Boiler LFO (mt)", "Boiler MGO (mt)", "Boiler LNG (mt)", "Boiler Other (mt)", "Boiler Other Fuel Type"] + (["Boiler LPG Propane (mt)", "Boiler LPG Butane (mt)"] if vessel_type == "LPG Tanker" else []),
            "IGG": ["IGG LFO (mt)", "IGG MGO (mt)", "IGG LNG (mt)", "IGG Other (mt)", "IGG Other Fuel Type"],
            "GCU": ["GCU LFO (mt)", "GCU MGO (mt)", "GCU LNG (mt)", "GCU Other (mt)", "GCU Other Fuel Type"] if vessel_type == "LNG Tanker" else [],
            "Incinerator": ["Incinerator LFO (mt)", "Incinerator MGO (mt)", "Incinerator LNG (mt)", "Incinerator Other (mt)", "Incinerator Other Fuel Type"]
        },
        "ROB": ["LFO ROB (mt)", "MGO ROB (mt)", "LNG ROB (mt)", "Other ROB (mt)", "Other Fuel Type ROB", "Total Fuel ROB (mt)"] + (["LPG Propane ROB (mt)", "LPG Butane ROB (mt)"] if vessel_type == "LPG Tanker" else []),
        "Fuel Allocation": {
            "Cargo Cooling" if vessel_type in ["LPG Tanker", "LNG Tanker"] else "Cargo Heating": 
                ["Cargo Cooling LFO (mt)", "Cargo Cooling MGO (mt)", "Cargo Cooling LNG (mt)", "Cargo Cooling Other (mt)", "Cargo Cooling Other Fuel Type"] + 
                (["Cargo Cooling LPG Propane (mt)", "Cargo Cooling LPG Butane (mt)"] if vessel_type == "LPG Tanker" else [])
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

# Define validation rules (updated)
VALIDATION_RULES = {
    "ME LFO (mt)": {"min": 0, "max": 25},
    "ME MGO (mt)": {"min": 0, "max": 25},
    "ME LNG (mt)": {"min": 0, "max": 25},
    "ME Other (mt)": {"min": 0, "max": 25},
    "ME LPG Propane (mt)": {"min": 0, "max": 25},
    "ME LPG Butane (mt)": {"min": 0, "max": 25},
    "AE LFO (mt)": {"min": 0, "max": 3},
    "AE MGO (mt)": {"min": 0, "max": 3},
    "AE LNG (mt)": {"min": 0, "max": 3},
    "AE Other (mt)": {"min": 0, "max": 3},
    "AE LPG Propane (mt)": {"min": 0, "max": 3},
    "AE LPG Butane (mt)": {"min": 0, "max": 3},
    "Boiler LFO (mt)": {"min": 0, "max": 4},
    "Boiler MGO (mt)": {"min": 0, "max": 4},
    "Boiler LNG (mt)": {"min": 0, "max": 4},
    "Boiler Other (mt)": {"min": 0, "max": 4},
    "Boiler LPG Propane (mt)": {"min": 0, "max": 4},
    "Boiler LPG Butane (mt)": {"min": 0, "max": 4},
}

# TRAINING_DATA (unchanged)
TRAINING_DATA = """
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
        {"role": "system", "content": TRAINING_DATA},
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
            temperature=1.0,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"I'm sorry, but I encountered an error while processing your request: {str(e)}. Please try again later."

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

def create_fields(fields, prefix, report_type, vessel_type):
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
            elif field.startswith("Latitude") or field.startswith("Longitude"):
                if "Degrees" in field:
                    value = st.number_input(field, value=lat_deg if "Latitude" in field else lon_deg, min_value=0, max_value=89 if "Latitude" in field else 179, key=field_key)
                elif "Minutes" in field:
                    value = st.number_input(field, value=lat_min if "Latitude" in field else lon_min, min_value=0.0, max_value=59.99, format="%.2f", key=field_key)
                elif "Direction" in field:
                    options = ["N", "S"] if "Latitude" in field else ["E", "W"]
                    default = lat_dir if "Latitude" in field else lon_dir
                    value = st.selectbox(field, options=options, index=options.index(default), key=field_key)
                position_fields_processed += 1
                
                if position_fields_processed == 6:
                    st.markdown('<p class="info-message">Current AIS position</p>', unsafe_allow_html=True)
            
            elif "LFO" in field or "MGO" in field or "LNG" in field or "Other" in field or "LPG" in field:
                if field.startswith("ME"):
                    max_val = 25.0
                    default_val = me_lfo if "LFO" in field else 0.0
                elif field.startswith("AE"):
                    max_val = 3.0
                    default_val = ae_lfo if "LFO" in field else 0.0
                elif field.startswith("Boiler"):
                    max_val = 4.0
                    default_val = 0.0
                else:
                    max_val = 25.0
                    default_val = 0.0
                
                value = st.number_input(field, value=default_val, min_value=0.0, max_value=max_val, step=0.1, key=field_key)
                
                if field.startswith("ME"):
                    me_total_consumption += value
                elif field.startswith("AE"):
                    ae_total_consumption += value
                
                if (field.startswith("ME") and "Other" in field and not me_fields_processed) or \
                   (field.startswith("AE") and "Other" in field and not ae_fields_processed):
                    total_consumption = me_total_consumption if field.startswith("ME") else ae_total_consumption
                    expected_consumption = 25 if field.startswith("ME") else 3
                    if total_consumption > expected_consumption:
                        st.markdown(f'<p class="info-message">Total {"ME" if field.startswith("ME") else "AE"} consumption exceeds expected consumption of {expected_consumption}.</p>', unsafe_allow_html=True)
                    st.markdown('<p class="info-message">MFM figures since last report</p>', unsafe_allow_html=True)
                    if field.startswith("ME"):
                        me_fields_processed = True
                    else:
                        ae_fields_processed = True
            
            elif field in VALIDATION_RULES:
                min_val, max_val = VALIDATION_RULES[field]["min"], VALIDATION_RULES[field]["max"]
                value = st.number_input(field, min_value=min_val, max_value=max_val, key=field_key)
                
                if value > max_val:
                    st.markdown(f'<p class="small-warning">Value must be less than or equal to {max_val}</p>', unsafe_allow_html=True)
            
            elif any(unit in field for unit in ["(%)", "(mt)", "(kW)", "(°C)", "(bar)", "(g/kWh)", "(knots)", "(meters)", "(seconds)", "(degrees)"]):
                value = st.number_input(field, key=field_key)
            elif "Direction" in field and "degrees" not in field:
                value = st.selectbox(field, options=["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=field_key)
            else:
                value = st.text_input(field, key=field_key)

    if me_total_consumption > 15 and not boiler_message_shown:
        st.markdown('<p class="info-message">Since Main Engine is running at more than 50% load, Boiler consumption is expected to be zero.</p>', unsafe_allow_html=True)

def create_form(report_type, vessel_type):
    st.header(f"New {report_type} for {vessel_type}")
    
    report_structure = REPORT_STRUCTURES.get(report_type, [])
    
    if not report_structure:
        st.error(f"No structure defined for report type: {report_type}")
        return False
    
    for section in report_structure:
        with st.expander(section, expanded=False):
            st.subheader(section)
            fields = get_section_fields(vessel_type).get(section, {})
            
            if isinstance(fields, dict):
                for subsection, subfields in fields.items():
                    st.subheader(subsection)
                    create_fields(subfields, f"{report_type}_{section}_{subsection}", report_type, vessel_type)
            elif isinstance(fields, list):
                create_fields(fields, f"{report_type}_{section}", report_type, vessel_type)
            else:
                st.error(f"Unexpected field type for section {section}: {type(fields)}")

    if st.button("Submit Report"):
        if validate_report(report_type, vessel_type):
            st.success(f"{report_type} for {vessel_type} submitted successfully!")
            return True
        else:
            st.error("Please correct the errors in the report before submitting.")
    return False
    
def validate_report(report_type, vessel_type):
    # Validation logic here
    # For example, checking if all required fields are filled and if the data is consistent (e.g., ROB calculations)
    # Placeholder for ROB validation
    fuel_types = ["LFO", "MGO", "LNG", "Other"] + (["LPG Propane", "LPG Butane"] if vessel_type == "LPG Tanker" else [])
    total_rob = 0
    for fuel in fuel_types:
        rob_key = f"{report_type}_ROB_{fuel.lower().replace(' ', '_')}_rob_(mt)"
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

VESSEL_TYPES = ["Oil Tanker", "LPG Tanker", "LNG Tanker"]

# Set page config
st.set_page_config(layout="wide", page_title="AI-Enhanced Maritime Reporting System")

# Custom CSS (unchanged)
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

# Define report types (unchanged)
REPORT_TYPES = [
    "Arrival", "Departure", "Begin of offhire", "End of offhire", "Arrival STS",
    "Departure STS", "STS", "Begin canal passage", "End canal passage",
    "Begin of sea passage", "End of sea passage", "Begin Anchoring/Drifting",
    "End Anchoring/Drifting", "Noon (Position) - Sea passage", "Noon (Position) - Port",
    "Noon (Position) - River", "Noon (Position) - Stoppage", "ETA update",
    "Begin fuel change over", "End fuel change over", "Change destination (Deviation)",
    "Begin of deviation", "End of deviation", "Entering special area", "Leaving special area"
]

# Define report structures (unchanged)
REPORT_STRUCTURES = {report_type: ["Vessel Data", "Voyage Data", "Event Data", "Position", "Cargo", "Fuel Consumption", "ROB", "Fuel Allocation", "Machinery", "Weather", "Draft"] for report_type in REPORT_TYPES}
REPORT_STRUCTURES["ETA update"] = ["Vessel Data", "Voyage Data", "Position"]

# Define section fields (updated)
def get_section_fields(vessel_type):
    return {
        "Vessel Data": ["Vessel Name", "Vessel IMO"],
        "Voyage Data": ["Local Date", "Local Time", "UTC Offset", "Voyage ID", "Segment ID", "From Port", "To Port"],
        "Event Data": ["Event Type", "Time Elapsed (hours)", "Sailing Time (hours)", "Anchor Time (hours)", "Ice Time (hours)", "Maneuvering (hours)", "Loading/Unloading (hours)", "Drifting (hours)"] + (["DP Time (hours)"] if vessel_type != "Oil Tanker" else []),
        "Position": ["Latitude Degrees", "Latitude Minutes", "Latitude Direction", "Longitude Degrees", "Longitude Minutes", "Longitude Direction"],
        "Cargo": ["Cargo Volume (m3)"] if vessel_type in ["LPG Tanker", "LNG Tanker"] else ["Cargo Weight (mt)"],
        "Fuel Consumption": {
            "Main Engine": ["ME LFO (mt)", "ME MGO (mt)", "ME LNG (mt)", "ME Other (mt)", "ME Other Fuel Type"] + (["ME LPG Propane (mt)", "ME LPG Butane (mt)"] if vessel_type == "LPG Tanker" else []),
            "Auxiliary Engines": ["AE LFO (mt)", "AE MGO (mt)", "AE LNG (mt)", "AE Other (mt)", "AE Other Fuel Type"] + (["AE LPG Propane (mt)", "AE LPG Butane (mt)"] if vessel_type == "LPG Tanker" else []),
            "Boilers": ["Boiler LFO (mt)", "Boiler MGO (mt)", "Boiler LNG (mt)", "Boiler Other (mt)", "Boiler Other Fuel Type"] + (["Boiler LPG Propane (mt)", "Boiler LPG Butane (mt)"] if vessel_type == "LPG Tanker" else []),
            "IGG": ["IGG LFO (mt)", "IGG MGO (mt)", "IGG LNG (mt)", "IGG Other (mt)", "IGG Other Fuel Type"],
            "GCU": ["GCU LFO (mt)", "GCU MGO (mt)", "GCU LNG (mt)", "GCU Other (mt)", "GCU Other Fuel Type"] if vessel_type == "LNG Tanker" else [],
            "Incinerator": ["Incinerator LFO (mt)", "Incinerator MGO (mt)", "Incinerator LNG (mt)", "Incinerator Other (mt)", "Incinerator Other Fuel Type"]
        },
        "ROB": ["LFO ROB (mt)", "MGO ROB (mt)", "LNG ROB (mt)", "Other ROB (mt)", "Other Fuel Type ROB", "Total Fuel ROB (mt)"] + (["LPG Propane ROB (mt)", "LPG Butane ROB (mt)"] if vessel_type == "LPG Tanker" else []),
        "Fuel Allocation": {
            "Cargo Cooling" if vessel_type in ["LPG Tanker", "LNG Tanker"] else "Cargo Heating": 
                ["Cargo Cooling LFO (mt)", "Cargo Cooling MGO (mt)", "Cargo Cooling LNG (mt)", "Cargo Cooling Other (mt)", "Cargo Cooling Other Fuel Type"] + 
                (["Cargo Cooling LPG Propane (mt)", "Cargo Cooling LPG Butane (mt)"] if vessel_type == "LPG Tanker" else [])
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

# Define validation rules (updated)
VALIDATION_RULES = {
    "ME LFO (mt)": {"min": 0, "max": 25},
    "ME MGO (mt)": {"min": 0, "max": 25},
    "ME LNG (mt)": {"min": 0, "max": 25},
    "ME Other (mt)": {"min": 0, "max": 25},
    "ME LPG Propane (mt)": {"min": 0, "max": 25},
    "ME LPG Butane (mt)": {"min": 0, "max": 25},
    "AE LFO (mt)": {"min": 0, "max": 3},
    "AE MGO (mt)": {"min": 0, "max": 3},
    "AE LNG (mt)": {"min": 0, "max": 3},
    "AE Other (mt)": {"min": 0, "max": 3},
    "AE LPG Propane (mt)": {"min": 0, "max": 3},
    "AE LPG Butane (mt)": {"min": 0, "max": 3},
    "Boiler LFO (mt)": {"min": 0, "max": 4},
    "Boiler MGO (mt)": {"min": 0, "max": 4},
    "Boiler LNG (mt)": {"min": 0, "max": 4},
    "Boiler Other (mt)": {"min": 0, "max": 4},
    "Boiler LPG Propane (mt)": {"min": 0, "max": 4},
    "Boiler LPG Butane (mt)": {"min": 0, "max": 4},
}

# TRAINING_DATA (unchanged)
TRAINING_DATA = """
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
        {"role": "system", "content": TRAINING_DATA},
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
            temperature=1.0,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"I'm sorry, but I encountered an error while processing your request: {str(e)}. Please try again later."

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

def create_fields(fields, prefix, report_type, vessel_type):
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
            elif field.startswith("Latitude") or field.startswith("Longitude"):
                if "Degrees" in field:
                    value = st.number_input(field, value=lat_deg if "Latitude" in field else lon_deg, min_value=0, max_value=89 if "Latitude" in field else 179, key=field_key)
                elif "Minutes" in field:
                    value = st.number_input(field, value=lat_min if "Latitude" in field else lon_min, min_value=0.0, max_value=59.99, format="%.2f", key=field_key)
                elif "Direction" in field:
                    options = ["N", "S"] if "Latitude" in field else ["E", "W"]
                    default = lat_dir if "Latitude" in field else lon_dir
                    value = st.selectbox(field, options=options, index=options.index(default), key=field_key)
                position_fields_processed += 1
                
                if position_fields_processed == 6:
                    st.markdown('<p class="info-message">Current AIS position</p>', unsafe_allow_html=True)
            
            elif "LFO" in field or "MGO" in field or "LNG" in field or "Other" in field or "LPG" in field:
                if field.startswith("ME"):
                    max_val = 25.0
                    default_val = me_lfo if "LFO" in field else 0.0
                elif field.startswith("AE"):
                    max_val = 3.0
                    default_val = ae_lfo if "LFO" in field else 0.0
                elif field.startswith("Boiler"):
                    max_val = 4.0
                    default_val = 0.0
                else:
                    max_val = 25.0
                    default_val = 0.0
                
                value = st.number_input(field, value=default_val, min_value=0.0, max_value=max_val, step=0.1, key=field_key)
                
                if field.startswith("ME"):
                    me_total_consumption += value
                elif field.startswith("AE"):
                    ae_total_consumption += value
                
                if (field.startswith("ME") and "Other" in field and not me_fields_processed) or \
                   (field.startswith("AE") and "Other" in field and not ae_fields_processed):
                    total_consumption = me_total_consumption if field.startswith("ME") else ae_total_consumption
                    expected_consumption = 25 if field.startswith("ME") else 3
                    if total_consumption > expected_consumption:
                        st.markdown(f'<p class="info-message">Total {"ME" if field.startswith("ME") else "AE"} consumption exceeds expected consumption of {expected_consumption}.</p>', unsafe_allow_html=True)
                    st.markdown('<p class="info-message">MFM figures since last report</p>', unsafe_allow_html=True)
                    if field.startswith("ME"):
                        me_fields_processed = True
                    else:
                        ae_fields_processed = True
            
            elif field in VALIDATION_RULES:
                min_val, max_val = VALIDATION_RULES[field]["min"], VALIDATION_RULES[field]["max"]
                value = st.number_input(field, min_value=min_val, max_value=max_val, key=field_key)
                
                if value > max_val:
                    st.markdown(f'<p class="small-warning">Value must be less than or equal to {max_val}</p>', unsafe_allow_html=True)
            
            elif any(unit in field for unit in ["(%)", "(mt)", "(kW)", "(°C)", "(bar)", "(g/kWh)", "(knots)", "(meters)", "(seconds)", "(degrees)"]):
                value = st.number_input(field, key=field_key)
            elif "Direction" in field and "degrees" not in field:
                value = st.selectbox(field, options=["N", "NE", "E", "SE", "S", "SW", "W", "NW"], key=field_key)
            else:
                value = st.text_input(field, key=field_key)

    if me_total_consumption > 15 and not boiler_message_shown:
        st.markdown('<p class="info-message">Since Main Engine is running at more than 50% load, Boiler consumption is expected to be zero.</p>', unsafe_allow_html=True)

def create_form(report_type, vessel_type):
    st.header(f"New {report_type} for {vessel_type}")
    
    report_structure = REPORT_STRUCTURES.get(report_type, [])
    
    if not report_structure:
        st.error(f"No structure defined for report type: {report_type}")
        return False
    
    for section in report_structure:
        with st.expander(section, expanded=False):
            st.subheader(section)
            fields = get_section_fields(vessel_type).get(section, {})
            
            if isinstance(fields, dict):
                for subsection, subfields in fields.items():
                    st.subheader(subsection)
                    create_fields(subfields, f"{report_type}_{section}_{subsection}", report_type, vessel_type)
            elif isinstance(fields, list):
                create_fields(fields, f"{report_type}_{section}", report_type, vessel_type)
            else:
                st.error(f"Unexpected field type for section {section}: {type(fields)}")

    if st.button("Submit Report"):
        if validate_report(report_type, vessel_type):
            st.success(f"{report_type} for {vessel_type} submitted successfully!")
            return True
        else:
            st.error("Please correct the errors in the report before submitting.")
    return False
    
def validate_report(report_type, vessel_type):
    # Validation logic here
    # For example, checking if all required fields are filled and if the data is consistent (e.g., ROB calculations)
    # Placeholder for ROB validation
    fuel_types = ["LFO", "MGO", "LNG", "Other"] + (["LPG Propane", "LPG Butane"] if vessel_type == "LPG Tanker" else [])
    total_rob = 0
    for fuel in fuel_types:
        rob_key = f"{report_type}_ROB_{fuel.lower().replace(' ', '_')}_rob_(mt)"
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
        
        # Check if a specific report type is agreed upon
        for report_type in REPORT_TYPES:
            if f"Agreed. The form for {report_type}" in response:
                if is_valid_report_sequence(last_reports, report_type):
                    st.session_state.current_report_type = report_type
                    st.session_state.show_form = True
                    break
                else:
                    st.warning(f"Invalid report sequence. {report_type} cannot follow the previous reports.")
        
        st.experimental_rerun()

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
    
    if "report_history" not in st.session_state:
        st.session_state.report_history = []
    
    if "vessel_type" not in st.session_state:
        st.session_state.vessel_type = "Oil Tanker"
    
    # Add vessel type selection dropdown
    st.session_state.vessel_type = st.selectbox("Select Vessel Type", VESSEL_TYPES, index=VESSEL_TYPES.index(st.session_state.vessel_type))
    
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.markdown('<div class="reportSection">', unsafe_allow_html=True)
        if 'current_report_type' in st.session_state:
            create_form(st.session_state.current_report_type, st.session_state.vessel_type)
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
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
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
    
    if "report_history" not in st.session_state:
        st.session_state.report_history = []
    
    if "vessel_type" not in st.session_state:
        st.session_state.vessel_type = "Oil Tanker"
    
    # Add vessel type selection dropdown
    st.session_state.vessel_type = st.selectbox("Select Vessel Type", VESSEL_TYPES, index=VESSEL_TYPES.index(st.session_state.vessel_type))
    
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.markdown('<div class="reportSection">', unsafe_allow_html=True)
        if st.session_state.get('show_form', False) and 'current_report_type' in st.session_state:
            create_form(st.session_state.current_report_type, st.session_state.vessel_type)
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
            st.session_state.show_form = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
