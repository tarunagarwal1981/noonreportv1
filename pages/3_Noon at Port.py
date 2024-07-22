import streamlit as st
import pandas as pd
from datetime import datetime, time

# Initialize session state
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Function to update progress
def update_progress():
    total_fields = 100  # Estimate of total fields
    filled_fields = sum(1 for value in st.session_state.form_data.values() if value)
    st.session_state.progress = min(filled_fields / total_fields, 1.0)

# Function to save form data
def save_form_data():
    st.session_state.form_data.update({k: v for k, v in st.session_state.items() if not k.startswith('_')})
    with open('form_data.json', 'w') as f:
        json.dump(st.session_state.form_data, f)
    st.success("Form data saved successfully!")

# Function to load form data
def load_form_data():
    try:
        with open('form_data.json', 'r') as f:
            st.session_state.form_data = json.load(f)
        st.success("Form data loaded successfully!")
    except FileNotFoundError:
        st.warning("No saved form data found.")

# Main app
def main():
    st.set_page_config(layout="wide", page_title="Maritime Report")

    st.title("Noon at Port Report")

    # Quick Fill and Save buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Quick Fill from Previous Report"):
            load_form_data()
    with col2:
        if st.button("Save Current Report"):
            save_form_data()
    with col3:
        if st.button("Review Summary"):
            st.session_state.show_summary = True

    # Search function
    search_term = st.sidebar.text_input("Search fields")

    tabs = st.tabs(["General Information", "Speed and Consumption", "Wind and Weather", "Drifting", "Engine"])

    with tabs[0]:
        general_info_tab(search_term)

    with tabs[1]:
        speed_consumption_tab(search_term)

    with tabs[2]:
        wind_weather_tab(search_term)

    with tabs[3]:
        drifting_tab(search_term)

    with tabs[4]:
        engine_tab(search_term)

    if st.button("Submit Report", type="primary"):
        save_report()
        st.success("Report submitted and saved successfully!")

    # Update progress
    update_progress()

    # Display summary if requested
    if st.session_state.get('show_summary', False):
        display_summary()
        if st.button("Close Summary"):
            st.session_state.show_summary = False

def general_info_tab(search_term):
    st.header("General Information")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Vessel Name", key="vessel_name", help="Enter the name of the vessel")
        st.text_input("Voyage No", key="voyage_no", help="Enter the voyage number")
        st.text_input("Cargo No", key="cargo_no", help="Enter the cargo number")
        st.selectbox("Vessel's Status", ["At Sea", "In Port"], key="vessel_status", help="Select the current status of the vessel")
        st.text_input("Current Port", key="current_port", help="Enter the current port if in port")
        st.text_input("Last Port", key="last_port", help="Enter the last port visited")
        st.text_input("Berth / Location", key="berth_location", help="Enter the specific berth or location")
    with col2:
        st.date_input("Report Date (LT)", datetime.now().date(), key="report_date_lt", help="Enter the local date of the report")
        st.time_input("Report Time (LT)", datetime.now().time(), key="report_time_lt", help="Enter the local time of the report")
        st.date_input("Report Date (UTC)", datetime.now().date(), key="report_date_utc", help="Enter the UTC date of the report")
        st.time_input("Report Time (UTC)", datetime.now().time(), key="report_time_utc", help="Enter the UTC time of the report")
        st.text_input("IDL Crossing", key="idl_crossing", help="Enter International Date Line crossing information if applicable")
        st.selectbox("IDL Direction", ["--Select--", "East", "West"], key="idl_direction", help="Select the direction of IDL crossing")
        st.checkbox("Off Port Limits", key="off_port_limits", help="Check if the vessel is at off port limits")
    with col3:
        st.text_input("Next Port", key="next_port", help="Enter the next port of call")
        st.date_input("ETA Date", datetime.now().date(), key="eta_date", help="Enter the estimated date of arrival at the next port")
        st.time_input("ETA Time", datetime.now().time(), key="eta_time", help="Enter the estimated time of arrival at the next port")
        st.number_input("Speed required to achieve Scheduled ETA (kts)", min_value=0.0, step=0.1, key="scheduled_eta_speed", help="Enter the required speed to meet the scheduled ETA")
        st.date_input("ETB", datetime.now().date(), key="etb", help="Enter the Estimated Time of Berthing")
        st.date_input("ETC/D", datetime.now().date(), key="etcd", help="Enter the Estimated Time of Completion/Departure")
        st.date_input("Best ETA PBG (LT)", datetime.now().date(), key="best_eta_pbg_lt_date", help="Enter the best estimated time of arrival at Pilot Boarding Ground (Local Time)")
        st.time_input("Best ETA PBG Time (LT)", datetime.now().time(), key="best_eta_pbg_lt_time", help="Enter the best estimated time of arrival at Pilot Boarding Ground (Local Time)")
        st.date_input("Best ETA PBG (UTC)", datetime.now().date(), key="best_eta_pbg_utc_date", help="Enter the best estimated time of arrival at Pilot Boarding Ground (UTC)")
        st.time_input("Best ETA PBG Time (UTC)", datetime.now().time(), key="best_eta_pbg_utc_time", help="Enter the best estimated time of arrival at Pilot Boarding Ground (UTC)")
        st.radio("Ballast/Laden", ["Ballast", "Laden"], key="ballast_laden", help="Select whether the vessel is in ballast or laden condition")

