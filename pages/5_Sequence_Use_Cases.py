import streamlit as st
import base64

st.set_page_config(layout="wide", page_title="Maritime Voyage Reporting System")

st.title("Maritime Voyage Reporting System")

# SVG Infographic
svg_code = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">
  <!-- Background -->
  <rect x="0" y="0" width="800" height="600" fill="#f0f0f0"/>
  
  <!-- Title -->
  <text x="400" y="30" font-family="Arial, sans-serif" font-size="24" fill="#333" text-anchor="middle" font-weight="bold">Maritime Reporting Flow</text>
  
  <!-- Timeline -->
  <line x1="50" y1="100" x2="750" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="50" y1="100" x2="50" y2="95" stroke="#333" stroke-width="2"/>
  <line x1="750" y1="100" x2="750" y2="95" stroke="#333" stroke-width="2"/>
  
  <!-- Report Sequence -->
  <g>
    <rect x="100" y="70" width="80" height="40" rx="5" ry="5" fill="#4a90e2"/>
    <text x="140" y="95" font-family="Arial, sans-serif" font-size="12" fill="white" text-anchor="middle">EOSP</text>
  </g>
  <g>
    <rect x="300" y="70" width="80" height="40" rx="5" ry="5" fill="#4a90e2"/>
    <text x="340" y="95" font-family="Arial, sans-serif" font-size="12" fill="white" text-anchor="middle">Arrival</text>
  </g>
  <g>
    <rect x="500" y="70" width="80" height="40" rx="5" ry="5" fill="#4a90e2"/>
    <text x="540" y="95" font-family="Arial, sans-serif" font-size="12" fill="white" text-anchor="middle">Departure</text>
  </g>
  <g>
    <rect x="700" y="70" width="80" height="40" rx="5" ry="5" fill="#4a90e2"/>
    <text x="740" y="95" font-family="Arial, sans-serif" font-size="12" fill="white" text-anchor="middle">COSP</text>
  </g>
  
  <!-- Noon Reports -->
  <g>
    <rect x="200" y="130" width="80" height="40" rx="5" ry="5" fill="#f39c12"/>
    <text x="240" y="155" font-family="Arial, sans-serif" font-size="10" fill="white" text-anchor="middle">Noon Report</text>
  </g>
  <g>
    <rect x="400" y="130" width="80" height="40" rx="5" ry="5" fill="#f39c12"/>
    <text x="440" y="155" font-family="Arial, sans-serif" font-size="10" fill="white" text-anchor="middle">Noon Report</text>
  </g>
  <g>
    <rect x="600" y="130" width="80" height="40" rx="5" ry="5" fill="#f39c12"/>
    <text x="640" y="155" font-family="Arial, sans-serif" font-size="10" fill="white" text-anchor="middle">Noon Report</text>
  </g>
  <g>
    <rect x="20" y="130" width="80" height="40" rx="5" ry="5" fill="#e74c3c"/>
    <text x="60" y="155" font-family="Arial, sans-serif" font-size="10" fill="white" text-anchor="middle">Noon at Sea</text>
  </g>
  
  <!-- Connecting lines for Noon Reports -->
  <line x1="60" y1="130" x2="60" y2="100" stroke="#e74c3c" stroke-width="2"/>
  <line x1="240" y1="130" x2="240" y2="100" stroke="#f39c12" stroke-width="2"/>
  <line x1="440" y1="130" x2="440" y2="100" stroke="#f39c12" stroke-width="2"/>
  <line x1="640" y1="130" x2="640" y2="100" stroke="#f39c12" stroke-width="2"/>
  
  <!-- Vessel Status -->
  <text x="140" y="190" font-family="Arial, sans-serif" font-size="14" fill="#333">Preparing to Stop</text>
  <text x="340" y="220" font-family="Arial, sans-serif" font-size="14" fill="#333">Stopped</text>
  <text x="540" y="190" font-family="Arial, sans-serif" font-size="14" fill="#333">Preparing to Move</text>
  <text x="740" y="220" font-family="Arial, sans-serif" font-size="14" fill="#333">Moving</text>
  
  <!-- Special Events -->
  <rect x="50" y="250" width="700" height="80" rx="10" ry="10" fill="#27ae60" fill-opacity="0.2" stroke="#27ae60" stroke-width="2"/>
  <text x="400" y="280" font-family="Arial, sans-serif" font-size="16" fill="#27ae60" text-anchor="middle" font-weight="bold">Special Events</text>
  <text x="400" y="305" font-family="Arial, sans-serif" font-size="12" fill="#27ae60" text-anchor="middle">ECA transit, Fuel changeover, Deviation, etc.</text>
  <text x="400" y="320" font-family="Arial, sans-serif" font-size="12" fill="#27ae60" text-anchor="middle">Reported in next report after start, carried forward until ended</text>
  
  <!-- Voyage Manifest -->
  <rect x="50" y="350" width="700" height="60" rx="10" ry="10" fill="#8e44ad" fill-opacity="0.2" stroke="#8e44ad" stroke-width="2"/>
  <text x="400" y="385" font-family="Arial, sans-serif" font-size="16" fill="#8e44ad" text-anchor="middle" font-weight="bold">Voyage Manifest</text>
  <text x="400" y="405" font-family="Arial, sans-serif" font-size="12" fill="#8e44ad" text-anchor="middle">All reports tagged with Voyage ID</text>
  
  <!-- Legend -->
  <rect x="50" y="430" width="20" height="20" fill="#4a90e2"/>
  <text x="80" y="445" font-family="Arial, sans-serif" font-size="12" fill="#333">Primary Reports</text>
  
  <rect x="50" y="460" width="20" height="20" fill="#f39c12"/>
  <text x="80" y="475" font-family="Arial, sans-serif" font-size="12" fill="#333">Noon Reports</text>
  
  <rect x="50" y="490" width="20" height="20" fill="#e74c3c"/>
  <text x="80" y="505" font-family="Arial, sans-serif" font-size="12" fill="#333">Noon at Sea Reports</text>
  
  <rect x="50" y="520" width="20" height="20" fill="#27ae60" fill-opacity="0.2" stroke="#27ae60" stroke-width="2"/>
  <text x="80" y="535" font-family="Arial, sans-serif" font-size="12" fill="#333">Special Events</text>
  
  <rect x="300" y="430" width="20" height="20" fill="#8e44ad" fill-opacity="0.2" stroke="#8e44ad" stroke-width="2"/>
  <text x="330" y="445" font-family="Arial, sans-serif" font-size="12" fill="#333">Voyage Manifest</text>
  
  <!-- Notes -->
  <text x="400" y="570" font-family="Arial, sans-serif" font-size="10" fill="#666" text-anchor="middle">Note: Noon Reports occur daily at 12:00 ship's local time, regardless of other reports or events.</text>
  <text x="400" y="585" font-family="Arial, sans-serif" font-size="10" fill="#666" text-anchor="middle">EOSP: End of Sea Passage, COSP: Commencement of Sea Passage</text>
