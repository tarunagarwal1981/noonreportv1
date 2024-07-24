import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

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
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: white;
        border: 1px solid #d0d0d0;
        border-radius: 5px;
        padding: 10px;
        z-index: 1000;
    }
    .start-report-btn {
        position: fixed;
        top: 70px;
        right: 20px;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# Compact infographic for report guide
def compact_infographic():
    return """
    <svg width="300" height="100">
        <rect width="300" height="100" fill="#f0f8ff"/>
        <circle cx="50" cy="50" r="30" fill="#4a90e2"/>
        <text x="50" y="55" font-family="Arial" font-size="12" fill="white" text-anchor="middle">Noon</text>
        <rect x="100" y="20" width="90" height="60" fill="#82ca9d" rx="5" ry="5"/>
        <text x="145" y="50" font-family="Arial" font-size="10" fill="white" text-anchor="middle">Arrival</text>
        <text x="145" y="65" font-family="Arial" font-size="8" fill="white" text-anchor="middle">EOSP → FWE</text>
        <rect x="200" y="20" width="90" height="60" fill="#f4a261" rx="5" ry="5"/>
        <text x="245" y="50" font-family="Arial" font-size="10" fill="white" text-anchor="middle">Departure</text>
        <text x="245" y="65" font-family="Arial" font-size="8" fill="white" text-anchor="middle">SBE → COSP</text>
    </svg>
    """

# Dummy data for completed voyages
completed_voyages = [
    {"id": "V001", "from": "Singapore", "to": "Rotterdam", "start": "2023-01-01", "end": "2023-02-15"},
    {"id": "V002", "from": "Rotterdam", "to": "New York", "start": "2023-02-20", "end": "2023-03-10"},
    {"id": "V003", "from": "New York", "to": "Houston", "start": "2023-03-15", "end": "2023-03-25"},
    {"id": "V004", "from": "Houston", "to": "Santos", "start": "2023-04-01", "end": "2023-04-20"},
    {"id": "V005", "from": "Santos", "to": "Cape Town", "start": "2023-04-25", "end": "2023-05-20"},
]

# Current voyage data
current_voyage = {
    "id": "V006",
    "from": "Cape Town",
    "to": "Dubai",
    "start": "2023-05-25",
    "expected_end": "2023-06-15",
    "legs": [
        {"from": "Cape Town", "to": "Mauritius", "start": "2023-05-25", "end": "2023-06-01"},
        {"from": "Mauritius", "to": "Maldives", "start": "2023-06-02", "end": "2023-06-08"},
        {"from": "Maldives", "to": "Dubai", "start": "2023-06-09", "end": None}
    ]
}

# Main layout
st.markdown('<p class="main-header">Maritime Reporting System</p>', unsafe_allow_html=True)

# Voyage progress bar
def create_voyage_progress():
    start = datetime.strptime(current_voyage['start'], '%Y-%m-%d')
    end = datetime.strptime(current_voyage['expected_end'], '%Y-%m-%d')
    total_days = (end - start).days
    today = datetime.now().date()
    
    fig = go.Figure(layout=go.Layout(height=100, margin=dict(t=0, b=0, l=0, r=0)))
    
    for leg in current_voyage['legs']:
        leg_start = datetime.strptime(leg['start'], '%Y-%m-%d')
        leg_end = datetime.strptime(leg['end'], '%Y-%m-%d') if leg['end'] else today
        leg_color = 'rgb(55, 126, 184)' if leg['end'] else 'rgb(228, 26, 28)'
        fig.add_trace(go.Bar(
            x=[(leg_end - leg_start).days], 
            y=[0], 
            orientation='h',
            marker=dict(color=leg_color),
            hoverinfo='text',
            hovertext=f"{leg['from']} to {leg['to']}: {leg_start.strftime('%Y-%m-%d')} - {leg_end.strftime('%Y-%m-%d')}"
        ))
    
    remaining_days = max((end - today).days, 0)
    fig.add_trace(go.Bar(
        x=[remaining_days], 
        y=[0], 
        orientation='h',
        marker=dict(color='lightgrey'),
        hoverinfo='text',
        hovertext=f"Remaining: {remaining_days} days"
    ))
    
    fig.update_layout(barmode='stack', showlegend=False, xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
    fig.add_annotation(x=0, y=0, text=f"{current_voyage['from']}<br>{start.strftime('%Y-%m-%d')}", showarrow=False, xanchor='right')
    fig.add_annotation(x=1, y=0, text=f"{current_voyage['to']}<br>{end.strftime('%Y-%m-%d')}", showarrow=False, xanchor='left')
    
    vessel_position = (today - start).days / total_days
    fig.add_shape(type="line", x0=vessel_position, x1=vessel_position, y0=0, y1=1, line=dict(color="red", width=3))
    
    st.plotly_chart(fig, use_container_width=True)

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
    
    st.markdown('<p class="sub-header">Voyage Details</p>', unsafe_allow_html=True)
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

# Floating elements
st.markdown(f"""
<div class="report-guide">
    <h4>Report Guide</h4>
    {compact_infographic()}
</div>
""", unsafe_allow_html=True)

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