def speed_consumption_tab(search_term):
    st.header("Speed and Consumption")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1, key="full_speed_hrs", help="Enter the time spent at full speed")
        st.number_input("Full Speed (nm)", min_value=0.0, step=0.1, key="full_speed_nm", help="Enter the distance covered at full speed")
        st.number_input("Reduced Speed/Slow Steaming (hrs)", min_value=0.0, step=0.1, key="reduced_speed_hrs", help="Enter the time spent at reduced speed")
        st.number_input("Reduced Speed/Slow Steaming (nm)", min_value=0.0, step=0.1, key="reduced_speed_nm", help="Enter the distance covered at reduced speed")
        st.number_input("Stopped (hrs)", min_value=0.0, step=0.1, key="stopped_hrs", help="Enter the time spent stopped")
        st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1, key="distance_observed_nm", help="Enter the total distance observed")
    with col2:
        st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1, key="obs_speed_sog", help="Enter the observed speed over ground")
        st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1, key="em_log_speed", help="Enter the speed from the electromagnetic log")
        st.number_input("Voyage Average Speed (kts)", min_value=0.0, step=0.1, key="voyage_avg_speed", help="Enter the average speed for the voyage")
        st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1, key="distance_to_go", help="Enter the remaining distance to the destination")
        st.number_input("Distance since COSP (nm)", min_value=0.0, step=0.1, key="distance_since_cosp", help="Enter the distance traveled since Commencement of Sea Passage")
    with col3:
        st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.1, key="voyage_order_speed", help="Enter the ordered speed for the voyage")
        st.number_input("Voyage Order ME FO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_fo_cons", help="Enter the ordered Main Engine Fuel Oil consumption")
        st.number_input("Voyage Order ME DO Cons (mt)", min_value=0.0, step=0.1, key="voyage_order_me_do_cons", help="Enter the ordered Main Engine Diesel Oil consumption")
        st.number_input("Course (°)", min_value=0.0, max_value=360.0, step=1.0, key="course", help="Enter the current course in degrees")
        st.number_input("Draft F (m)", min_value=0.0, step=0.01, key="draft_f", help="Enter the forward draft in meters")
        st.number_input("Draft A (m)", min_value=0.0, step=0.01, key="draft_a", help="Enter the aft draft in meters")
        st.number_input("Displacement (mt)", min_value=0.0, step=0.1, key="displacement", help="Enter the current displacement in metric tons")

