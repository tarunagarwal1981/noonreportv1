import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import base64

# Set page config at the very beginning
st.set_page_config(layout="wide", page_title="Maritime Reporting System")

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {font-size: 24px; font-weight: bold; margin-bottom: 20px;}
    .sub-header {font-size: 18px; font-weight: bold; margin-top: 30px; margin-bottom: 10px;}
    .voyage-card {
        background-color: #f0f0f0;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        transition: background-color 0.3s;
    }
    .voyage-card:hover {background-color: #e0e0e0;}
    .info-card {
        border: 1px solid #d0d0d0;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .report-guide {
        background-color: white;
        border: 1px solid #d0d0d0;
        border-radius: 5px;
        padding: 10px;
        margin-top: 20px;
    }
    .start-report-btn {
        position: fixed;
        top: 70px;
        right: 20px;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# ... (rest of the code remains the same)

# Main function to run the app
def main():
    st.markdown('<p class="main-header">Maritime Reporting System</p>', unsafe_allow_html=True)

    # Layout
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown('<p class="sub-header">Completed Voyages</p>', unsafe_allow_html=True)
        for voyage in completed_voyages:
            st.markdown(f"""
            <div class="voyage-card">
                <b>{voyage['id']}</b>: {voyage['from']} to {voyage['to']}<br>
                {voyage['start']} - {voyage['end']}
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="sub-header">Current Voyage: {}</p>'.format(current_voyage['id']), unsafe_allow_html=True)
        create_voyage_progress()
        
        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Total Fuel Consumed (mt)", "1500")
        col_b.metric("Total CO2 Emissions (mt)", "4500")
        col_c.metric("Total Distance (nm)", "7000")
        col_d.metric("Average Speed (kts)", "12.5")
        
        st.markdown('<p class="sub-header">Voyage Legs</p>', unsafe_allow_html=True)
        for leg in current_voyage['legs']:
            st.markdown(f"""
            <div class="info-card">
                <b>{leg['from']} to {leg['to']}</b><br>
                Start: {leg['start']}<br>
                End: {leg['end'] if leg['end'] else 'Ongoing'}
            </div>
            """, unsafe_allow_html=True)

    # Report Guide in sidebar
    st.sidebar.markdown("## Report Guide")
    compact_infographic()

    # Start New Report button
    st.markdown("""
    <div class="start-report-btn">
        <a href="?new_report=true" target="_self">
            <button style="font-size: 16px; padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">
            Start New Report
        </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Check if new report button was clicked
    if st.experimental_get_query_params().get("new_report"):
        with st.form("new_report_form"):
            st.subheader("Start New Report")
            report_type = st.selectbox("Select Report Type", ["Noon", "EOSP", "FWE", "SBE", "COSP"])
            voyage_id = st.text_input("Voyage ID")
            report_date = st.date_input("Report Date")
            submit_button = st.form_submit_button("Create Report")
            
            if submit_button:
                st.success(f"New {report_type} report created for Voyage {voyage_id} on {report_date}")
                st.experimental_set_query_params()

if __name__ == "__main__":
    main()
