import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Function to generate the infographic
def generate_infographic():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 100" style="width:100%; height:auto;">
        <rect x="0" y="0" width="800" height="100" fill="#f0f8ff"/>
        
        <circle cx="100" cy="50" r="40" fill="#4a90e2"/>
        <text x="100" y="55" font-family="Arial, sans-serif" font-size="14" fill="white" text-anchor="middle">Noon</text>
        <text x="100" y="90" font-family="Arial, sans-serif" font-size="12" fill="#333" text-anchor="middle">Daily</text>

        <rect x="200" y="10" width="250" height="80" fill="#82ca9d" rx="10" ry="10"/>
        <text x="325" y="30" font-family="Arial, sans-serif" font-size="14" fill="white" text-anchor="middle">Arrival</text>
        <text x="325" y="45" font-family="Arial, sans-serif" font-size="10" fill="white" text-anchor="middle">(Anchor, Port, Drifting, STS, etc.)</text>
        <rect x="210" y="55" width="110" height="30" fill="white" rx="5" ry="5"/>
        <text x="265" y="75" font-family="Arial, sans-serif" font-size="12" fill="#333" text-anchor="middle">1. EOSP</text>
        <rect x="330" y="55" width="110" height="30" fill="white" rx="5" ry="5"/>
        <text x="385" y="75" font-family="Arial, sans-serif" font-size="12" fill="#333" text-anchor="middle">2. FWE</text>

        <rect x="500" y="10" width="250" height="80" fill="#f4a261" rx="10" ry="10"/>
        <text x="625" y="30" font-family="Arial, sans-serif" font-size="14" fill="white" text-anchor="middle">Departure</text>
        <text x="625" y="45" font-family="Arial, sans-serif" font-size="10" fill="white" text-anchor="middle">(Anchor, Port, Drifting, STS, etc.)</text>
        <rect x="510" y="55" width="110" height="30" fill="white" rx="5" ry="5"/>
        <text x="565" y="75" font-family="Arial, sans-serif" font-size="12" fill="#333" text-anchor="middle">1. SBE</text>
        <rect x="630" y="55" width="110" height="30" fill="white" rx="5" ry="5"/>
        <text x="685" y="75" font-family="Arial, sans-serif" font-size="12" fill="#333" text-anchor="middle">2. COSP</text>
    </svg>
    """

# Function to create dummy voyage data
def create_dummy_voyages():
    return [
        {"id": "V001", "from": "Singapore", "to": "Rotterdam", "type": "Laden", "start_date": "2023-01-01", "end_date": "2023-02-15"},
        {"id": "V002", "from": "Rotterdam", "to": "New York", "type": "Ballast", "start_date": "2023-02-20", "end_date": "2023-03-10"},
        {"id": "V003", "from": "New York", "to": "Houston", "type": "Laden", "start_date": "2023-03-15", "end_date": "2023-03-25"},
        {"id": "V004", "from": "Houston", "to": "Santos", "type": "Laden", "start_date": "2023-04-01", "end_date": "2023-04-20"},
        {"id": "V005", "from": "Santos", "to": "Cape Town", "type": "Ballast", "start_date": "2023-04-25", "end_date": "2023-05-20"},
        {"id": "V006", "from": "Cape Town", "to": "Dubai", "type": "Laden", "start_date": "2023-05-25", "end_date": "2023-06-15"}
    ]

# Function to create dummy voyage legs
def create_dummy_legs(voyage_id):
    legs = {
        "V001": [
            {"from": "Singapore", "to": "Colombo (Anchor)", "type": "COSP to EOSP"},
            {"from": "Colombo", "to": "Suez Canal", "type": "COSP to EOSP"},
            {"from": "Suez Canal", "to": "Rotterdam", "type": "COSP to EOSP"},
        ],
        "V002": [
            {"from": "Rotterdam", "to": "English Channel", "type": "COSP to EOSP"},
            {"from": "English Channel", "to": "New York", "type": "COSP to EOSP"},
        ],
        "V003": [
            {"from": "New York", "to": "Florida Coast", "type": "COSP to EOSP"},
            {"from": "Florida Coast", "to": "Houston", "type": "COSP to EOSP"},
        ],
        "V004": [
            {"from": "Houston", "to": "Caribbean Sea", "type": "COSP to EOSP"},
            {"from": "Caribbean Sea", "to": "Santos", "type": "COSP to EOSP"},
        ],
        "V005": [
            {"from": "Santos", "to": "Rio de Janeiro", "type": "COSP to EOSP"},
            {"from": "Rio de Janeiro", "to": "Cape Town", "type": "COSP to EOSP"},
        ],
        "V006": [
            {"from": "Cape Town", "to": "Mauritius", "type": "COSP to EOSP"},
            {"from": "Mauritius", "to": "Dubai", "type": "COSP to EOSP"},
        ]
    }
    return legs.get(voyage_id, [])

# Function to create dummy KPI data
def create_dummy_kpis(voyage_id):
    return {
        "total_fuel": round(1000 + 500 * int(voyage_id[-1]), 2),
        "total_co2": round(3000 + 1500 * int(voyage_id[-1]), 2),
        "total_distance": round(5000 + 2000 * int(voyage_id[-1]), 2),
        "avg_speed": round(12 + 0.5 * int(voyage_id[-1]), 2),
    }

# Main app
def main():
    st.set_page_config(layout="wide", page_title="Maritime Reporting System")

    # Add custom CSS
    st.markdown("""
        <style>
        .stickytop {
            position: sticky;
            top: 0;
            z-index: 999;
            background-color: white;
            padding: 10px 0;
        }
        .reportbutton {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 999;
        }
        .voyage-item {
            background-color: #f0f0f0;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .voyage-item:hover {
            background-color: #e0e0e0;
        }
        </style>
        """, unsafe_allow_html=True)

    # Display the infographic at the top
    st.markdown('<div class="stickytop">', unsafe_allow_html=True)
    st.components.v1.html(generate_infographic(), height=120)
    st.markdown('</div>', unsafe_allow_html=True)

    # Create two columns for the main content
    left_column, right_column = st.columns([1, 3])

    # Left column: Historical Voyages
    with left_column:
        st.subheader("Historical Voyages")
        voyages = create_dummy_voyages()
        for voyage in voyages:
            voyage_html = f"""
            <div class="voyage-item">
                <h4>{voyage['id']}: {voyage['from']} to {voyage['to']}</h4>
                <p>Type: {voyage['type']}</p>
                <p>Date: {voyage['start_date']} to {voyage['end_date']}</p>
            </div>
            """
            if st.markdown(voyage_html, unsafe_allow_html=True):
                selected_voyage_id = voyage['id']
                break

    # Right column: Voyage Details and KPIs
    with right_column:
        st.subheader(f"Voyage Details: {selected_voyage_id}")
        
        # KPI Metrics
        kpis = create_dummy_kpis(selected_voyage_id)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Fuel Consumed (mt)", kpis['total_fuel'])
        col2.metric("Total CO2 Emissions (mt)", kpis['total_co2'])
        col3.metric("Total Distance (nm)", kpis['total_distance'])
        col4.metric("Average Speed (kts)", kpis['avg_speed'])

        # KPI Bar Chart
        st.subheader("KPI Comparison")
        chart_data = pd.DataFrame({
            'KPI': ['Fuel', 'CO2', 'Distance', 'Speed'],
            'Value': [kpis['total_fuel'], kpis['total_co2'], kpis['total_distance'], kpis['avg_speed']]
        })
        st.bar_chart(chart_data.set_index('KPI'))

        # Voyage Legs
        st.subheader("Voyage Legs")
        legs = create_dummy_legs(selected_voyage_id)
        leg_df = pd.DataFrame(legs)
        st.table(leg_df)

    # Floating button to start a new report
    st.markdown(
        f'''
        <div class="reportbutton">
            <button onclick="parent.postMessage('new_report', '*')" style="font-size: 16px; padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Start New Report
            </button>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Check if new report button was clicked
    if st.session_state.get('show_new_report_modal', False):
        show_new_report_modal()

def show_new_report_modal():
    with st.form("new_report_form"):
        st.subheader("Start New Report")
        report_type = st.selectbox("Select Report Type", ["Noon", "EOSP", "FWE", "SBE", "COSP"])
        voyage_id = st.text_input("Voyage ID")
        report_date = st.date_input("Report Date")
        submit_button = st.form_submit_button("Create Report")

        if submit_button:
            st.success(f"New {report_type} report created for Voyage {voyage_id} on {report_date}")
            st.session_state.show_new_report_modal = False

if __name__ == "__main__":
    main()
