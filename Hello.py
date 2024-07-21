import streamlit as st
from datetime import datetime

st.title("Vessel Departure Report")

# Tabs for different sections
tabs = st.tabs([
    "General Information", "Bilge, Sludge", "Voyage Planning", 
    "Remarks", "Lube Oil", "Fresh Water", "Services in Port", 
    "Consumption", "Cargo Operations", "Ballasting / Deballasting", 
    "Tank Cleaning", "Other Operations", "Emission in Port"
])

with tabs[0]:
    st.header("General Information")
    vessel = st.text_input("Vessel")
    voyage_no = st.text_input("Voyage No")
    port = st.text_input("Port")
    next_port = st.text_input("Next Port")
    berth_location = st.text_input("Name of Berth/Location")
    cosp = st.text_input("COSP")
    ship_mean_time_utc = st.time_input("Ship Mean Time (UTC)", datetime.now().time())
    ship_mean_time_lt = st.time_input("Ship Mean Time (LT)", datetime.now().time())
    departure_date = st.date_input("Departure Date", datetime.now().date())
    pilot_on_board = st.datetime_input("Pilot on Board (POB)", datetime.now())
    standby_engines = st.datetime_input("Standby Engines (SBE)", datetime.now())
    all_gone_and_clear = st.datetime_input("All Gone and Clear (AGC)", datetime.now())
    anchor_aweigh = st.datetime_input("Anchor Aweigh (AAW)", datetime.now())
    dropping_of_last_outward_sea_pilot = st.datetime_input("Dropping of Last Outward Sea Pilot (DLOSP)", datetime.now())
    pilot_full_away = st.datetime_input("Pilot Full Away (PFA)", datetime.now())
    commencement_of_sea_passage = st.datetime_input("Commencement of Sea Passage (COSP)", datetime.now())
    ballast_laden = st.selectbox("Ballast/Laden", ["Ballast", "Laden"])
    draft_f = st.number_input("Draft F (m)", min_value=0.0, step=0.01)
    draft_a = st.number_input("Draft A (m)", min_value=0.0, step=0.01)
    start_new_voyage = st.checkbox("Start New Voyage")
    off_hire_delay = st.number_input("Off Hire Delay (hrs)", min_value=0.0, step=0.01)
    maneuvering = st.number_input("Maneuvering (hrs)", min_value=0.0, step=0.01)
    maneuvering_distance = st.number_input("Maneuvering distance (nm)", min_value=0.0, step=0.01)
    last_port = st.text_input("Last Port")
    next_port_operation = st.text_input("Next Port operation")
    distance_to_go = st.number_input("Distance to Go (nm)", min_value=0.0, step=0.01)
    eta = st.datetime_input("ETA", datetime.now())
    me_time_counter_at_cosp = st.text_input("ME Time Counter at COSP")
    shaft_generator_power = st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.01)

with tabs[1]:
    st.header("Bilge, Sludge")
    quantity_of_sludge_landed = st.number_input("Quantity of Sludge Landed (cu.m)", min_value=0.0, step=0.01)
    quantity_of_bilge_water_landed = st.number_input("Quantity of Bilge Water Landed (cu.m)", min_value=0.0, step=0.01)
    quantity_of_garbage_landed = st.number_input("Quantity of Garbage Landed (cu.m)", min_value=0.0, step=0.01)
    lo_sample_presence = st.checkbox("LO Sample presence")

with tabs[2]:
    st.header("Voyage Planning")
    optimum_speed = st.checkbox("Optimum Speed")
    optimum_trim = st.checkbox("Optimum Trim")
    most_efficient_route = st.checkbox("Most Efficient Route")
    cargo_stowage = st.checkbox("Cargo Stowage")
    any_cargo_tank_cargo_hold_cleaning = st.checkbox("Any Cargo tank / Cargo Hold Cleaning")
    charter_standard = st.text_input("Charter Standard")
    voyage_plan_remarks = st.text_area("Voyage Plan Remarks")

with tabs[3]:
    st.header("Remarks")
    remarks = st.text_area("Remarks")

