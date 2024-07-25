import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import base64

# Page configuration
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

def render_svg(svg):
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}" width="300" height="100"/>'
    st.markdown(html, unsafe_allow_html=True)

def compact_infographic():
    svg = """
    <svg width="300" height="100" xmlns="http://www.w3.org/2000/svg">
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
    render_svg(svg)

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
    "start": "2023-05-25 08:00",
    "expected_end": "2023-06-15 14:00",
    "legs": [
        {"from": "Cape Town", "to": "Mauritius", "start": "2023-05-25 08:00", "end": "2023-06-01 12:00"},
        {"from": "Mauritius", "to": "Maldives", "start": "2023-06-02 09:00", "end": "2023-06-08 18:00"},
        {"from": "Maldives", "to": "Dubai", "start": "2023-06-09 10:00", "end": None}
    ]
}

def parse_date(date_str):
    if date_str is None:
        return datetime.now()
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    except ValueError:
        st.warning(f"Invalid date format: {date_str}. Using current date instead.")
        return datetime.now()

def create_voyage_progress():
    start = parse_date(current_voyage['start'])
    end = parse_date(current_voyage['expected_end'])
    total_days = max((end - start).days, 1)
    today = datetime.now()

    fig = go.Figure(layout=go.Layout(height=150, margin=dict(t=20, b=20, l=0, r=0)))

    completed_legs = [leg for leg in current_voyage['legs'] if leg['end']]
    ongoing_leg = next((leg for leg in current_voyage['legs'] if not leg['end']), None)

    colors = ['rgb(55, 126, 184)', 'rgb(77, 175, 74)', 'rgb(152, 78, 163)']
    
    cumulative_days = 0
    for i, leg in enumerate(completed_legs):
        leg_start = parse_date(leg['start'])
        leg_end = parse_date(leg['end'])
        leg_days = (leg_end - leg_start).days
        fig.add_trace(go.Bar(
            x=[leg_days], y=[0],
            orientation='h',
            marker=dict(color=colors[i % len(colors)]),
            hoverinfo='text',
            hovertext=f"{leg['from']} to {leg['to']}: {leg_start.strftime('%Y-%m-%d %H:%M')} - {leg_end.strftime('%Y-%m-%d %H:%M')}",
            base=cumulative_days
        ))
        cumulative_days += leg_days

    if ongoing_leg:
        ongoing_start = parse_date(ongoing_leg['start'])
        ongoing_days = (today - ongoing_start).days
        fig.add_trace(go.Bar(
            x=[ongoing_days], y=[0],
            orientation='h',
            marker=dict(color='rgb(228, 26, 28)', opacity=0.5),
            hoverinfo='text',
            hovertext=f"{ongoing_leg['from']} to {ongoing_leg['to']}: {ongoing_start.strftime('%Y-%m-%d %H:%M')} - Ongoing",
            base=cumulative_days
        ))
        cumulative_days += ongoing_days

    remaining_days = max(total_days - cumulative_days, 0)
    fig.add_trace(go.Bar(
        x=[remaining_days], y=[0],
        orientation='h',
        marker=dict(color='lightgrey', opacity=0.5),
        hoverinfo='text',
        hovertext=f"Remaining: {remaining_days} days",
        base=cumulative_days
    ))

    vessel_position = (today - start).days
    fig.add_shape(
        type="line", x0=vessel_position, x1=vessel_position, y0=-0.4, y1=0.4,
        line=dict(color="red", width=3)
    )

    fig.add_annotation(x=0, y=1, text=f"{current_voyage['from']}<br>{start.strftime('%Y-%m-%d %H:%M')}", showarrow=False, yanchor="bottom")
    fig.add_annotation(x=total_days, y=1, text=f"{current_voyage['to']}<br>{end.strftime('%Y-%m-%d %H:%M')}", showarrow=False, yanchor="bottom", xanchor="right")

    fig.update_layout(
        barmode='stack',
        showlegend=False,
        xaxis=dict(range=[0, total_days], showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Past History")
    for leg in current_voyage['legs']:
        st.markdown(f"**{leg['from']} to {leg['to']}**")
        st.markdown(f"Start: {leg['start']}")
        st.markdown(f"End: {leg['end'] if leg['end'] else 'Ongoing'}")
        
# Main layout
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
st.sidebar.markdown("## New Report Guide")
#st.sidebar.markdown("### Infographic")
with st.sidebar:
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