</svg>
"""

# Display the SVG
st.components.v1.html(f'<div style="width: 100%; height: 600px;">{svg_code}</div>', height=600)

st.header("Voyage Flowcharts")

flowcharts = {
    "Port to Port Voyage": """
    digraph {
        A [label="At Port"]
        B [label="SBE", shape=diamond]
        C [label="Departure"]
        D [label="COSP"]
        E [label="Noon at Sea", shape=diamond]
        F [label="EOSP", shape=diamond]
        G [label="Arrival"]
        H [label="FWE"]
        I [label="At Port"]
        J [label="Noon at Port", shape=diamond]
        K [label="Special Events", shape=box, style=dotted]
        A -> B -> C -> D -> E
        E -> E [label="Daily"]
        E -> F -> G -> H -> I
        I -> J
        J -> J [label="Daily"]
        J -> B
        K -> K [label="Ongoing"]
        {rank=same; E K}
    }
    """,
    "Port to Anchorage and Back Voyage": """
    digraph {
        A [label="At Port"]
        B [label="SBE", shape=diamond]
        C [label="Departure"]
        D [label="COSP"]
        E [label="Noon at Sea", shape=diamond]
        F [label="EOSP", shape=diamond]
        G [label="FWE: Anchored"]
        H [label="Noon at Anchor", shape=diamond]
        I [label="SBE", shape=diamond]
        J [label="COSP"]
        K [label="EOSP", shape=diamond]
        L [label="Arrival"]
        M [label="FWE"]
        N [label="At Port"]
        O [label="Noon at Port", shape=diamond]
        P [label="Special Events", shape=box, style=dotted]
        A -> B -> C -> D -> E
        E -> E [label="Daily"]
        E -> F -> G -> H
        H -> H [label="Daily"]
        H -> I -> J -> E
        E -> K -> L -> M -> N
        N -> O
        O -> O [label="Daily"]
        O -> B
        P -> P [label="Ongoing"]
        {rank=same; E P}
        {rank=same; H P}
    }
    """,
    "Anchorage and Drifting Transitions": """
    digraph {
        A [label="Noon at Anchor", shape=diamond]
        B [label="SBE", shape=diamond]
        C [label="COSP"]
        D [label="Start Drifting"]
        E [label="Noon while Drifting", shape=diamond]
        F [label="EOSP", shape=diamond]
        G [label="FWE: Anchoring"]
        H [label="Special Events", shape=box, style=dotted]
        A -> B -> C -> D -> E
        E -> E [label="Daily"]
        E -> F -> G -> A
        A -> A [label="Daily"]
        H -> H [label="Ongoing"]
        {rank=same; E H}
    }
    """,
    "Drifting to Canal/River Voyage": """
    digraph {
        A [label="Noon while Drifting", shape=diamond]
        B [label="SBE", shape=diamond]
        C [label="COSP"]
        D [label="Noon at Sea", shape=diamond]
        E [label="EOSP: Canal/River Entry", shape=diamond]
        F [label="Noon in Canal/River", shape=diamond]
        G [label="COSP: Canal/River Exit"]
        H [label="EOSP", shape=diamond]
        I [label="FWE: Drifting"]
        J [label="Special Events", shape=box, style=dotted]
        A -> B -> C -> D
        D -> D [label="Daily"]
        D -> E -> F
        F -> F [label="Daily"]
        F -> G -> D
        D -> H -> I -> A
        J -> J [label="Ongoing"]
        {rank=same; D J}
        {rank=same; F J}
    }
    """,
    "STS Operation from Anchorage": """
    digraph {
        A [label="Noon at Anchor", shape=diamond]
        B [label="SBE", shape=diamond]
        C [label="COSP"]
        D [label="Noon at Sea", shape=diamond]
        E [label="EOSP", shape=diamond]
        F [label="FWE: STS"]
        G [label="Noon at STS", shape=diamond]
        H [label="SBE", shape=diamond]
        I [label="COSP"]
        J [label="EOSP", shape=diamond]
        K [label="FWE: Anchored"]
        L [label="Special Events", shape=box, style=dotted]
        A -> B -> C -> D
        D -> D [label="Daily"]
        D -> E -> F -> G
        G -> G [label="Daily"]
        G -> H -> I -> D
        D -> J -> K -> A
        L -> L [label="Ongoing"]
        {rank=same; D L}
        {rank=same; G L}
    }
    """,
    "Shifting Berth Voyage": """
    digraph {
        A [label="At Berth"]
        B [label="SBE", shape=diamond]
        C [label="Departure"]
        D [label="Noon at Canal/River", shape=diamond]
        E [label="Arrival"]
        F [label="FWE"]
        G [label="At New Berth"]
        H [label="Noon at Port", shape=diamond]
        I [label="Special Events", shape=box, style=dotted]
        A -> B -> C -> D -> E -> F -> G
        G -> H
        H -> H [label="Daily"]
        H -> B
        I -> I [label="Ongoing"]
        {rank=same; D I}
    }
    """
}

selected_flowchart = st.selectbox("Select a Voyage Scenario", list(flowcharts.keys()))

st.subheader(selected_flowchart)
st.graphviz_chart(flowcharts[selected_flowchart])

st.markdown("""
### Flowchart Legend:
- SBE: Stand By Engines
- COSP: Commencement of Sea Passage
- EOSP: End of Sea Passage
- FWE: Finished With Engines
- STS: Ship-to-Ship

