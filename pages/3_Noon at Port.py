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

if __name__ == "__main__":
    main()