def wind_weather_tab(search_term):
    st.header("Wind and Weather")

    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Wind Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="wind_direction", help="Select the wind direction")
        st.number_input("Wind Force", min_value=0, max_value=12, key="wind_force", help="Enter the wind force on the Beaufort scale")
        st.number_input("Visibility (nm)", min_value=0.0, step=0.1, key="visibility", help="Enter the visibility in nautical miles")
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1, key="sea_height", help="Enter the sea height in meters")
        st.selectbox("Sea Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="sea_direction", help="Select the sea direction")
    with col2:
        st.number_input("Swell Height (m)", min_value=0.0, step=0.1, key="swell_height", help="Enter the swell height in meters")
        st.selectbox("Swell Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="swell_direction", help="Select the swell direction")
        st.number_input("Current Set (kts)", min_value=0.0, step=0.1, key="current_set", help="Enter the current set in knots")
        st.selectbox("Current Drift", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="current_drift", help="Select the current drift direction")
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="air_temp", help="Enter the air temperature in Celsius")
        st.checkbox("Icing on Deck?", key="icing_on_deck", help="Check if there is icing on the deck")

    st.subheader("Forecast next 24 Hrs")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Wind Direction (Forecast)", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="forecast_wind_direction", help="Select the forecasted wind direction")
        st.number_input("Wind Force (Forecast)", min_value=0, max_value=12, key="forecast_wind_force", help="Enter the forecasted wind force on the Beaufort scale")
        st.number_input("Sea Height (Forecast) (m)", min_value=0.0, step=0.1, key="forecast_sea_height", help="Enter the forecasted sea height in meters")
    with col2:
        st.selectbox("Sea Direction (Forecast)", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"], key="forecast_sea_direction", help="Select the forecasted sea direction")
        st.number_input("Swell Height (Forecast) (m)", min_value=0.0, step=0.1, key="forecast_swell_height", help="Enter the forecasted swell height in meters")

def drifting_tab(search_term):
    st.header("Drifting")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Drifting Start Latitude", key="drifting_start_latitude", help="Enter the latitude where drifting started")
        st.text_input("Drifting Start Longitude", key="drifting_start_longitude", help="Enter the longitude where drifting started")
        st.date_input("Drifting Start Date", datetime.now().date(), key="drifting_start_date", help="Enter the date when drifting started")
        st.time_input("Drifting Start Time", datetime.now().time(), key="drifting_start_time", help="Enter the time when drifting started")
        st.number_input("Drifting Distance (nm)", min_value=0.0, step=0.1, key="drifting_distance_nm", help="Enter the total distance drifted")
    with col2:
        st.text_input("Drifting End Latitude", key="drifting_end_latitude", help="Enter the latitude where drifting ended")
        st.text_input("Drifting End Longitude", key="drifting_end_longitude", help="Enter the longitude where drifting ended")
        st.date_input("Drifting End Date", datetime.now().date(), key="drifting_end_date", help="Enter the date when drifting ended")
        st.time_input("Drifting End Time", datetime.now().time(), key="drifting_end_time", help="Enter the time when drifting ended")
        st.number_input("Drifting Time (hrs)", min_value=0.0, step=0.1, key="drifting_time_hrs", help="Enter the total time spent drifting")

def engine_tab(search_term):
    st.header("Engine Information")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Engine Distance (nm)", min_value=0.0, step=0.1, key="engine_distance", help="Enter the engine distance in nautical miles")
        st.number_input("Slip (%)", min_value=0.0, step=0.1, key="slip", help="Enter the slip percentage")
        st.number_input("Avg Slip since COSP (%)", min_value=0.0, step=0.1, key="avg_slip_cosp", help="Enter the average slip since Commencement of Sea Passage")
    with col2:
        st.number_input("ER Temp (°C)", min_value=-50.0, max_value=100.0, step=0.1, key="er_temp", help="Enter the engine room temperature in Celsius")
        st.number_input("SW Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="sw_temp", help="Enter the sea water temperature in Celsius")
        st.number_input("SW Press (bar)", min_value=0.0, step=0.1, key="sw_press", help="Enter the sea water pressure in bar")

    st.subheader("Auxiliary Engines")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("A/E No.1 Generator Load (kw)", min_value=0, step=1, key="ae1_load", help="Enter the load of Auxiliary Engine No.1 Generator in kilowatts")
        st.number_input("A/E No.2 Generator Load (kw)", min_value=0, step=1, key="ae2_load", help="Enter the load of Auxiliary Engine No.2 Generator in kilowatts")
        st.number_input("A/E No.3 Generator Load (kw)", min_value=0, step=1, key="ae3_load", help="Enter the load of Auxiliary Engine No.3 Generator in kilowatts")
        st.number_input("A/E No.4 Generator Load (kw)", min_value=0, step=1, key="ae4_load", help="Enter the load of Auxiliary Engine No.4 Generator in kilowatts")
    with col2:
        st.number_input("A/E No.1 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae1_hours", help="Enter the hours of operation for Auxiliary Engine No.1 Generator")
        st.number_input("A/E No.2 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae2_hours", help="Enter the hours of operation for Auxiliary Engine No.2 Generator")
        st.number_input("A/E No.3 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae3_hours", help="Enter the hours of operation for Auxiliary Engine No.3 Generator")
        st.number_input("A/E No.4 Generator Hours of Operation (hrs)", min_value=0.0, step=0.1, key="ae4_hours", help="Enter the hours of operation for Auxiliary Engine No.4 Generator")
    st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.1, key="shaft_generator_power", help="Enter the power output of the Shaft Generator in kilowatts")

    st.subheader("Fresh Water")
    fresh_water_data = {
        "Fresh Water": ["Domestic Fresh Water", "Drinking Water", "Boiler Water", "Tank Cleaning Water"],
        "Previous ROB": [0.0] * 4,
        "Produced": [0.0] * 4,
        "ROB": [0.0] * 4,
        "Consumption": [0.0] * 4
    }
    fresh_water_df = pd.DataFrame(fresh_water_data)
    st.data_editor(fresh_water_df, key="fresh_water_editor", hide_index=True)
    st.number_input("Boiler Water Chlorides (ppm)", min_value=0.0, step=0.1, key="boiler_water_chlorides", help="Enter the boiler water chlorides in parts per million")

def input_field(label, field_type, search_term, **kwargs):
    if search_term.lower() in label.lower():
        st.markdown(f"**{label}**")
    if field_type == "text":
        return st.text_input(label, key=label, help=kwargs.get("help", ""), value=st.session_state.form_data.get(label, ""))
    elif field_type == "number":
        return st.number_input(label, key=label, help=kwargs.get("help", ""), value=st.session_state.form_data.get(label, 0.0), **kwargs)
    elif field_type == "date":
        return st.date_input(label, key=label, help=kwargs.get("help", ""), value=st.session_state.form_data.get(label, datetime.now().date()))
    elif field_type == "time":
        return st.time_input(label, key=label, help=kwargs.get("help", ""), value=st.session_state.form_data.get(label, datetime.now().time()))
    elif field_type == "selectbox":
        return st.selectbox(label, key=label, help=kwargs.get("help", ""), options=kwargs.get("options", []), index=kwargs.get("options", []).index(st.session_state.form_data.get(label, kwargs.get("options", [""])[0])))
    elif field_type == "radio":
        return st.radio(label, key=label, help=kwargs.get("help", ""), options=kwargs.get("options", []), index=kwargs.get("options", []).index(st.session_state.form_data.get(label, kwargs.get("options", [""])[0])))
    elif field_type == "checkbox":
        return st.checkbox(label, key=label, help=kwargs.get("help", ""), value=st.session_state.form_data.get(label, False))

def create_summary():
    summary = {}
    for key, value in st.session_state.items():
        if not key.startswith('_') and key != 'form_data':
            summary[key] = value
    return summary

def display_summary():
    st.title("Report Summary")
    summary = create_summary()
    for section, fields in summary.items():
        st.header(section)
        for field, value in fields.items():
            st.write(f"{field}: {value}")

def save_report():
    summary = create_summary()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"maritime_report_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(summary, f)
    st.success(f"Report saved as {filename}")

if __name__ == "__main__":
    main()
