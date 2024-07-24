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
        H [label="Noon at Port", shape=diamond]
        A -> B -> C -> D
        D -> D [label="Daily"]
        D -> E -> F -> G
        G -> H
        H -> H [label="Daily"]
        H -> B
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
        J -> J [label="Daily"]
        J -> K -> L -> M
        M -> M [label="Daily"]
        M -> N -> O
        O -> D
    }
    """,
    "Anchorage and Drifting Transitions": """
    digraph {
        A [label="Noon at Anchor", shape=diamond]
        B [label="SBE", shape=diamond]
        C [label="Start Drifting"]
        D [label="Noon while Drifting", shape=diamond]
        E [label="SBE", shape=diamond]
        F [label="Anchoring"]
        A -> B -> C -> D
        D -> D [label="Daily"]
        D -> E -> F -> A
        A -> A [label="Daily"]
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
        H [label="FWE: Drifting"]
        A -> B -> C -> D
        D -> D [label="Daily"]
        D -> E -> F
        F -> F [label="Daily"]
        F -> G -> D
        D -> H -> A
    }
    """,
    "Anchorage to Canal/River Voyage": """
    digraph {
        A [label="Noon at Anchor", shape=diamond]
        B [label="SBE", shape=diamond]
        C [label="COSP"]
        D [label="EOSP: Canal/River Entry", shape=diamond]
        E [label="Noon in Canal/River", shape=diamond]
        F [label="COSP: Canal/River Exit"]
        G [label="EOSP", shape=diamond]
        H [label="FWE: Anchored"]
        A -> B -> C -> D -> E
        E -> E [label="Daily"]
        E -> F -> C
        C -> G -> H -> A
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
        A -> B -> C -> D
        D -> D [label="Daily"]
        D -> E -> F -> G
        G -> G [label="Daily"]
        G -> H -> I -> D
        D -> J -> K -> A
    }
    """,
    "Shifting Berth Voyage": """
    digraph {
        A [label="At Berth"]
        B [label="SBE", shape=diamond]
        C [label="Noon at Canal/River", shape=diamond]
        D [label="FWE"]
        E [label="At New Berth"]
        F [label="Noon at Port", shape=diamond]
        A -> B -> C -> D -> E
        E -> F
        F -> F [label="Daily"]
        F -> B
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