with tabs[4]:
    st.header("Lube Oil (Ltrs)")
    me_cylinder_oil_40 = {
        "Prev. ROB": st.number_input("ME Cylinder Oil 40 TBN - Prev. ROB", min_value=0.0, step=0.01),
        "Cons": st.number_input("ME Cylinder Oil 40 TBN - Cons", min_value=0.0, step=0.01),
        "Received": st.number_input("ME Cylinder Oil 40 TBN - Received", min_value=0.0, step=0.01),
        "ROB": st.number_input("ME Cylinder Oil 40 TBN - ROB", min_value=0.0, step=0.01)
    }
    me_cylinder_oil_50 = {
        "Prev. ROB": st.number_input("ME Cylinder Oil 50 TBN - Prev. ROB", min_value=0.0, step=0.01),
        "Cons": st.number_input("ME Cylinder Oil 50 TBN - Cons", min_value=0.0, step=0.01),
        "Received": st.number_input("ME Cylinder Oil 50 TBN - Received", min_value=0.0, step=0.01),
        "ROB": st.number_input("ME Cylinder Oil 50 TBN - ROB", min_value=0.0, step=0.01)
    }
    # Repeat for other lube oil types

with tabs[5]:
    st.header("Fresh Water")
    domestic_fresh_water = {
        "Previous ROB": st.number_input("Domestic Fresh Water - Previous ROB", min_value=0.0, step=0.01),
        "Received": st.number_input("Domestic Fresh Water - Received", min_value=0.0, step=0.01),
        "ROB on Dep": st.number_input("Domestic Fresh Water - ROB on Dep", min_value=0.0, step=0.01),
        "Cons": st.number_input("Domestic Fresh Water - Cons", min_value=0.0, step=0.01)
    }
    drinking_water = {
        "Previous ROB": st.number_input("Drinking Water - Previous ROB", min_value=0.0, step=0.01),
        "Received": st.number_input("Drinking Water - Received", min_value=0.0, step=0.01),
        "ROB on Dep": st.number_input("Drinking Water - ROB on Dep", min_value=0.0, step=0.01),
        "Cons": st.number_input("Drinking Water - Cons", min_value=0.0, step=0.01)
    }
    # Repeat for other water types

with tabs[6]:
    st.header("Services in Port")
    service_type = st.text_input("Service Type")
    qty = st.number_input("Qty", min_value=0.0, step=0.01)
    unit = st.text_input("Unit")
    est_cost = st.number_input("Est Cost", min_value=0.0, step=0.01)
    currency = st.text_input("Currency")
    service_on = st.text_input("Service On")
    remarks_service = st.text_area("Remarks")

with tabs[7]:
    st.header("Consumption (MT)")
    complied_with_guidelines = st.checkbox("Have you read and complied with guidelines in Circulars T17 and T17D?")
    local_port_agent_confirmed = st.checkbox("Local Port Agent has confirmed that your ship can use fuel with more than 0.1%S?")
    fuel_types = {
        "Previous ROB": st.number_input("Fuel Types - Previous ROB", min_value=0.0, step=0.01),
        "In Port - M/E": st.number_input("Fuel Types - In Port - M/E", min_value=0.0, step=0.01),
        "In Port - A/E": st.number_input("Fuel Types - In Port - A/E", min_value=0.0, step=0.01),
        "In Port - BLR": st.number_input("Fuel Types - In Port - BLR", min_value=0.0, step=0.01),
        "In Port - IGG": st.number_input("Fuel Types - In Port - IGG", min_value=0.0, step=0.01),
        "In Port - GE/EG": st.number_input("Fuel Types - In Port - GE/EG", min_value=0.0, step=0.01),
        "In Port - OTH": st.number_input("Fuel Types - In Port - OTH", min_value=0.0, step=0.01),
        "Bunker Qty": st.number_input("Fuel Types - Bunker Qty", min_value=0.0, step=0.01),
        "Sulphur %": st.number_input("Fuel Types - Sulphur %", min_value=0.0, step=0.01),
        "ROB @ (BDN)": st.number_input("Fuel Types - ROB @ (BDN)", min_value=0.0, step=0.01),
        "At Harbour - M/E": st.number_input("Fuel Types - At Harbour - M/E", min_value=0.0, step=0.01),
        "At Harbour - A/E": st.number_input("Fuel Types - At Harbour - A/E", min_value=0.0, step=0.01),
        "At Harbour - BLR": st.number_input("Fuel Types - At Harbour - BLR", min_value=0.0, step=0.01),
        "At Harbour - IGG": st.number_input("Fuel Types - At Harbour - IGG", min_value=0.0, step=0.01),
        "At Harbour - GE/EG": st.number_input("Fuel Types - At Harbour - GE/EG", min_value=0.0, step=0.01),
        "At Harbour - OTH": st.number_input("Fuel Types - At Harbour - OTH", min_value=0.0, step=0.01),
        "ROB @ (COSP)": st.number_input("Fuel Types - ROB @ (COSP)", min_value=0.0, step=0.01)
    }
    action = st.text_input("Action")