### Flowchart Explanation:
- Diamond shapes represent Noon reports and key decision points.
- Rectangles represent other reports (COSP, FWE, etc.) and vessel states.
- Dotted boxes represent ongoing Special Events.
- Looping arrows (e.g., on Noon reports) indicate that these reports continue daily until the next event.
- All reports within a voyage are tagged with the Voyage Manifest ID (not shown in flowcharts for simplicity).

### Voyage Manifest:
The Voyage Manifest is a crucial component of the maritime reporting system:
- It's created at the beginning of each voyage and can be saved as a draft.
- Once activated, all subsequent reports are tagged with the Voyage Manifest ID.
- A new Voyage Manifest can only be opened after the previous one is closed.
- It provides context for all reports within a voyage, ensuring continuity and traceability.

### Special Events:
Special events are represented in the flowcharts as dotted boxes to indicate their ongoing nature. These include:
- ECA (Emission Control Area) transit
- Fuel changeover
- Deviation from planned route
- Weather routing
- Slow steaming
- Equipment malfunction

Special events are reported in the next report after they start and are carried forward in all subsequent reports until they end.

### Time-Based Rules:
While not explicitly shown in the flowcharts, the following time-based rules should be considered:
1. Noon Reports must be filed daily at 12:00 ship's local time.
2. EOSP should be filed as soon as the vessel is preparing to stop.
3. Arrival Report should be filed immediately after the vessel has stopped.
4. Departure Report should be filed when the vessel is preparing to move.
5. COSP should be filed as soon as the vessel starts moving for a sea passage.
6. Special event start and end times should be recorded as accurately as possible.

