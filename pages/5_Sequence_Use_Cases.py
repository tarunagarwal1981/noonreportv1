import streamlit as st
import streamlit.components.v1 as components

# Ensure you have streamlit-mermaid installed
# pip install streamlit-mermaid
import mermaid

st.set_page_config(layout="wide", page_title="Maritime Voyage Flowcharts")

st.title("Maritime Voyage Flowcharts")

flowcharts = {
    "Port to Port Voyage": """
    graph TD
        A[At Port] --> B{SBE}
        B --> C[COSP]
        C --> D{Noon at Sea}
        D --> D
        D --> E{EOSP}
        E --> F[FWE]
        F --> G[At Port]
    """,
    "Port to Anchorage Voyage": """
    graph TD
        A[At Port] --> B{SBE}
        B --> C[COSP]
        C --> D{Noon at Sea}
        D --> D
        D --> E{EOSP}
        E --> F[FWE: Anchored]
        F --> G{Noon at Anchor}
        G --> G
    """,
    "Anchorage to Port Voyage": """
    graph TD
        A{Noon at Anchor} --> B{SBE}
        B --> C[COSP]
        C --> D{Noon at Sea}
        D --> D
        D --> E{EOSP}
        E --> F[FWE]
        F --> G[At Port]
    """,
    "Port to Drifting Voyage": """
    graph TD
        A[At Port] --> B{SBE}
        B --> C[COSP]
        C --> D{Noon at Sea}
        D --> D
        D --> E[FWE: Drifting]
        E --> F{Noon while Drifting}
        F --> F
    """,
    "Drifting to Port Voyage": """
    graph TD
        A{Noon while Drifting} --> B{SBE}
        B --> C[COSP]
        C --> D{Noon at Sea}
        D --> D
        D --> E{EOSP}
        E --> F[FWE]
        F --> G[At Port]
    """,
    "Port to Canal/River Voyage": """
    graph TD
        A[At Port] --> B{SBE}
        B --> C[COSP]
        C --> D{Noon at Sea}
        D --> D
        D --> E{EOSP: Canal/River Entry}
        E --> F{Noon in Canal/River}
        F --> F
        F --> G[COSP: Canal/River Exit]
        G --> H{Noon at Sea}
        H --> H
    """,
    "Canal/River to Port Voyage": """
    graph TD
        A{Noon in Canal/River} --> B[COSP: Canal/River Exit]
        B --> C{Noon at Sea}
        C --> C
        C --> D{EOSP}
        D --> E[FWE]
        E --> F[At Port]
    """,
    "Port to STS Operation Voyage": """
    graph TD
        A[At Port] --> B{SBE}
        B --> C[COSP]
        C --> D{Noon at Sea}
        D --> D
        D --> E{EOSP}
        E --> F[FWE: STS]
        F --> G{Noon at STS}
        G --> G
    """,
    "STS Operation to Port Voyage": """
    graph TD
        A{Noon at STS} --> B{SBE}
        B --> C[COSP]
        C --> D{Noon at Sea}
        D --> D
        D --> E{EOSP}
        E --> F[FWE]
        F --> G[At Port]
    """,
    "Shifting Berth Voyage": """
    graph TD
        A[At Berth] --> B{SBE}
        B --> C[Maneuvering]
        C --> D[FWE]
        D --> E[At New Berth]
    """
}

selected_flowchart = st.selectbox("Select a Voyage Scenario", list(flowcharts.keys()))

st.subheader(selected_flowchart)
mermaid(flowcharts[selected_flowchart])

st.markdown("""
### Flowchart Legend:
- SBE: Stand By Engines
- COSP: Commencement of Sea Passage
- EOSP: End of Sea Passage
- FWE: Finished With Engines
- STS: Ship-to-Ship

### Notes:
- Noon reports are represented by diamond shapes and occur daily.
- Other reports (SBE, COSP, EOSP, FWE) are represented by rectangles and occur at specific events.
- Looping arrows (e.g., on Noon reports) indicate that these reports continue daily until the next event.
""")

st.markdown("---")
st.markdown("© 2023 Maritime Reporting System. All rights reserved.")
