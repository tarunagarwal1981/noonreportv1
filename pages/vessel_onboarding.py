import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Vessel Onboarding")

def create_input_row(labels, keys, col_count=4):
    cols = st.columns(col_count)
    for i, (label, key) in enumerate(zip(labels, keys)):
        with cols[i % col_count]:
            st.text_input(label, key=f"{key}_{i}")

def main():
    st.title("Vessel Onboarding")

    with st.expander("Vessel Particulars", expanded=True):
        create_input_row(
            ["Vessel Name", "LOA", "Vessel Type", "LBP"],
            ["vessel_name", "loa", "vessel_type", "lbp"]
        )
        create_input_row(
            ["Vessel Sub type", "Beam", "IMO Number", "Height above keel"],
            ["vessel_subtype", "beam", "imo_number", "height_above_keel"]
        )
        create_input_row(
            ["MMSI Number", "Bridge to bow", "Port Of Registry", "Bridge to stern"],
            ["mmsi_number", "bridge_to_bow", "port_of_registry", "bridge_to_stern"]
        )
        create_input_row(
            ["Call SIGN", "GRT", "NRT", "Lightship"],
            ["call_sign", "grt", "nrt", "lightship"]
        )

    with st.expander("Shipyard Info"):
        create_input_row(
            ["Keel laid", "Date launched", "Delivered", "Hull / Build Number"],
            ["keel_laid", "date_launched", "delivered", "hull_build_number"]
        )
        create_input_row(
            ["Ice class", "Ice class Notation", "EEDI no.", "EEXI value"],
            ["ice_class", "ice_class_notation", "eedi_no", "eexi_value"]
        )

    with st.expander("Deadweight and Freeboard"):
        create_input_row(
            ["Summer Dwt", "Winter Dwt", "Tropical Dwt", "Summer FW Dwt"],
            ["summer_dwt", "winter_dwt", "tropical_dwt", "summer_fw_dwt"]
        )
        create_input_row(
            ["Summer freeboard", "Winter freeboard", "Tropical freeboard", "Summer FW freeboard"],
            ["summer_freeboard", "winter_freeboard", "tropical_freeboard", "summer_fw_freeboard"]
        )
        create_input_row(
            ["Summer draft", "Winter draft", "Tropical draft", "Summer FW draft"],
            ["summer_draft", "winter_draft", "tropical_draft", "summer_fw_draft"]
        )

    with st.expander("Machinery Particulars"):
        create_input_row(
            ["Main ENGINE #1 make/model", "Generator#1 Make/Model", "Boiler#1 Make/Model", "Cargo pumps#1 Make/Model"],
            ["main_engine_1", "generator_1", "boiler_1", "cargo_pumps_1"]
        )
        create_input_row(
            ["Main ENGINE #2 make/model", "Generator#2 Make/Model", "Boiler#2 Make/Model", "Cargo pumps#2 Make/Model"],
            ["main_engine_2", "generator_2", "boiler_2", "cargo_pumps_2"]
        )
        create_input_row(
            ["Generator#3 Make/Model", "Generator#4 Make/Model", "Generator#5 Make/Model", "FW Generator Make/Model"],
            ["generator_3", "generator_4", "generator_5", "fw_generator"]
        )

    with st.expander("Engine Details"):
        create_input_row(
            ["Scrubber Fitted?", "Scrubber Make/Model", "Shaft Generator Fitted?", "Engine fitted with EPL/Derated Engine?"],
            ["scrubber_fitted", "scrubber_make_model", "shaft_generator_fitted", "engine_epl_derated"]
        )
        create_input_row(
            ["Volumetric or Mass Flow Meter?", "ME#1 Flowmeters make/model", "ME#2 Flowmeters make/model", "Propeller Diameter (mm)"],
            ["flow_meter_type", "me1_flowmeter", "me2_flowmeter", "propeller_diameter"]
        )

    with st.expander("Consumption Details"):
        st.subheader("At Sea")
        create_input_row(
            ["M/E Ballast", "A/E Ballast", "Blr Ballast", "M/E Laden"],
            ["me_ballast", "ae_ballast", "blr_ballast", "me_laden"]
        )
        create_input_row(
            ["A/E Laden", "Blr Laden", "", ""],
            ["ae_laden", "blr_laden", "empty1", "empty2"]
        )

        st.subheader("At Port")
        create_input_row(
            ["AE HSFO", "BLKR HSFO", "AE VLSFO", "BLKR VLSFO"],
            ["ae_hsfo", "blkr_hsfo", "ae_vlsfo", "blkr_vlsfo"]
        )

    with st.expander("Fuel Compatibility"):
        fuels = ["HFO", "LFO", "MGO", "MDO", "LPGP", "LPGB", "LNG", "LNGN2", "Methanol", "Ethanol", "Ethane", "Blend"]
        for i in range(0, len(fuels), 4):
            create_input_row(
                fuels[i:i+4],
                [f"fuel_{fuel.lower()}" for fuel in fuels[i:i+4]]
            )

    if st.button("Submit"):
        st.success("Vessel onboarding information submitted successfully!")

if __name__ == "__main__":
    main()