### Notes:
- The system must maintain chronological order of all reports and events.
- Data consistency (e.g., positions, fuel consumption) should be maintained across reports.
- Any changes or corrections to submitted reports must be logged with appropriate justification.
""")

st.markdown("---")

st.subheader("Implementation Considerations")

st.markdown("""
When implementing this maritime reporting system, consider the following:

1. **User Interface**: Design an intuitive interface that guides users through the correct sequence of reports based on the vessel's current status.

2. **Validation Rules**: Implement strict validation rules to ensure the logical flow of reports and data consistency.

3. **Special Events Handling**: Develop a mechanism to easily start, track, and end special events across multiple reports.

4. **Voyage Manifest Integration**: Ensure all reports are properly tagged with the current Voyage Manifest ID and that manifests are managed correctly.

5. **Time Zone Management**: Implement robust time zone handling to manage the distinction between ship's local time and UTC.

6. **Data Analytics**: Consider implementing analytics features to derive insights from the collected data, such as fuel efficiency analysis or route optimization.

7. **Compliance Reporting**: Ensure the system can generate reports that comply with MRV (Monitoring, Reporting, Verification) and IMO DCS (Data Collection System) regulations.

8. **Offline Capability**: Given the nature of maritime operations, consider implementing offline capabilities with data synchronization when connectivity is available.

9. **Security and Audit Trail**: Implement strong security measures and maintain a comprehensive audit trail of all report submissions and modifications.

10. **Integration**: Consider integration capabilities with other shipboard systems (e.g., AIS, ECDIS) for enhanced data accuracy and reduced manual input.
""")

st.markdown("---")
st.markdown("© 2023 Maritime Reporting System. All rights reserved.")
