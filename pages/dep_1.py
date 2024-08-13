import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import uuid
import random

st.set_page_config(layout="wide", page_title="Maritime Reporting Portal")

def create_voyage_timeline(vessel_info, voyage_info, segment_info):
    # Vessel Info
    col1, col2, col3 = st.columns(3)
    col1.write(f"**Vessel:** {vessel_info['name']}")
    col2.write(f"**IMO:** {vessel_info['imo']}")
    col3.write(f"**Type:** {vessel_info['type']}")

    # Voyage Info
    st.write(f"**Voyage ID:** {voyage_info['voyageId']} | **{segment_info['vesselCondition']}** | "
             f"**CP Speed:** {segment_info['speedOrder']} knots | "
             f"**CP Consumption:** {segment_info['cpConsumption']} mT/day")

    # Timeline
    ports = [
        {"name": "Rotterdam", "unlocode": "NLRTM", "date": "22/05/2024"},
        {"name": "Port Said", "unlocode": "EGPSD", "date": "01/06/2024"},
        {"name": "Jeddah", "unlocode": "SAJED", "date": "10/06/2024"},
        {"name": "Colombo", "unlocode": "LKCMB", "date": "20/06/2024"},
        {"name": "Singapore", "unlocode": "SGSIN", "date": "01/07/2024"},
        {"name": "Lagos", "unlocode": "NGLOS", "date": "22/07/2024"}
    ]

     # Custom CSS for port information
    st.markdown("""
    <style>
    .port-info {
        font-size: 12px;
    }
    .port-info strong {
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display ports with custom CSS class
    cols = st.columns(len(ports))
    for i, port in enumerate(ports):
        with cols[i]:
            st.markdown(f"""
            <div class="port-info">
                <strong>{port['name']}</strong><br>
                {port['unlocode']}<br>
                {port['date']}
            </div>
            """, unsafe_allow_html=True)


    # Custom HTML for timeline line with segment IDs
    timeline_html = """
    <style>
        .timeline-container {
            position: relative;
            width: 85%;
            height: 40px;
            margin-top: 10px;
        }
        .timeline-line {
            position: absolute;
            top: 25%;
            left: 0;
            right: 0;
            height: 2px;
            background-color: #000;
        }
        .timeline-dot {
            position: absolute;
            top: 25%;
            width: 10px;
            height: 10px;
            background-color: #000;
            border-radius: 50%;
            transform: translate(-50%, -50%);
        }
        .segment-id {
            position: absolute;
            top: 75%;
            font-size: 12px;
            transform: translate(-50%, -50%);
        }
    </style>
    <div class="timeline-container">
        <div class="timeline-line"></div>
    """

    for i in range(len(ports)):
        position = i * (100 / (len(ports) - 1))
        timeline_html += f'<div class="timeline-dot" style="left: {position}%;"></div>'
        if i < len(ports) - 1:
            segment_position = (i + 0.5) * (100 / (len(ports) - 1))
            timeline_html += f'<div class="segment-id" style="left: {segment_position}%;">SEG00{i+1}</div>'

    timeline_html += "</div>"

    st.markdown(timeline_html, unsafe_allow_html=True)

def main():
    vessel_info = {
        "name": "Ocean Explorer",
        "imo": "1234567",
        "type": "Tanker"
    }

    voyage_info = {
        "voyageId": "VOY123456",
    }

    segment_info = {
        "vesselCondition": "Laden",
        "voyageType": "One-way",
        "speedOrder": "12.5",
        "cpConsumption": f"{random.uniform(20, 25):.1f}"
    }

    create_voyage_timeline(vessel_info, voyage_info, segment_info)

    st.title("Maritime Reporting Portal")

    
    # Departure Report Selection
    st.markdown("<h2 style='text-align: center;'>Departure Report Selection</h2>", unsafe_allow_html=True)
    
    # Arrange the noon report checkboxes in rows of three
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        noon_at_portshift = st.checkbox("Departure for Berth Shifting")
    with col2:
        noon_at_port = st.checkbox("Departure Port")
    with col3:
        noon_at_anchor = st.checkbox("Departure Anchor")
    with col4:
        noon_at_drifting = st.checkbox("Departure Drifting")  
    with col5:
        noon_at_sts = st.checkbox("Departure STS")    
    
    # Display the relevant form based on the selected checkbox
    if noon_at_portshift:
        st.markdown("### Departure for Berth Shifting")
        display_base_report_form()
    if noon_at_port:
        st.markdown("### Departure Port")
        display_base_report_form()
    if noon_at_anchor:
        st.markdown("### Departure Anchor")
        display_custom_report_form("Departure Anchor")
    if noon_at_drifting:
        st.markdown("### Departure Drifting")
        display_base_report_form()
    if noon_at_sts:
        st.markdown("### Departure STS")
        display_base_report_form()    
        
def display_base_report_form():
    sections = [
        "Speed, Position and Navigation",
        "Special Events",
        "Weather and Sea Conditions",
        "Cargo and Stability",
        "Fuel Consumption",
        "Machinery",
        "Environmental Compliance",
        "Miscellaneous Consumables",
    ]

    for section in sections:
        with st.expander(f"#### {section}"):
            function_name = f"display_{section.lower().replace(' ', '_').replace(',', '')}"
            if function_name in globals():
                globals()[function_name]()
            else:
                st.write(f"Function {function_name} not found.")

    if st.button("Submit Report", type="primary", key=f"submit_report_{uuid.uuid4()}"):
        st.success("Report submitted successfully!")


def display_custom_report_form(noon_report_type):
    st.write(f"Displaying custom form for: {noon_report_type}")
    
    sections = [
        "Speed, Position and Navigation",
        "Special Events",
        "Weather and Sea Conditions",
        "Cargo and Stability",
        "Fuel Consumption",
        "Machinery",
        "Environmental Compliance",
        "Miscellaneous Consumables",
    ]

    for section in sections:
        with st.expander(f"#### {section}"):
            function_name = f"display_custom_{section.lower().replace(' ', '_').replace(',', '')}"
            if function_name in globals():
                globals()[function_name](noon_report_type)
            else:
                st.write(f"Custom function {function_name} not found. Displaying default section.")
                display_default_section(section)

    if st.button("Submit Report", type="primary", key=f"submit_report_{uuid.uuid4()}"):
        st.success("Report submitted successfully!")



def display_special_events():
    st.subheader("Special Events")

    columns = [
        "Event", "Start Date Time", "Start Lat", "Start Long", "End Date Time",
        "End Lat", "End Long", "Distance Travelled", "Total Consumption", "Consumption Tank Name"
    ]
    
    if 'special_events_df' not in st.session_state:
        default_row = {
            "Event": "Off-hire",
            "Start Date Time": datetime.now(),
            "Start Lat": "0.0",
            "Start Long": "0.0",
            "End Date Time": datetime.now(),
            "End Lat": "0.0",
            "End Long": "0.0",
            "Distance Travelled": 0.0,
            "Total Consumption": 0.0,
            "Consumption Tank Name": "Tank 1"
        }
        st.session_state.special_events_df = pd.DataFrame([default_row])

    edited_df = st.data_editor(
        st.session_state.special_events_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Event": st.column_config.SelectboxColumn(
                "Event", width="medium",
                options=[
                    "Off-hire", "ECA Transit", "Fuel Changeover", "Stoppage",
                    "Deviation - Heavy weather", "Deviation - SAR operation",
                    "Deviation - Navigational area Warning", "Deviation - Med-evac",
                    "Deviation - Others", "Transiting Special Area - JWC area",
                    "Transiting Special Area - IWL", "Transiting Special Area - ICE regions",
                    "Transiting Special Area - HRA"
                ],
            ),
            "Start Date Time": st.column_config.DatetimeColumn(
                "Start Date Time", format="DD/MM/YYYY HH:mm", step=60
            ),
            "End Date Time": st.column_config.DatetimeColumn(
                "End Date Time", format="DD/MM/YYYY HH:mm", step=60
            ),
            "Distance Travelled": st.column_config.NumberColumn(
                "Distance Travelled", min_value=0, max_value=1000, step=0.1, format="%.1f"
            ),
            "Total Consumption": st.column_config.NumberColumn(
                "Total Consumption", min_value=0, max_value=1000, step=0.1, format="%.1f"
            ),
            "Consumption Tank Name": st.column_config.SelectboxColumn(
                "Consumption Tank Name", options=[f"Tank {i}" for i in range(1, 9)]
            ),
        }
    )

    st.session_state.special_events_df = edited_df

def display_custom_special_events(noon_report_type):
    st.subheader("Special Events")

    columns = [
        "Event", "Start Date Time", "Start Lat", "Start Long", "End Date Time",
        "End Lat", "End Long", "Distance Travelled", "Total Consumption", "Consumption Tank Name"
    ]
    
    if 'special_events_df' not in st.session_state:
        default_row = {
            "Event": "Off-hire",
            "Start Date Time": datetime.now(),
            "Start Lat": "0.0",
            "Start Long": "0.0",
            "End Date Time": datetime.now(),
            "End Lat": "0.0",
            "End Long": "0.0",
            "Distance Travelled": 0.0,
            "Total Consumption": 0.0,
            "Consumption Tank Name": "Tank 1"
        }
        st.session_state.special_events_df = pd.DataFrame([default_row])

    edited_df = st.data_editor(
        st.session_state.special_events_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Event": st.column_config.SelectboxColumn(
                "Event", width="medium",
                options=[
                    "Off-hire", "ECA Transit", "Fuel Changeover", "Stoppage",
                    "Deviation - Heavy weather", "Deviation - SAR operation",
                    "Deviation - Navigational area Warning", "Deviation - Med-evac",
                    "Deviation - Others", "Transiting Special Area - JWC area",
                    "Transiting Special Area - IWL", "Transiting Special Area - ICE regions",
                    "Transiting Special Area - HRA"
                ],
            ),
            "Start Date Time": st.column_config.DatetimeColumn(
                "Start Date Time", format="DD/MM/YYYY HH:mm", step=60
            ),
            "End Date Time": st.column_config.DatetimeColumn(
                "End Date Time", format="DD/MM/YYYY HH:mm", step=60
            ),
            "Distance Travelled": st.column_config.NumberColumn(
                "Distance Travelled", min_value=0, max_value=1000, step=0.1, format="%.1f"
            ),
            "Total Consumption": st.column_config.NumberColumn(
                "Total Consumption", min_value=0, max_value=1000, step=0.1, format="%.1f"
            ),
            "Consumption Tank Name": st.column_config.SelectboxColumn(
                "Consumption Tank Name", options=[f"Tank {i}" for i in range(1, 9)]
            ),
        }
    )

    st.session_state.special_events_df = edited_df

def display_speed_position_and_navigation():
    st.subheader("Speed, Position and Navigation")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.number_input("Time Since Last Report (hours)", min_value=0.0, step=0.1, key="time_since_last_report")
        st.selectbox("Clocks Advanced/Retarded", ["", "Advanced", "Retarded"], key="clocks_change")
        st.number_input("Clocks Changed By (minutes)", min_value=0, step=1, key="clocks_change_minutes")
        st.time_input("SBE Date Time (Local)", value=datetime.now().time(), key=f"local_time_{uuid.uuid4()}")
    with col2:
        #st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, value=0.00, key=f"distance_observed_{uuid.uuid4()}")
        st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1, value=0.00, key=f"distance_togo_{uuid.uuid4()}")
        st.number_input("Distance Through Water (nm)", min_value=0.0, step=0.1, key=f"distance_through_water_{uuid.uuid4()}")
       # st.number_input("Engine Distance (nm)", min_value=0.0, step=0.1, key=f"engine_distance_{uuid.uuid4()}")
    with col3:
        st.number_input("Latitude", min_value=-90, max_value=90, step=1, key=f"lat_degree_{uuid.uuid4()}")
        st.selectbox("Latitude N/S", ["N", "S"], key=f"lat_ns_{uuid.uuid4()}")
        st.number_input("Longitude", min_value=-180, max_value=180, step=1, key=f"lon_degree_{uuid.uuid4()}")
        st.selectbox("Longitude E/W", ["E", "W"], key=f"lon_ew_{uuid.uuid4()}")
    with col4:
        st.number_input("Course (°)", min_value=0, max_value=359, step=1, key=f"course_{uuid.uuid4()}")
        st.number_input("Heading (°)", min_value=0, max_value=359, step=1, key=f"heading_{uuid.uuid4()}")
        #st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key=f"obs_speed_sog_{uuid.uuid4()}")
        #st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key=f"em_log_speed_{uuid.uuid4()}")
    with col5:
        #st.text_input("Ordered Speed", key=f"speed_order_{uuid.uuid4()}")
        #st.text_input("True Slip", key="true_slip")
        #st.text_input("Observed Slip", key="obs_slip")
        st.time_input(" SBE Date Time (UTC)", value=datetime.now().time(), key=f"local_time_{uuid.uuid4()}")

def display_custom_speed_position_and_navigation(noon_report_type):
    st.subheader("Speed, Position and Navigation")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.date_input("SBE Date Time (Local)", value=datetime.now(), key=f"local_date_{uuid.uuid4()}")
        st.number_input("Anchor Pos. Longitude", min_value=-180, max_value=180, step=1, key=f"lon_degree_{uuid.uuid4()}")
        st.number_input("Water Depth (m)", min_value=0, max_value=359, step=1, key=f"depth_{uuid.uuid4()}")
        
    with col2:
        st.date_input("SBE Date Time (UTC)", value=datetime.now(), key=f"utc_date_{uuid.uuid4()}")
        st.number_input("Anchor Pos. Latitude", min_value=-90, max_value=90, step=1, key=f"lat_degree_{uuid.uuid4()}")
        st.number_input("Heading (°)", min_value=0, max_value=359, step=1, key=f"heading_{uuid.uuid4()}")
       
                
    with col3:
        st.time_input("Anchor Aweigh (UTC)", value=datetime.now().time(), key=f"local_time_{uuid.uuid4()}")
        st.selectbox("Anchor Pos. Longitude E/W", ["E", "W"], key=f"lon_ew_{uuid.uuid4()}")
        
        
    with col4:
        st.time_input("Anchor Aweigh (LT)", value=datetime.now().time(), key=f"local_time_{uuid.uuid4()}")
        st.selectbox("Anchor Pos. Latitude N/S", ["N", "S"], key=f"lat_ns_{uuid.uuid4()}")
        st.text_input("Anchor Location", key="anchor_loc")
        
def display_weather_and_sea_conditions():
    st.subheader("Weather and Sea Conditions")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.number_input("True Wind Speed (kts)", min_value=0.0, step=0.1, key=f"true_wind_speed_{uuid.uuid4()}")
        st.selectbox("BF Scale", range(13), key=f"bf_scale_{uuid.uuid4()}")
    with col2:
        st.number_input("True Wind Direction (°)", min_value=0, max_value=359, step=1, key=f"true_wind_direction_{uuid.uuid4()}")
        st.number_input("Sea Water Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1, key=f"sea_water_temp_{uuid.uuid4()}")
    with col3:
        st.number_input("Significant Wave Height (m)", min_value=0.0, step=0.1, key=f"sig_wave_height_{uuid.uuid4()}")
        st.number_input("Wave Direction (°)", min_value=0, max_value=359, step=1, key=f"wave_direction_{uuid.uuid4()}")
        st.selectbox("Sea State (Douglas)", range(10), key=f"douglas_sea_state_{uuid.uuid4()}")
    with col4:
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key=f"sea_height_{uuid.uuid4()}")
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key=f"air_temp_{uuid.uuid4()}")
    with col5:
        st.number_input("Sea Direction (°)", min_value=0, max_value=359, step=1, key=f"sea_direction_{uuid.uuid4()}")
        st.number_input("Swell Direction (°)", min_value=0, max_value=359, step=1, key=f"swell_direction_{uuid.uuid4()}")
        st.number_input("Swell Height (m) (DSS)", min_value=0.0, step=0.1, key=f"swell_height_{uuid.uuid4()}")

def display_custom_weather_and_sea_conditions(noon_report_type):
    st.subheader("Weather and Sea Conditions")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.number_input("True Wind Speed (kts)", min_value=0.0, step=0.1, key=f"true_wind_speed_{uuid.uuid4()}")
        st.selectbox("BF Scale", range(13), key=f"bf_scale_{uuid.uuid4()}")
    with col2:
        st.number_input("True Wind Direction (°)", min_value=0, max_value=359, step=1, key=f"true_wind_direction_{uuid.uuid4()}")
        st.number_input("Sea Water Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1, key=f"sea_water_temp_{uuid.uuid4()}")
    with col3:
        st.number_input("Significant Wave Height (m)", min_value=0.0, step=0.1, key=f"sig_wave_height_{uuid.uuid4()}")
        st.number_input("Wave Direction (°)", min_value=0, max_value=359, step=1, key=f"wave_direction_{uuid.uuid4()}")
        st.selectbox("Sea State (Douglas)", range(10), key=f"douglas_sea_state_{uuid.uuid4()}")
    with col4:
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key=f"sea_height_{uuid.uuid4()}")
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key=f"air_temp_{uuid.uuid4()}")
    with col5:
        st.number_input("Sea Direction (°)", min_value=0, max_value=359, step=1, key=f"sea_direction_{uuid.uuid4()}")
        st.number_input("Swell Direction (°)", min_value=0, max_value=359, step=1, key=f"swell_direction_{uuid.uuid4()}")
        st.number_input("Swell Height (m) (DSS)", min_value=0.0, step=0.1, key=f"swell_height_{uuid.uuid4()}")

def display_cargo_and_stability():
    st.subheader("Cargo and Stability")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("FWD Draft (m)", min_value=0.0, step=0.01, key=f"fwd_draft_{uuid.uuid4()}")
        st.number_input("GM (m)", min_value=0.0, step=0.01, key=f"gm_{uuid.uuid4()}")
        st.number_input("LCG (m)", min_value=0.0, step=0.01, key=f"lcg_{uuid.uuid4()}")
    with col2:
        st.number_input("Displacement (MT)", min_value=0.0, step=0.1, key=f"displacement_{uuid.uuid4()}")
        st.number_input("Mid Draft (m)", min_value=0.0, step=0.01, key=f"mid_draft_{uuid.uuid4()}")
        st.number_input("Ballast Quantity (m³)", min_value=0.0, step=0.1, key=f"ballast_qty_{uuid.uuid4()}")
    with col3:
        st.number_input("Water Plane Co-efficient", min_value=0.0, step=0.01, key=f"water_plane_coefficient_{uuid.uuid4()}")
        st.number_input("AFT Draft (m)", min_value=0.0, step=0.01, key=f"aft_draft_{uuid.uuid4()}")
        st.number_input("Freeboard (m)", min_value=0.0, step=0.01, key=f"freeboard_{uuid.uuid4()}")
    with col4:
        st.number_input("Cb (Block Co-efficient)", min_value=0.0, step=0.01, key=f"cb_{uuid.uuid4()}")
        st.number_input("Cargo Weight (MT)", min_value=0.0, step=0.1, key=f"cargo_weight_{uuid.uuid4()}")
        st.number_input("Cargo Volume (m³)", min_value=0.0, step=0.1, key=f"cargo_volume_{uuid.uuid4()}")

def display_custom_cargo_and_stability(noon_report_type):
    st.subheader("Cargo and Stability")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("FWD Draft (m)", min_value=0.0, step=0.01, key=f"fwd_draft_{uuid.uuid4()}")
        st.number_input("GM (m)", min_value=0.0, step=0.01, key=f"gm_{uuid.uuid4()}")
        st.number_input("LCG (m)", min_value=0.0, step=0.01, key=f"lcg_{uuid.uuid4()}")
    with col2:
        st.number_input("Displacement (MT)", min_value=0.0, step=0.1, key=f"displacement_{uuid.uuid4()}")
        st.number_input("Mid Draft (m)", min_value=0.0, step=0.01, key=f"mid_draft_{uuid.uuid4()}")
        st.number_input("Ballast Quantity (m³)", min_value=0.0, step=0.1, key=f"ballast_qty_{uuid.uuid4()}")
    with col3:
        st.number_input("Water Plane Co-efficient", min_value=0.0, step=0.01, key=f"water_plane_coefficient_{uuid.uuid4()}")
        st.number_input("AFT Draft (m)", min_value=0.0, step=0.01, key=f"aft_draft_{uuid.uuid4()}")
        st.number_input("Freeboard (m)", min_value=0.0, step=0.01, key=f"freeboard_{uuid.uuid4()}")
    with col4:
        st.number_input("Cb (Block Co-efficient)", min_value=0.0, step=0.01, key=f"cb_{uuid.uuid4()}")
        st.number_input("Cargo Weight (MT)", min_value=0.0, step=0.1, key=f"cargo_weight_{uuid.uuid4()}")
        st.number_input("Cargo Volume (m³)", min_value=0.0, step=0.1, key=f"cargo_volume_{uuid.uuid4()}")

def display_fuel_consumption():
    if 'consumers' not in st.session_state:
        st.session_state.consumers = [
            'Main Engine', 'Aux Engine1', 'Aux Engine2', 'Aux Engine3',
            'Boiler 1',
            '    Boiler 1 - Cargo Heating',
            '    Boiler 1 - Discharge',
            'Boiler 2',
            '    Boiler 2 - Cargo Heating',
            '    Boiler 2 - Discharge',
            'IGG', 'Incinerator',
            'DPP1', 'DPP2', 'DPP3'
        ]
    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]
    if 'consumption_data' not in st.session_state:
        st.session_state.consumption_data = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.tanks)
    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {tank: np.random.uniform(20, 100) for tank in st.session_state.tanks}
    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {tank: np.random.uniform(0.05, 0.49) for tank in st.session_state.tanks}
    if 'previous_rob' not in st.session_state:
        st.session_state.previous_rob = pd.Series({tank: np.random.uniform(100, 1000) for tank in st.session_state.tanks})
    if 'bunkered_qty' not in st.session_state:
        st.session_state.bunkered_qty = pd.Series({tank: 0 for tank in st.session_state.tanks})
    if 'debunkered_qty' not in st.session_state:
        st.session_state.debunkered_qty = pd.Series({tank: 0 for tank in st.session_state.tanks})
    if 'bunkering_entries' not in st.session_state:
        st.session_state.bunkering_entries = []
    if 'debunkering_entries' not in st.session_state:
        st.session_state.debunkering_entries = []

    st.title('Fuel Consumption Tracker')

    col1, col2 = st.columns(2)
    with col1:
        bunkering_happened = st.checkbox("Bunkering Happened")
    with col2:
        debunkering_happened = st.checkbox("Debunkering Happened")

    if bunkering_happened:
        st.markdown("<h4 style='font-size: 18px;'>Bunkering Details</h4>", unsafe_allow_html=True)
        for i, entry in enumerate(st.session_state.bunkering_entries):
            st.markdown(f"<h5 style='font-size: 16px;'>Bunkering Entry {i+1}</h5>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                entry['bdn_number'] = st.text_input("Bunker Delivery Note Number", key=f"bdn_number_{i}")
                entry['delivery_date'] = st.date_input("Bunker Delivery Date", key=f"delivery_date_{i}")
                entry['delivery_time'] = st.time_input("Bunker Delivery Time", key=f"delivery_time_{i}")
            with col2:
                entry['imo_number'] = st.text_input("IMO number", key=f"imo_number_{i}")
                entry['fuel_type'] = st.text_input("Fuel Type", key=f"fuel_type_{i}")
                entry['mass'] = st.number_input("Mass (mt)", min_value=0.0, step=0.1, key=f"mass_{i}")
            with col3:
                entry['lower_heating_value'] = st.number_input("Lower heating value (MJ/kg)", min_value=0.0, step=0.1, key=f"lower_heating_value_{i}")
                entry['eu_ghg_intensity'] = st.number_input("EU GHG emission intensity (gCO2eq/MJ)", min_value=0.0, step=0.1, key=f"eu_ghg_intensity_{i}")
                entry['imo_ghg_intensity'] = st.number_input("IMO GHG emission intensity (gCO2eq/MJ)", min_value=0.0, step=0.1, key=f"imo_ghg_intensity_{i}")
                entry['lcv_eu'] = st.number_input("Lower Calorific Value (EU) (MJ/kg)", min_value=0.0, step=0.1, key=f"lcv_eu_{i}")
                entry['sustainability'] = st.text_input("Sustainability", key=f"sustainability_{i}")
        if st.button("➕ Add Bunkering Entry"):
            st.session_state.bunkering_entries.append({})
            st.experimental_rerun()

    if debunkering_happened:
        st.markdown("<h4 style='font-size: 18px;'>Debunkering Details</h4>", unsafe_allow_html=True)
        for i, entry in enumerate(st.session_state.debunkering_entries):
            st.markdown(f"<h5 style='font-size: 16px;'>Debunkering Entry {i+1}</h5>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                entry['date'] = st.date_input("Date of Debunkering", key=f"debunker_date_{i}")
                entry['quantity'] = st.number_input("Quantity Debunkered (mt)", min_value=0.0, step=0.1, key=f"debunker_qty_{i}")
            with col2:
                entry['bdn_number'] = st.text_input("BDN Number of Debunkered Oil", key=f"debunker_bdn_{i}")
                entry['receipt_file'] = st.file_uploader("Upload Receipt", type=['pdf', 'jpg', 'png'], key=f"receipt_file_{i}")
        if st.button("➕ Add Debunkering Entry"):
            st.session_state.debunkering_entries.append({})
            st.experimental_rerun()

    def format_column_header(tank):
        return f"{tank}\nVisc: {st.session_state.viscosity[tank]:.1f}\nSulfur: {st.session_state.sulfur[tank]:.2f}%"

    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers
        if bunkering_happened:
            index += ['Bunkered Qty']
        if debunkering_happened:
            index += ['Debunkered Qty']
        index += ['Current ROB']
        df = pd.DataFrame(index=index, columns=st.session_state.tanks)
        df.loc['Previous ROB'] = st.session_state.previous_rob
        df.loc[st.session_state.consumers] = st.session_state.consumption_data
        if bunkering_happened:
            total_bunkered = sum(entry.get('total_qty', 0) for entry in st.session_state.bunkering_entries)
            df.loc['Bunkered Qty'] = [total_bunkered] + [0] * (len(st.session_state.tanks) - 1)
        if debunkering_happened:
            total_debunkered = sum(entry.get('quantity', 0) for entry in st.session_state.debunkering_entries)
            df.loc['Debunkered Qty'] = [total_debunkered] + [0] * (len(st.session_state.tanks) - 1)
        total_consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - total_consumption
        if bunkering_happened:
            df.loc['Current ROB'] += df.loc['Bunkered Qty']
        if debunkering_happened:
            df.loc['Current ROB'] -= df.loc['Debunkered Qty']
        df.columns = [format_column_header(tank) for tank in st.session_state.tanks]
        return df

    df = create_editable_dataframe()

    st.write("Fuel Consumption Data:")
    custom_css = """
    <style>
        .dataframe td:first-child {
            font-weight: bold;
        }
        .dataframe td.italic-row {
            font-style: italic;
        }
        .dataframe td.boiler-subsection {
            padding-left: 30px !important;
            font-style: italic;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    df_html = df.to_html(classes='dataframe', escape=False)
    df_html = df_html.replace('<th>', '<th style="text-align: center;">')
    italic_rows = ['Boiler 1', 'Boiler 2', 'DPP1', 'DPP2', 'DPP3']
    for consumer in st.session_state.consumers:
        if consumer.startswith('    '):
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="boiler-subsection">{consumer.strip()}</td>')
        elif consumer in italic_rows:
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="italic-row">{consumer}</td>')
    st.markdown(df_html, unsafe_allow_html=True)

    def display_additional_table():
        st.write("Additional Consumption Data:")
        additional_data = pd.DataFrame({
            'Work': [0, 0, 0, 0],
            'SFOC': [0, 0, 0, ''],
            'Tank Name': ['', '', '', '']
        }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
        custom_css = """
        <style>
            .additional-table th {
                text-align: center !important;
            }
            .additional-table td {
                text-align: center !important;
            }
            .grey-out {
                background-color: #f0f0f0 !important;
                color: #888 !important;
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
        table_html = additional_data.to_html(classes='additional-table', escape=False)
        table_html = table_html.replace('<td></td>', '<td>-</td>')
        table_html = table_html.replace('<td>Shore-Side Electricity</td><td>0</td><td></td><td></td>', 
                                        '<td>Shore-Side Electricity</td><td>0</td><td class="grey-out">-</td><td class="grey-out">-</td>')
        st.markdown(table_html, unsafe_allow_html=True)

    display_additional_table()

    def edit_tank_properties():
        st.write("Edit tank properties:")
        tank_props = pd.DataFrame({
            'Viscosity': st.session_state.viscosity,
            'Sulfur (%)': st.session_state.sulfur
        })
        edited_props = st.data_editor(
            tank_props,
            use_container_width=True,
            column_config={
                'Viscosity': st.column_config.NumberColumn(
                    'Viscosity', min_value=20.0, max_value=100.0, step=0.1, format="%.1f"
                ),
                'Sulfur (%)': st.column_config.NumberColumn(
                    'Sulfur (%)', min_value=0.05, max_value=0.49, step=0.01, format="%.2f"
                )
            }
        )
        st.session_state.viscosity = edited_props['Viscosity'].to_dict()
        st.session_state.sulfur = edited_props['Sulfur (%)'].to_dict()

    if st.checkbox("Edit Tank Properties"):
        edit_tank_properties()


def display_custom_fuel_consumption(noon_report_type):
    if 'consumers' not in st.session_state:
        st.session_state.consumers = [
            'Main Engine', 'Aux Engine1', 'Aux Engine2', 'Aux Engine3',
            'Boiler 1',
            '    Boiler 1 - Cargo Heating',
            '    Boiler 1 - Discharge',
            'Boiler 2',
            '    Boiler 2 - Cargo Heating',
            '    Boiler 2 - Discharge',
            'IGG', 'Incinerator',
            'DPP1', 'DPP2', 'DPP3'
        ]
    if 'tanks' not in st.session_state:
        st.session_state.tanks = [f'Tank {i}' for i in range(1, 9)]
    if 'consumption_data' not in st.session_state:
        st.session_state.consumption_data = pd.DataFrame(0, index=st.session_state.consumers, columns=st.session_state.tanks)
    if 'viscosity' not in st.session_state:
        st.session_state.viscosity = {tank: np.random.uniform(20, 100) for tank in st.session_state.tanks}
    if 'sulfur' not in st.session_state:
        st.session_state.sulfur = {tank: np.random.uniform(0.05, 0.49) for tank in st.session_state.tanks}
    if 'previous_rob' not in st.session_state:
        st.session_state.previous_rob = pd.Series({tank: np.random.uniform(100, 1000) for tank in st.session_state.tanks})
    if 'bunkered_qty' not in st.session_state:
        st.session_state.bunkered_qty = pd.Series({tank: 0 for tank in st.session_state.tanks})
    if 'debunkered_qty' not in st.session_state:
        st.session_state.debunkered_qty = pd.Series({tank: 0 for tank in st.session_state.tanks})
    if 'bunkering_entries' not in st.session_state:
        st.session_state.bunkering_entries = []
    if 'debunkering_entries' not in st.session_state:
        st.session_state.debunkering_entries = []

    st.title('Fuel Consumption Tracker')

    col1, col2 = st.columns(2)
    with col1:
        bunkering_happened = st.checkbox("Bunkering Happened")
    with col2:
        debunkering_happened = st.checkbox("Debunkering Happened")

    if bunkering_happened:
        st.markdown("<h4 style='font-size: 18px;'>Bunkering Details</h4>", unsafe_allow_html=True)
        for i, entry in enumerate(st.session_state.bunkering_entries):
            st.markdown(f"<h5 style='font-size: 16px;'>Bunkering Entry {i+1}</h5>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                entry['bdn_number'] = st.text_input("Bunker Delivery Note Number", key=f"bdn_number_{i}")
                entry['delivery_date'] = st.date_input("Bunker Delivery Date", key=f"delivery_date_{i}")
                entry['delivery_time'] = st.time_input("Bunker Delivery Time", key=f"delivery_time_{i}")
            with col2:
                entry['imo_number'] = st.text_input("IMO number", key=f"imo_number_{i}")
                entry['fuel_type'] = st.text_input("Fuel Type", key=f"fuel_type_{i}")
                entry['mass'] = st.number_input("Mass (mt)", min_value=0.0, step=0.1, key=f"mass_{i}")
            with col3:
                entry['lower_heating_value'] = st.number_input("Lower heating value (MJ/kg)", min_value=0.0, step=0.1, key=f"lower_heating_value_{i}")
                entry['eu_ghg_intensity'] = st.number_input("EU GHG emission intensity (gCO2eq/MJ)", min_value=0.0, step=0.1, key=f"eu_ghg_intensity_{i}")
                entry['imo_ghg_intensity'] = st.number_input("IMO GHG emission intensity (gCO2eq/MJ)", min_value=0.0, step=0.1, key=f"imo_ghg_intensity_{i}")
                entry['lcv_eu'] = st.number_input("Lower Calorific Value (EU) (MJ/kg)", min_value=0.0, step=0.1, key=f"lcv_eu_{i}")
                entry['sustainability'] = st.text_input("Sustainability", key=f"sustainability_{i}")
        if st.button("➕ Add Bunkering Entry"):
            st.session_state.bunkering_entries.append({})
            st.experimental_rerun()

    if debunkering_happened:
        st.markdown("<h4 style='font-size: 18px;'>Debunkering Details</h4>", unsafe_allow_html=True)
        for i, entry in enumerate(st.session_state.debunkering_entries):
            st.markdown(f"<h5 style='font-size: 16px;'>Debunkering Entry {i+1}</h5>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                entry['date'] = st.date_input("Date of Debunkering", key=f"debunker_date_{i}")
                entry['quantity'] = st.number_input("Quantity Debunkered (mt)", min_value=0.0, step=0.1, key=f"debunker_qty_{i}")
            with col2:
                entry['bdn_number'] = st.text_input("BDN Number of Debunkered Oil", key=f"debunker_bdn_{i}")
                entry['receipt_file'] = st.file_uploader("Upload Receipt", type=['pdf', 'jpg', 'png'], key=f"receipt_file_{i}")
        if st.button("➕ Add Debunkering Entry"):
            st.session_state.debunkering_entries.append({})
            st.experimental_rerun()

    def format_column_header(tank):
        return f"{tank}\nVisc: {st.session_state.viscosity[tank]:.1f}\nSulfur: {st.session_state.sulfur[tank]:.2f}%"

    def create_editable_dataframe():
        index = ['Previous ROB'] + st.session_state.consumers
        if bunkering_happened:
            index += ['Bunkered Qty']
        if debunkering_happened:
            index += ['Debunkered Qty']
        index += ['Current ROB']
        df = pd.DataFrame(index=index, columns=st.session_state.tanks)
        df.loc['Previous ROB'] = st.session_state.previous_rob
        df.loc[st.session_state.consumers] = st.session_state.consumption_data
        if bunkering_happened:
            total_bunkered = sum(entry.get('total_qty', 0) for entry in st.session_state.bunkering_entries)
            df.loc['Bunkered Qty'] = [total_bunkered] + [0] * (len(st.session_state.tanks) - 1)
        if debunkering_happened:
            total_debunkered = sum(entry.get('quantity', 0) for entry in st.session_state.debunkering_entries)
            df.loc['Debunkered Qty'] = [total_debunkered] + [0] * (len(st.session_state.tanks) - 1)
        total_consumption = df.loc[st.session_state.consumers].sum()
        df.loc['Current ROB'] = df.loc['Previous ROB'] - total_consumption
        if bunkering_happened:
            df.loc['Current ROB'] += df.loc['Bunkered Qty']
        if debunkering_happened:
            df.loc['Current ROB'] -= df.loc['Debunkered Qty']
        df.columns = [format_column_header(tank) for tank in st.session_state.tanks]
        return df

    df = create_editable_dataframe()

    st.write("Fuel Consumption Data:")
    custom_css = """
    <style>
        .dataframe td:first-child {
            font-weight: bold;
        }
        .dataframe td.italic-row {
            font-style: italic;
        }
        .dataframe td.boiler-subsection {
            padding-left: 30px !important;
            font-style: italic;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    df_html = df.to_html(classes='dataframe', escape=False)
    df_html = df_html.replace('<th>', '<th style="text-align: center;">')
    italic_rows = ['Boiler 1', 'Boiler 2', 'DPP1', 'DPP2', 'DPP3']
    for consumer in st.session_state.consumers:
        if consumer.startswith('    '):
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="boiler-subsection">{consumer.strip()}</td>')
        elif consumer in italic_rows:
            df_html = df_html.replace(f'<td>{consumer}</td>', f'<td class="italic-row">{consumer}</td>')
    st.markdown(df_html, unsafe_allow_html=True)

    def display_additional_table():
        st.write("Additional Consumption Data:")
        additional_data = pd.DataFrame({
            'Work': [0, 0, 0, 0],
            'SFOC': [0, 0, 0, ''],
            'Tank Name': ['', '', '', '']
        }, index=['Reefer container', 'Cargo cooling', 'Heating/Discharge pump', 'Shore-Side Electricity'])
        custom_css = """
        <style>
            .additional-table th {
                text-align: center !important;
            }
            .additional-table td {
                text-align: center !important;
            }
            .grey-out {
                background-color: #f0f0f0 !important;
                color: #888 !important;
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
        table_html = additional_data.to_html(classes='additional-table', escape=False)
        table_html = table_html.replace('<td></td>', '<td>-</td>')
        table_html = table_html.replace('<td>Shore-Side Electricity</td><td>0</td><td></td><td></td>', 
                                        '<td>Shore-Side Electricity</td><td>0</td><td class="grey-out">-</td><td class="grey-out">-</td>')
        st.markdown(table_html, unsafe_allow_html=True)

    display_additional_table()

    def edit_tank_properties():
        st.write("Edit tank properties:")
        tank_props = pd.DataFrame({
            'Viscosity': st.session_state.viscosity,
            'Sulfur (%)': st.session_state.sulfur
        })
        edited_props = st.data_editor(
            tank_props,
            use_container_width=True,
            column_config={
                'Viscosity': st.column_config.NumberColumn(
                    'Viscosity', min_value=20.0, max_value=100.0, step=0.1, format="%.1f"
                ),
                'Sulfur (%)': st.column_config.NumberColumn(
                    'Sulfur (%)', min_value=0.05, max_value=0.49, step=0.01, format="%.2f"
                )
            }
        )
        st.session_state.viscosity = edited_props['Viscosity'].to_dict()
        st.session_state.sulfur = edited_props['Sulfur (%)'].to_dict()

    if st.checkbox("Edit Tank Properties"):
        edit_tank_properties()

def display_machinery():
    st.subheader("Machinery")

    st.subheader("Main Engine")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("ME RPM", min_value=0.0, step=0.1, key=f"me_rpm_{uuid.uuid4()}")
        st.number_input("ME TC1 RPM", min_value=0.0, step=0.1, key=f"me_tc1_rpm_{uuid.uuid4()}")
        st.number_input("ME TC2 RPM", min_value=0.0, step=0.1, key=f"me_tc2_rpm_{uuid.uuid4()}")
    with col2:
        st.number_input("Exhaust Max. Temp.(C)", min_value=0.0, step=0.1, key=f"exhaust_max_temp_{uuid.uuid4()}")
        st.number_input("Exhaust Min. Temp.(C)", min_value=0.0, step=0.1, key=f"exhaust_min_temp_{uuid.uuid4()}")
    with col3:
        st.number_input("M/E rev counter", min_value=0, step=1, key=f"me_rev_counter_{uuid.uuid4()}")
        st.number_input("Scavenge pressure(BAR)", min_value=0.0, step=0.01, key=f"scavenge_pressure_{uuid.uuid4()}")
        st.number_input("MCR", min_value=0.0, max_value=100.0, step=0.1, key=f"mcr_{uuid.uuid4()}")
    with col4:
        st.number_input("kWhr", min_value=0.0, step=0.1, key=f"avg_kw_{uuid.uuid4()}")
        st.number_input("Slip", min_value=0.0, max_value=100.0, step=0.1, key=f"slip_{uuid.uuid4()}")
        st.number_input("SFOC", min_value=0.0, step=0.1, key=f"sfoc_{uuid.uuid4()}")

    st.subheader("Auxiliary Engines")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Avg A/E power 1", min_value=0.0, step=0.1, key=f"avg_ae_power_1_{uuid.uuid4()}")
    with col2:
        st.number_input("Avg A/E power 2", min_value=0.0, step=0.1, key=f"avg_ae_power_2_{uuid.uuid4()}")
    with col3:
        st.number_input("Avg A/E power 3", min_value=0.0, step=0.1, key=f"avg_ae_power_3_{uuid.uuid4()}")
    with col4:
        st.number_input("Avg A/E power 4", min_value=0.0, step=0.1, key=f"avg_ae_power_4_{uuid.uuid4()}")

    st.subheader("Running Hours")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Main engine", min_value=0.0, step=0.1, key=f"main_engine_hours_{uuid.uuid4()}")
        st.number_input("AE-1", min_value=0.0, step=0.1, key=f"ae_1_hours_{uuid.uuid4()}")
    with col2:
        st.number_input("A/E 2", min_value=0.0, step=0.1, key=f"ae_2_hours_{uuid.uuid4()}")
        st.number_input("A/E 3", min_value=0.0, step=0.1, key=f"ae_3_hours_{uuid.uuid4()}")
    with col3:
        st.number_input("A/E 4", min_value=0.0, step=0.1, key=f"ae_4_hours_{uuid.uuid4()}")
        st.number_input("Boilers", min_value=0.0, step=0.1, key=f"boilers_hours_{uuid.uuid4()}")
    with col4:
        st.number_input("Scrubbers", min_value=0.0, step=0.1, key=f"scrubbers_hours_{uuid.uuid4()}")
        st.number_input("Shaft gen", min_value=0.0, step=0.1, key=f"shaft_gen_hours_{uuid.uuid4()}")

    st.subheader("Boilers")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Boiler 1 running hrs", min_value=0.0, step=0.1, key=f"boiler_1_hours_{uuid.uuid4()}")
    with col2:
        st.number_input("Boiler 2 running hrs", min_value=0.0, step=0.1, key=f"boiler_2_hours_{uuid.uuid4()}")

def display_custom_machinery(noon_report_type):
    st.subheader("Machinery")

    st.subheader("Main Engine")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("M/E rev counter", min_value=0, step=1, key=f"me_rev_counter_{uuid.uuid4()}")

    st.subheader("Auxiliary Engines")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Avg A/E power 1", min_value=0.0, step=0.1, key=f"avg_ae_power_1_{uuid.uuid4()}")
    with col2:
        st.number_input("Avg A/E power 2", min_value=0.0, step=0.1, key=f"avg_ae_power_2_{uuid.uuid4()}")
    with col3:
        st.number_input("Avg A/E power 3", min_value=0.0, step=0.1, key=f"avg_ae_power_3_{uuid.uuid4()}")
    with col4:
        st.number_input("Avg A/E power 4", min_value=0.0, step=0.1, key=f"avg_ae_power_4_{uuid.uuid4()}")

    st.subheader("Running Hours")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Main engine", min_value=0.0, step=0.1, key=f"main_engine_hours_{uuid.uuid4()}")
        st.number_input("AE-1", min_value=0.0, step=0.1, key=f"ae_1_hours_{uuid.uuid4()}")
    with col2:
        st.number_input("A/E 2", min_value=0.0, step=0.1, key=f"ae_2_hours_{uuid.uuid4()}")
        st.number_input("A/E 3", min_value=0.0, step=0.1, key=f"ae_3_hours_{uuid.uuid4()}")
    with col3:
        st.number_input("A/E 4", min_value=0.0, step=0.1, key=f"ae_4_hours_{uuid.uuid4()}")
        st.number_input("Boilers", min_value=0.0, step=0.1, key=f"boilers_hours_{uuid.uuid4()}")
    with col4:
        st.number_input("Scrubbers", min_value=0.0, step=0.1, key=f"scrubbers_hours_{uuid.uuid4()}")
        st.number_input("Shaft gen", min_value=0.0, step=0.1, key=f"shaft_gen_hours_{uuid.uuid4()}")

    st.subheader("Boilers")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Boiler 1 running hrs", min_value=0.0, step=0.1, key=f"boiler_1_hours_{uuid.uuid4()}")
    with col2:
        st.number_input("Boiler 2 running hrs", min_value=0.0, step=0.1, key=f"boiler_2_hours_{uuid.uuid4()}")

def display_environmental_compliance():
    st.subheader("Environmental Compliance")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1, key=f"sludge_rob_{uuid.uuid4()}")
        st.number_input("Sludge Burnt in Incinerator (MT)", min_value=0.0, step=0.1, key=f"sludge_burnt_{uuid.uuid4()}")
    with col2:
        st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1, key=f"sludge_landed_{uuid.uuid4()}")
        st.number_input("Bilge Water Quantity (m³)", min_value=0.0, step=0.1, key=f"bilge_water_qty_{uuid.uuid4()}")
    with col3:
        st.number_input("Bilge Water Pumped Out through 15ppm Equipment (m³)", min_value=0.0, step=0.1, key=f"bilge_pumped_out_{uuid.uuid4()}")
        st.number_input("Bilge Water Landed Ashore (m³)", min_value=0.0, step=0.1, key=f"bilge_landed_{uuid.uuid4()}")
    with col4:
        st.number_input("Food waste Disposed (m³)", min_value=0.0, step=0.1, key=f"food_waste_{uuid.uuid4()}")
    with col5:
        st.number_input("Garbage landed (m³)", min_value=0.0, step=0.1, key=f"garbage_waste_{uuid.uuid4()}")

def display_custom_environmental_compliance(noon_report_type):
    st.subheader("Environmental Compliance")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.number_input("Sludge ROB (MT)", min_value=0.0, step=0.1, key=f"sludge_rob_{uuid.uuid4()}")
    with col2:
        st.number_input("Sludge Landed Ashore (MT)", min_value=0.0, step=0.1, key=f"sludge_landed_{uuid.uuid4()}")
        st.number_input("Bilge Water Quantity (m³)", min_value=0.0, step=0.1, key=f"bilge_water_qty_{uuid.uuid4()}")
    with col3:
        st.number_input("Food waste Landed (m³)", min_value=0.0, step=0.1, key=f"food_wastel_{uuid.uuid4()}")
        st.number_input("Garbage landed (m³)", min_value=0.0, step=0.1, key=f"garbage_waste_{uuid.uuid4()}")
    with col4:
        st.number_input("Bilge Water Landed Ashore (m³)", min_value=0.0, step=0.1, key=f"bilge_landed_{uuid.uuid4()}")

def display_miscellaneous_consumables():
    st.subheader("Miscellaneous Consumables")
    st.markdown("Fresh Water")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Fresh Water Bunkered (m³)", min_value=0.0, step=0.1, key=f"fw_bunkered_{uuid.uuid4()}")
        st.number_input("Fresh Water Consumption - Drinking (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_drinking_{uuid.uuid4()}")
    with col2:
        st.number_input("Fresh Water Consumption - Technical (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_technical_{uuid.uuid4()}")
        st.number_input("Fresh Water Consumption - Washing (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_washing_{uuid.uuid4()}")
    with col3:
        st.number_input("Fresh Water Produced (m³)", min_value=0.0, step=0.1, key=f"fw_produced_{uuid.uuid4()}")
        st.number_input("Fresh Water ROB (m³)", min_value=0.0, step=0.1, key=f"fw_rob_{uuid.uuid4()}")

    st.markdown("Lubricating Oil")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("ME Cylinder Oil High BN ROB (liters)", min_value=0, step=1, key=f"me_cyl_oil_high_bn_rob_{uuid.uuid4()}")
        st.number_input("ME Cylinder Oil Low BN ROB (liters)", min_value=0, step=1, key=f"me_cyl_oil_low_bn_rob_{uuid.uuid4()}")
    with col2:
        st.number_input("ME System Oil ROB (liters)", min_value=0, step=1, key=f"me_system_oil_rob_{uuid.uuid4()}")
        st.number_input("AE System Oil ROB (liters)", min_value=0, step=1, key=f"ae_system_oil_rob_{uuid.uuid4()}")
    with col3:
        st.number_input("ME Cylinder Oil Consumption (liters)", min_value=0, step=1, key=f"me_cyl_oil_consumption_{uuid.uuid4()}")
        st.number_input("ME Cylinder Oil Feed Rate (g/kWh)", min_value=0.0, step=0.1, key=f"me_cyl_oil_feed_rate_{uuid.uuid4()}")
    with col4:
        st.number_input("ME System Oil Consumption (liters)", min_value=0, step=1, key=f"me_system_oil_consumption_{uuid.uuid4()}")
        st.number_input("AE System Oil Consumption (liters)", min_value=0, step=1, key=f"ae_system_oil_consumption_{uuid.uuid4()}")

def display_custom_miscellaneous_consumables(noon_report_type):
    st.subheader("Miscellaneous Consumables")
    st.markdown("Fresh Water")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Fresh Water Bunkered (m³)", min_value=0.0, step=0.1, key=f"fw_bunkered_{uuid.uuid4()}")
        st.number_input("Fresh Water Consumption - Drinking (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_drinking_{uuid.uuid4()}")
    with col2:
        st.number_input("Fresh Water Consumption - Technical (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_technical_{uuid.uuid4()}")
        st.number_input("Fresh Water Consumption - Washing (m³)", min_value=0.0, step=0.1, key=f"fw_consumption_washing_{uuid.uuid4()}")
    with col3:
        st.number_input("Fresh Water Produced (m³)", min_value=0.0, step=0.1, key=f"fw_produced_{uuid.uuid4()}")
        st.number_input("Fresh Water ROB (m³)", min_value=0.0, step=0.1, key=f"fw_rob_{uuid.uuid4()}")

    st.markdown("Lubricating Oil")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("ME Cylinder Oil High BN ROB (liters)", min_value=0, step=1, key=f"me_cyl_oil_high_bn_rob_{uuid.uuid4()}")
        st.number_input("ME Cylinder Oil Low BN ROB (liters)", min_value=0, step=1, key=f"me_cyl_oil_low_bn_rob_{uuid.uuid4()}")
    with col2:
        st.number_input("ME System Oil ROB (liters)", min_value=0, step=1, key=f"me_system_oil_rob_{uuid.uuid4()}")
        st.number_input("AE System Oil ROB (liters)", min_value=0, step=1, key=f"ae_system_oil_rob_{uuid.uuid4()}")
    with col3:
        st.number_input("ME Cylinder Oil Consumption (liters)", min_value=0, step=1, key=f"me_cyl_oil_consumption_{uuid.uuid4()}")
        st.number_input("ME Cylinder Oil Feed Rate (g/kWh)", min_value=0.0, step=0.1, key=f"me_cyl_oil_feed_rate_{uuid.uuid4()}")
    with col4:
        st.number_input("ME System Oil Consumption (liters)", min_value=0, step=1, key=f"me_system_oil_consumption_{uuid.uuid4()}")
        st.number_input("AE System Oil Consumption (liters)", min_value=0, step=1, key=f"ae_system_oil_consumption_{uuid.uuid4()}")

if __name__ == "__main__":
    main()