import streamlit as st

st.set_page_config(layout="wide", page_title="Maritime Voyage Flowcharts")

st.title("Maritime Voyage Flowcharts")

flowcharts = {
    "Port to Port Voyage": """
    digraph {
        A [label="At Port"]
        B [label="SBE", shape=diamond]
        C [label="COSP"]
        D [label="Noon at Sea", shape=diamond]
        E [label="EOSP", shape=diamond]
        F [label="FWE"]
        G [label="At Port"]
        A -> B -> C -> D
        D -> D [label="Daily"]
        D -> E -> F -> G
    }
    """,
    "Port to Anchorage and Back Voyage": """
    digraph {
        A [label="At Port"]
        B [label="SBE", shape=diamond]
        C [label="COSP"]
        D [label="Noon at Sea", shape=diamond]
        E [label="EOSP", shape=diamond]
        F [label="FWE: Anchored"]
        G [label="Noon at Anchor", shape=diamond]
        H [label="Anchor Lifting", shape=diamond]
        I [label="Berthing"]
        J [label="Noon at Port", shape=diamond]
        K [label="SBE", shape=diamond]
        L [label="Anchoring"]
        M [label="Noon at Anchor", shape=diamond]
        N [label="Anchor Lift", shape=diamond]
        O [label="COSP"]
        A -> B -> C -> D
        D -> D [label="Daily"]
        D -> E -> F -> G
        G -> G [label="Daily"]
        G -> H -> I -> J
        J -> K -> L -> M
        M -> N -> O
        O -> D
    }
    """,
    "Port to Drifting Voyage": """
    digraph {
        A [label="At Port"]
        B [label="SBE", shape=diamond]
        C [label="COSP"]
        D [label="Noon at Sea", shape=diamond]
        E [label="FWE: Drifting"]
        F [label="Noon while Drifting", shape=diamond]
        G [label="SBE", shape=diamond]
        H [label="COSP"]
        A -> B -> C -> D
        D -> D [label="Daily"]
        D -> E -> F
        F -> F [label="Daily"]
        F -> G -> H
        H -> D
    }
    """,
    "Port to Canal/River Voyage": """
    digraph {
        A [label="At Port"]
        B [label="SBE", shape=diamond]
        C [label="COSP"]
        D [label="Noon at Sea", shape=diamond]
        E [label="EOSP: Canal/River Entry", shape=diamond]
        F [label="Noon in Canal/River", shape=diamond]
        G [label="COSP: Canal/River Exit"]
        H [label="Noon at Sea", shape=diamond]
        I [label="EOSP for Anchor", shape=diamond]
        J [label="Anchoring"]
        K [label="Noon at Anchor", shape=diamond]
        L [label="SBE for Canal/River Entry", shape=diamond]
        M [label="Noon in Canal/River", shape=diamond]
        N [label="COSP"]
        O [label="Noon at Sea", shape=diamond]
        A -> B -> C -> D
        D -> D [label="Daily"]
        D -> E -> F
        F -> F [label="Daily"]
        F -> G -> H
        H -> H [label="Daily"]
        H -> I -> J -> K
        K -> L -> M
        M -> N -> O
        O -> O [label="Daily"]
    }
    """,
    "STS Operation Voyage": """
    digraph {
        A [label="At Port"]
        B [label="SBE", shape=diamond]
        C [label="COSP"]
        D [label="Noon at Sea", shape=diamond]
        E [label="EOSP", shape=diamond]
        F [label="FWE: STS"]
        G [label="Noon at STS", shape=diamond]
        H [label="SBE", shape=diamond]
        I [label="COSP"]
        J [label="Noon at Sea", shape=diamond]
        K [label="EOSP", shape=diamond]
        L [label="FWE"]
        M [label="At Port"]
        A -> B -> C -> D
        D -> D [label="Daily"]
        D -> E -> F -> G
        G -> G [label="Daily"]
        G -> H -> I -> J
        J -> J [label="Daily"]
        J -> K -> L -> M
    }
    """,
    "Shifting Berth Voyage": """
    digraph {
        A [label="At Berth"]
        B [label="SBE", shape=diamond]
        C [label="Noon at Canal/River", shape=diamond]
        D [label="FWE"]
        E [label="At New Berth"]
        A -> B -> C -> D -> E
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

### Notes:
- Noon reports and key decision points are represented by diamond shapes.
- Other reports (COSP, FWE) and states are represented by rectangles.
- Looping arrows (e.g., on Noon reports) indicate that these reports continue daily until the next event.
""")

st.markdown("---")
st.markdown("© 2023 Maritime Reporting System. All rights reserved.")
