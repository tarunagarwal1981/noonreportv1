import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Function to generate the infographic (as previously defined)
def generate_infographic():
    svg_code = f"""
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
    return svg_code
  
# Function to create dummy voyage data
def create_dummy_voyages():
    return [
        {"id": "V001", "from": "Singapore", "to": "Rotterdam", "type": "Laden"},
        {"id": "V002", "from": "Rotterdam", "to": "New York", "type": "Ballast"},
        {"id": "V003", "from": "New York", "to": "Houston", "type": "Laden"},
    ]

# Function to create dummy voyage legs
def create_dummy_legs(voyage_id):
    if voyage_id == "V001":
        return [
            {"from": "Singapore", "to": "Colombo (Anchor)", "type": "COSP to EOSP"},
            {"from": "Colombo", "to": "Suez Canal", "type": "COSP to EOSP"},
            {"from": "Suez Canal", "to": "Rotterdam", "type": "COSP to EOSP"},
        ]
    elif voyage_id == "V002":
        return [
            {"from": "Rotterdam", "to": "English Channel", "type": "COSP to EOSP"},
            {"from": "English Channel", "to": "New York", "type": "COSP to EOSP"},
        ]
    else:
        return [
            {"from": "New York", "to": "Florida Coast", "type": "COSP to EOSP"},
            {"from": "Florida Coast", "to": "Houston", "type": "COSP to EOSP"},
        ]

# Function to create dummy KPI data
def create_dummy_kpis(voyage_id):
    return {
        "total_fuel": round(1000 + 500 * int(voyage_id[-1]), 2),
        "total_co2": round(3000 + 1500 * int(voyage_id[-1]), 2),
        "total_distance": round(5000 + 2000 * int(voyage_id[-1]), 2),
        "avg_speed": round(12 + 0.5 * int(voyage_id[-1]), 2),
    }

# Function to create KPI charts
def create_kpi_charts(kpis):
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "number+gauge+delta",
        value = kpis['total_fuel'],
        domain = {'x': [0, 0.5], 'y': [0, 0.5]},
        title = {'text': "Total Fuel Consumed (mt)"},
        delta = {'reference': 2000},
        gauge = {
            'axis': {'range': [None, 5000]},
            'bar': {'color': "darkblue"},
            'steps' : [
                {'range': [0, 1500], 'color': "lightgray"},
                {'range': [1500, 3000], 'color': "gray"}],
            'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 3000}}))

    fig.add_trace(go.Indicator(
        mode = "number+gauge+delta",
        value = kpis['total_co2'],
        domain = {'x': [0.5, 1], 'y': [0, 0.5]},
        title = {'text': "Total CO2 Emissions (mt)"},
        delta = {'reference': 6000},
        gauge = {
            'axis': {'range': [None, 15000]},
            'bar': {'color': "darkgreen"},
            'steps' : [
                {'range': [0, 5000], 'color': "lightgray"},
                {'range': [5000, 10000], 'color': "gray"}],
            'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 9000}}))

    fig.add_trace(go.Indicator(
        mode = "number+gauge+delta",
        value = kpis['total_distance'],
        domain = {'x': [0, 0.5], 'y': [0.5, 1]},
        title = {'text': "Total Distance (nm)"},
        delta = {'reference': 8000},
        gauge = {
            'axis': {'range': [None, 20000]},
            'bar': {'color': "darkorange"},
            'steps' : [
                {'range': [0, 5000], 'color': "lightgray"},
                {'range': [5000, 10000], 'color': "gray"}],
            'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 12000}}))

    fig.add_trace(go.Indicator(
        mode = "number+gauge+delta",
        value = kpis['avg_speed'],
        domain = {'x': [0.5, 1], 'y': [0.5, 1]},
        title = {'text': "Average Speed (kts)"},
        delta = {'reference': 13},
        gauge = {
            'axis': {'range': [None, 20]},
            'bar': {'color': "darkred"},
            'steps' : [
                {'range': [0, 10], 'color': "lightgray"},
                {'range': [10, 15], 'color': "gray"}],
            'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 15}}))

    fig.update_layout(height=500)
    return fig

# Main app
def main():
    st.set_page_config(layout="wide", page_title="Maritime Reporting System")

    # Add custom CSS to make the infographic sticky
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
        </style>
        """, unsafe_allow_html=True)

    # Display the infographic at the top
    st.markdown('<div class="stickytop">', unsafe_allow_html=True)
    st.markdown(generate_infographic(), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Create two columns for the main content
    left_column, right_column = st.columns([1, 3])

    # Left column: Historical Voyages
    with left_column:
        st.subheader("Historical Voyages")
        voyages = create_dummy_voyages()
        selected_voyage = st.selectbox("Select a Voyage", 
                                       [f"{v['id']}: {v['from']} to {v['to']} ({v['type']})" for v in voyages])
        selected_voyage_id = selected_voyage.split(":")[0]

    # Right column: Voyage Details and KPIs
    with right_column:
        st.subheader(f"Voyage Details: {selected_voyage}")
        
        # KPI Charts
        kpis = create_dummy_kpis(selected_voyage_id)
        st.plotly_chart(create_kpi_charts(kpis), use_container_width=True)

        # Voyage Legs
        st.subheader("Voyage Legs")
        legs = create_dummy_legs(selected_voyage_id)
        leg_df = pd.DataFrame(legs)
        st.table(leg_df)

    # Floating button to start a new report
    st.markdown(
        f'''
        <div class="reportbutton">
            <a href="?new_report=true" target="_self">
                <button style="font-size: 16px; padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    Start New Report
                </button>
            </a>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Check if new report button was clicked
    if st.experimental_get_query_params().get("new_report"):
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
            # Here you would typically save the new report and redirect to the report page
            st.experimental_set_query_params()  # Clear the query parameter

if __name__ == "__main__":
    main()