with tabs[8]:
    st.header("Cargo Operations")
    no_cargo_operations = st.checkbox("No Cargo Operations in this port")
    cargo_operation = {
        "Cargo": st.text_input("Cargo"),
        "Is Critical": st.checkbox("Is Critical"),
        "Qty (MT)": st.number_input("Qty (MT)", min_value=0.0, step=0.01),
        "Vapour Qty (MT)": st.number_input("Vapour Qty (MT)", min_value=0.0, step=0.01),
        "Oil Major Cargo": st.text_input("Oil Major Cargo"),
        "Oil Major": st.text_input("Oil Major"),
        "Basis of Final Qty": st.text_input("Basis of Final Qty"),
        "BTB Transfer Y/N": st.text_input("BTB Transfer Y/N"),
        "Commenced": st.datetime_input("Commenced", datetime.now()),
        "Completed": st.datetime_input("Completed", datetime.now()),
        "Action": st.text_input("Action")
    }

with tabs[9]:
    st.header("Ballasting / Deballasting")
    commenced_ballasting = st.datetime_input("Commenced Ballasting", datetime.now())
    completed_ballasting = st.datetime_input("Completed Ballasting", datetime.now())
    quantity_ballasted = st.number_input("Quantity Ballasted (MT)", min_value=0.0, step=0.01)
    commenced_deballasting = st.datetime_input("Commenced Deballasting", datetime.now())
    completed_deballasting = st.datetime_input("Completed Deballasting", datetime.now())
    quantity_deballasted = st.number_input("Quantity Deballasted (MT)", min_value=0.0, step=0.01)

with tabs[10]:
    st.header("Tank Cleaning")
    hold_tank_cleaning = st.checkbox("Hold / Tank Cleaning")
    hold_tank_cleaning_commenced = st.datetime_input("Hold / Tank Cleaning Commenced", datetime.now())
    hold_tank_cleaning_completed = st.datetime_input("Hold / Tank Cleaning Completed", datetime.now())
    stripping_draining = st.checkbox("Stripping / Draining")
    stripping_draining_remarks = st.text_area("Stripping / Draining Remarks")

with tabs[11]:
    st.header("Other Operations")
    other_operations = {
        "Description": st.text_area("Description"),
        "Commenced": st.datetime_input("Commenced", datetime.now()),
        "Completed": st.datetime_input("Completed", datetime.now()),
        "Action": st.text_input("Action")
    }

with tabs[12]:
    st.header("Emission in Port")
    vessel_name = st.text_input("Vessel Name")
    voyage_no_emission = st.text_input("Voyage No")
    port_emission = st.text_input("Port")
    ballast_laden_emission = st.checkbox("Ballast/Laden")
    eu_port = st.checkbox("EU Port")
    arrival = st.datetime_input("Arrival", datetime.now())
    departure = st.datetime_input("Departure", datetime.now())
    total_time_in_port = st.number_input("Total Time in Port (hrs)", min_value=0.0, step=0.01)
    total_aggregated_co2_emitted = st.number_input("Total Aggregated CO2 Emitted (T CO2)", min_value=0.0, step=0.01)

    st.subheader("Consumption (Emission in Port)")
    fuel_type = st.text_input("Fuel Type")
    emission_factor = st.number_input("Emission Factor", min_value=0.0, step=0.01)
    rob_at_fwe = st.number_input("ROB @ FWE", min_value=0.0, step=0.01)
    bunkered = st.number_input("Bunkered", min_value=0.0, step=0.01)
    rob_at_swe = st.number_input("ROB @ SWE", min_value=0.0, step=0.01)
    total_fo_cons = st.number_input("Total FO Cons", min_value=0.0, step=0.01)
    cargo_heating_cons = st.number_input("Cargo Heating Cons", min_value=0.0, step=0.01)
    aggregated_co2_emitted = st.number_input("Aggregated CO2 Emitted (MT CO2)", min_value=0.0, step=0.01)

if st.button("Submit"):
    st.write("Form submitted successfully!")
