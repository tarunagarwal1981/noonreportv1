import streamlit as st
from datetime import datetime

# Set up the page layout
st.set_page_config(layout="wide", page_title="Noon in Port Report")

def main():
    st.title("Noon in Port Report")

    # General Information Section
    st.header("General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Ship Mean Time", value="UTC")
        st.number_input("Offset", min_value=-12, max_value=12, step=1)
    with col2:
        st.date_input("Report Date (LT)", datetime.now())
        st.time_input("Report Time (LT)", datetime.now().time())
    with col3:
        st.date_input("Report Date (UTC)", datetime.now())
        st.time_input("Report Time (UTC)", datetime.now().time())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.checkbox("IDL Crossing")
        st.selectbox("IDL Direction", ["--Select--", "East", "West"])
        st.text_input("Voyage No")
    with col2:
        st.text_input("Cargo No")
        st.selectbox("Vessel's Status", ["At Sea", "In Port"])
        st.text_input("Current Port")
    with col3:
        st.text_input("Last Port")
        st.checkbox("Off Port Limits")
        st.text_input("Berth / Location")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Latitude")
    with col2:
        st.text_input("Longitude")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Next Port")
        st.date_input("ETA Date", datetime.now())
        st.time_input("ETA Time", datetime.now().time())
    with col2:
        st.text_input("Speed required to achieve Scheduled ETA (kts)")
        st.date_input("ETB", datetime.now())
        st.date_input("ETC/D", datetime.now())
        st.time_input("ETC/D Time", datetime.now().time())

    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Best ETA PBG (LT)", datetime.now())
        st.time_input("Best ETA PBG Time (LT)", datetime.now().time())
    with col2:
        st.date_input("Best ETA PBG (UTC)", datetime.now())
        st.time_input("Best ETA PBG Time (UTC)", datetime.now().time())

    st.radio("Ballast/Laden", ["Ballast", "Laden"])

    # Speed and Consumption Section
    st.header("Speed and Consumption")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Full Speed (hrs)", min_value=0.0, step=0.1)
        st.number_input("Full Speed (nm)", min_value=0.0, step=0.1)
        st.number_input("Reduced Speed/Slow Steaming (hrs)", min_value=0.0, step=0.1)
        st.number_input("Reduced Speed/Slow Steaming (nm)", min_value=0.0, step=0.1)
        st.number_input("Stopped (hrs)", min_value=0.0, step=0.1)
        st.number_input("Distance Observed (nm)", min_value=0.0, step=0.1)
    with col2:
        st.number_input("Obs Speed (SOG) (kts)", min_value=0.0, step=0.1)
        st.number_input("EM Log Speed (LOG) (kts)", min_value=0.0, step=0.1)
        st.number_input("Voyage Average Speed (kts)", min_value=0.0, step=0.1)
        st.number_input("Distance To Go (nm)", min_value=0.0, step=0.1)
        st.number_input("Distance since COSP (nm)", min_value=0.0, step=0.1)
    with col3:
        st.number_input("Voyage Order Speed (kts)", min_value=0.0, step=0.1)
        st.number_input("Voyage Order ME FO Cons (mt)", min_value=0.0, step=0.1)
        st.number_input("Voyage Order ME DO Cons (mt)", min_value=0.0, step=0.1)
        st.number_input("Course (°)", min_value=0.0, max_value=360.0, step=1.0)
        st.number_input("Draft F (m)", min_value=0.0, step=0.01)
        st.number_input("Draft A (m)", min_value=0.0, step=0.01)
        st.number_input("Displacement (mt)", min_value=0.0, step=0.1)

    # Wind and Weather Section
    st.header("Wind and Weather")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Wind Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
        st.number_input("Wind Force", min_value=0, max_value=12)
        st.number_input("Visibility (nm)", min_value=0.0, step=0.1)
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1)
        st.selectbox("Sea Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
    with col2:
        st.number_input("Swell Height (m)", min_value=0.0, step=0.1)
        st.selectbox("Swell Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
        st.number_input("Current Set (kts)", min_value=0.0, step=0.1)
        st.selectbox("Current Drift", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
        st.number_input("Air Temp (°C)", min_value=-50.0, max_value=50.0, step=0.1)
        st.checkbox("Icing on Deck?")
    st.number_input("Period of bad Weather (beyond BF scale 5, in Hours)", min_value=0.0, step=0.1)

    # Forecast next 24 Hrs Section
    st.header("Forecast next 24 Hrs")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Wind Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
        st.number_input("Wind Force", min_value=0, max_value=12)
        st.number_input("Sea Height (m)", min_value=0.0, step=0.1)
    with col2:
        st.selectbox("Sea Direction", ["North", "East", "South", "West", "North East", "North West", "South East", "South West"])
        st.number_input("Swell Height (m)", min_value=0.0, step=0.1)

    # Drifting Section
    st.header("Drifting")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Drifting Start Latitude")
        st.text_input("Drifting Start Longitude")
        st.date_input("Drifting Start Date", datetime.now())
        st.time_input("Drifting Start Time", datetime.now().time())
        st.number_input("Drifting Distance (nm)", min_value=0.0, step=0.1)
    with col2:
        st.text_input("Drifting End Latitude")
        st.text_input("Drifting End Longitude")
        st.date_input("Drifting End Date", datetime.now())
        st.time_input("Drifting End Time", datetime.now().time())
        st.number_input("Drifting Time (hrs)", min_value=0.0, step=0.1)

if __name__ == "__main__":
    main()
