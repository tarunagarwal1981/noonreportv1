import streamlit as st
import openai
from datetime import datetime
import pytz
import os
import random
import string

# [All existing imports and constant definitions remain the same]

# New function to get field prompts
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

# Modified create_fields function
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
    
    # Generate random position and other data
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
            
            # Check if the field has been filled by the chatbot
            if field_key in st.session_state.get('chatbot_filled_fields', {}):
                value = st.session_state['chatbot_filled_fields'][field_key]
            else:
                # Use the existing logic to set default values
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

            # Display the field with the appropriate input type
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

            # Update consumption totals and display messages
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

            # Display position message
            if field == "Longitude Direction":
                position_fields_processed += 1
                if position_fields_processed == 6:
                    st.markdown('<p class="info-message">Current AIS position</p>', unsafe_allow_html=True)

    # Check if we need to display the Boiler message after all fields have been processed
    if me_total_consumption > 15 and not boiler_message_shown:
        st.markdown('<p class="info-message">Since Main Engine is running at more than 50% load, Boiler consumption is expected to be zero.</p>', unsafe_allow_html=True)

# Modified create_chatbot function
def create_chatbot(last_reports):
    st.header("AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Create a container for the chat messages with a fixed height and scrollbar
    chat_container = st.container()
    
    # Display chat messages in the scrollable container
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # User input
    if prompt := st.chat_input("How can I assist you with your maritime reporting?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Check if a form is already open
        if hasattr(st.session_state, 'current_report_type') and st.session_state.current_report_type:
            # Form is open, help fill the fields
            response = fill_form_fields(prompt, st.session_state.current_report_type)
        else:
            # No form open, use the regular AI response
            response = get_ai_response(prompt, last_reports)
            
            # Check if a specific report type is agreed upon
            for report_type in REPORT_TYPES:
                if f"Agreed. The form for {report_type}" in response:
                    if is_valid_report_sequence(last_reports, report_type):
                        st.session_state.current_report_type = report_type
                        st.session_state.show_form = True
                        # Initialize chatbot_filled_fields if not exists
                        if 'chatbot_filled_fields' not in st.session_state:
                            st.session_state.chatbot_filled_fields = {}
                        response += "\n\nSome fields have been automatically filled. Let's go through the remaining fields. What would you like to fill first?"
                        break
                    else:
                        st.warning(f"Invalid report sequence. {report_type} cannot follow the previous reports.")
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.experimental_rerun()

# New function to handle form field filling
def fill_form_fields(user_input, report_type):
    # Get the structure for the current report type
    report_structure = REPORT_STRUCTURES.get(report_type, [])
    all_fields = []
    for section in report_structure:
        fields = SECTION_FIELDS.get(section, {})
        if isinstance(fields, dict):
            for subsection, subfields in fields.items():
                all_fields.extend(subfields)
        elif isinstance(fields, list):
            all_fields.extend(fields)
    
    # Check if all fields are filled
    if all(f"{report_type}_{field.lower().replace(' ', '_')}" in st.session_state.chatbot_filled_fields for field in all_fields):
        return "Great! All fields for this report have been filled. You can now submit the report or make any final adjustments."
    
    # Try to extract field value from user input
    for field in all_fields:
        field_key = f"{report_type}_{field.lower().replace(' ', '_')}"
        if field_key not in st.session_state.chatbot_filled_fields:
            # Check if the user's input contains a value for this field
            if field.lower() in user_input.lower():
                # Extract the value (this is a simple extraction, you might need more sophisticated parsing)
                value = user_input.lower().split(field.lower())[-1].strip()
                # Validate the value
                if validate_field_value(field, value):
                    st.session_state.chatbot_filled_fields[field_key] = value
                    return f"I've filled in the {field} with {value}. What's the next field you'd like to fill?"
                else:
                    return f"The value for {field} doesn't seem to be valid. Could you please provide a valid value?"
    
    # If no field was filled, prompt for the next empty field
    for field in all_fields:
        field_key = f"{report_type}_{field.lower().replace(' ', '_')}"
        if field_key not in st.session_state.chatbot_filled_fields:
            return get_field_prompt(field)
    
    return "I'm not sure which field you're trying to fill. Could you please specify the field name and value?"

# New function to validate field values
def validate_field_value(field, value):
    # Add your validation logic here
    # For now, we'll just return True for all fields
    return True

# Modify the main function to use the scrollable chat
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

# Add this to your existing CSS
st.markdown("""
<style>
    ... [existing styles] ...
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .chat-container {
        height: 400px;
        overflow-y: auto;
        border: 1px solid #ddd;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Modify the create_chatbot function to use the scrollable container
def create_chatbot(last_reports):
    st.header("AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Create a container for the chat messages with a fixed height and scrollbar
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # User input
    if prompt := st.chat_input("How can I assist you with your maritime reporting?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Check if a form is already open
        if hasattr(st.session_state, 'current_report_type') and st.session_state.current_report_type:
            # Form is open, help fill the fields
            response = fill_form_fields(prompt, st.session_state.current_report_type)
        else:
            # No form open, use the regular AI response
            response = get_ai_response(prompt, last_reports)
            
            # Check if a specific report type is agreed upon
            for report_type in REPORT_TYPES:
                if f"Agreed. The form for {report_type}" in response:
                    if is_valid_report_sequence(last_reports, report_type):
                        st.session_state.current_report_type = report_type
                        st.session_state.show_form = True
                        # Initialize chatbot_filled_fields if not exists
                        if 'chatbot_filled_fields' not in st.session_state:
                            st.session_state.chatbot_filled_fields = {}
                        response += "\n\nSome fields have been automatically filled. Let's go through the remaining fields. What would you like to fill first?"
                        break
                    else:
                        st.warning(f"Invalid report sequence. {report_type} cannot follow the previous reports.")
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.experimental_rerun()

# Modify the fill_form_fields function to handle multiple fields and validation
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
            # Check if the user's input contains a value for this field
            if field.lower() in user_input.lower():
                # Extract the value (this is a simple extraction, you might need more sophisticated parsing)
                value = user_input.lower().split(field.lower())[-1].strip()
                # Validate the value
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
        # If no field was filled, prompt for the next empty field
        for field in all_fields:
            field_key = f"{report_type}_{field.lower().replace(' ', '_')}"
            if field_key not in st.session_state.chatbot_filled_fields:
                return get_field_prompt(field)
        response = "Great! All fields for this report have been filled. You can now submit the report or make any final adjustments."
    
    return response

# Enhance the validate_field_value function with some basic validations
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
        return True  # For fields without specific validation, accept any non-empty value
    
# Modify the main function to include the new chat interface
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
