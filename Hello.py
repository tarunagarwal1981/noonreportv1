import streamlit as st
from datetime import datetime

st.title("Vessel Departure Report")

# Tabs for different sections
tabs = st.tabs(["General Information", "Operations", "Emissions in Port"])

# General Information Tab
with tabs[0]:
    st.header("General Information")
    # General Information Fields
    col1, col2, col3 = st.columns(3)
    with col1:
        vessel = st.text_input("Vessel")
        voyage_no = st.text_input("Voyage No")
        port = st.text_input("Port")
        next_port = st.text_input("Next Port")
    with col2:
        berth_location = st.text_input("Name of Berth/Location")
        cosp = st.text_input("COSP")
        ship_mean_time_utc = st.time_input("Ship Mean Time (UTC)", datetime.now().time())
        ship_mean_time_lt = st.time_input("Ship Mean Time (LT)", datetime.now().time())
    with col3:
        departure_date = st.date_input("Departure Date", datetime.now().date())
        last_port = st.text_input("Last Port")
        next_port_operation = st.text_input("Next Port operation")
        distance_to_go = st.number_input("Distance to Go (nm)", min_value=0.0, step=0.01)
    
    col1, col2 = st.columns(2)
    with col1:
        eta = st.date_input("ETA Date", datetime.now().date())
        eta_time = st.time_input("ETA Time", datetime.now().time())
        me_time_counter_at_cosp = st.text_input("ME Time Counter at COSP")
        shaft_generator_power = st.number_input("Shaft Generator Power (kw)", min_value=0.0, step=0.01)
    with col2:
        draft_f = st.number_input("Draft F (m)", min_value=0.0, step=0.01)
        draft_a = st.number_input("Draft A (m)", min_value=0.0, step=0.01)
        start_new_voyage = st.checkbox("Start New Voyage")
        off_hire_delay = st.number_input("Off Hire Delay (hrs)", min_value=0.0, step=0.01)
        maneuvering = st.number_input("Maneuvering (hrs)", min_value=0.0, step=0.01)
        maneuvering_distance = st.number_input("Maneuvering distance (nm)", min_value=0.0, step=0.01)
    
    st.header("Voyage Planning")
    col1, col2 = st.columns(2)
    with col1:
        optimum_speed = st.checkbox("Optimum Speed")
        optimum_trim = st.checkbox("Optimum Trim")
        most_efficient_route = st.checkbox("Most Efficient Route")
        cargo_stowage = st.checkbox("Cargo Stowage")
    with col2:
        any_cargo_tank_cargo_hold_cleaning = st.checkbox("Any Cargo tank / Cargo Hold Cleaning")
        charter_standard = st.text_input("Charter Standard")
    voyage_plan_remarks = st.text_area("Voyage Plan Remarks")
    
    st.header("Remarks")
    remarks_general = st.text_area("General Remarks")
    
    st.header("Services in Port")
    service_type = st.text_input("Service Type")
    col1, col2, col3 = st.columns(3)
    with col1:
        qty = st.number_input("Qty", min_value=0.0, step=0.01)
        unit = st.text_input("Unit")
    with col2:
        est_cost = st.number_input("Est Cost", min_value=0.0, step=0.01)
        currency = st.text_input("Currency")
    with col3:
        service_on = st.text_input("Service On")
    remarks_service = st.text_area("Service Remarks")
    
    st.header("Consumption (MT)")
    col1, col2 = st.columns(2)
    with col1:
        complied_with_guidelines = st.checkbox("Have you read and complied with guidelines in Circulars T17 and T17D?")
        local_port_agent_confirmed = st.checkbox("Local Port Agent has confirmed that your ship can use fuel with more than 0.1%S?")
    with col2:
        fuel_types_prev_rob = st.number_input("Fuel Types - Previous ROB", min_value=0.0, step=0.01)
        fuel_types_in_port_me = st.number_input("Fuel Types - In Port - M/E", min_value=0.0, step=0.01)
        fuel_types_in_port_ae = st.number_input("Fuel Types - In Port - A/E", min_value=0.0, step=0.01)
        fuel_types_in_port_blr = st.number_input("Fuel Types - In Port - BLR", min_value=0.0, step=0.01)
        fuel_types_in_port_igg = st.number_input("Fuel Types - In Port - IGG", min_value=0.0, step=0.01)
        fuel_types_in_port_geeg = st.number_input("Fuel Types - In Port - GE/EG", min_value=0.0, step=0.01)
        fuel_types_in_port_oth = st.number_input("Fuel Types - In Port - OTH", min_value=0.0, step=0.01)
        fuel_types_bunker_qty = st.number_input("Fuel Types - Bunker Qty", min_value=0.0, step=0.01)
        fuel_types_sulphur = st.number_input("Fuel Types - Sulphur %", min_value=0.0, step=0.01)
        fuel_types_rob_bdn = st.number_input("Fuel Types - ROB @ (BDN)", min_value=0.0, step=0.01)
        fuel_types_rob_cosp = st.number_input("Fuel Types - ROB @ (COSP)", min_value=0.0, step=0.01)
    action = st.text_input("Consumption Action")
    
    st.header("Fresh Water")
    col1, col2, col3 = st.columns(3)
    with col1:
        domestic_fresh_water_prev_rob = st.number_input("Domestic Fresh Water - Previous ROB", min_value=0.0, step=0.01)
        domestic_fresh_water_received = st.number_input("Domestic Fresh Water - Received", min_value=0.0, step=0.01)
        domestic_fresh_water_rob_dep = st.number_input("Domestic Fresh Water - ROB on Dep", min_value=0.0, step=0.01)
        domestic_fresh_water_cons = st.number_input("Domestic Fresh Water - Cons", min_value=0.0, step=0.01)
    with col2:
        drinking_water_prev_rob = st.number_input("Drinking Water - Previous ROB", min_value=0.0, step=0.01)
        drinking_water_received = st.number_input("Drinking Water - Received", min_value=0.0, step=0.01)
        drinking_water_rob_dep = st.number_input("Drinking Water - ROB on Dep", min_value=0.0, step=0.01)
        drinking_water_cons = st.number_input("Drinking Water - Cons", min_value=0.0, step=0.01)
    with col3:
        boiler_water_prev_rob = st.number_input("Boiler Water - Previous ROB", min_value=0.0, step=0.01)
        boiler_water_received = st.number_input("Boiler Water - Received", min_value=0.0, step=0.01)
        boiler_water_rob_dep = st.number_input("Boiler Water - ROB on Dep", min_value=0.0, step=0.01)
        boiler_water_cons = st.number_input("Boiler Water - Cons", min_value=0.0, step=0.01)
        tank_cleaning_water_prev_rob = st.number_input("Tank Cleaning Water - Previous ROB", min_value=0.0, step=0.01)
        tank_cleaning_water_received = st.number_input("Tank Cleaning Water - Received", min_value=0.0, step=0.01)
        tank_cleaning_water_rob_dep = st.number_input("Tank Cleaning Water - ROB on Dep", min_value=0.0, step=0.01)
        tank_cleaning_water_cons = st.number_input("Tank Cleaning Water - Cons", min_value=0.0, step=0.01)
    
    st.header("Lube Oil (Ltrs)")
    col1, col2, col3 = st.columns(3)
    with col1:
        me_cylinder_oil_40_prev_rob = st.number_input("ME Cylinder Oil 40 TBN - Prev. ROB", min_value=0.0, step=0.01)
        me_cylinder_oil_40_cons = st.number_input("ME Cylinder Oil 40 TBN - Cons", min_value=0.0, step=0.01)
        me_cylinder_oil_40_received = st.number_input("ME Cylinder Oil 40 TBN - Received", min_value=0.0, step=0.01)
        me_cylinder_oil_40_rob = st.number_input("ME Cylinder Oil 40 TBN - ROB", min_value=0.0, step=0.01)
    with col2:
        me_cylinder_oil_50_prev_rob = st.number_input("ME Cylinder Oil 50 TBN - Prev. ROB", min_value=0.0, step=0.01)
        me_cylinder_oil_50_cons = st.number_input("ME Cylinder Oil 50 TBN - Cons", min_value=0.0, step=0.01)
        me_cylinder_oil_50_received = st.number_input("ME Cylinder Oil 50 TBN - Received", min_value=0.0, step=0.01)
        me_cylinder_oil_50_rob = st.number_input("ME Cylinder Oil 50 TBN - ROB", min_value=0.0, step=0.01)
    with col3:
        me_cylinder_oil_70_prev_rob = st.number_input("ME Cylinder Oil 70 TBN - Prev. ROB", min_value=0.0, step=0.01)
        me_cylinder_oil_70_cons = st.number_input("ME Cylinder Oil 70 TBN - Cons", min_value=0.0, step=0.01)
        me_cylinder_oil_70_received = st.number_input("ME Cylinder Oil 70 TBN - Received", min_value=0.0, step=0.01)
        me_cylinder_oil_70_rob = st.number_input("ME Cylinder Oil 70 TBN - ROB", min_value=0.0, step=0.01)
    with col1:
        me_cylinder_oil_100_prev_rob = st.number_input("ME Cylinder Oil 100 TBN - Prev. ROB", min_value=0.0, step=0.01)
        me_cylinder_oil_100_cons = st.number_input("ME Cylinder Oil 100 TBN - Cons", min_value=0.0, step=0.01)
        me_cylinder_oil_100_received = st.number_input("ME Cylinder Oil 100 TBN - Received", min_value=0.0, step=0.01)
        me_cylinder_oil_100_rob = st.number_input("ME Cylinder Oil 100 TBN - ROB", min_value=0.0, step=0.01)
    with col2:
        me_mt_system_oil_prev_rob = st.number_input("ME/MT System Oil - Prev. ROB", min_value=0.0, step=0.01)
        me_mt_system_oil_cons = st.number_input("ME/MT System Oil - Cons", min_value=0.0, step=0.01)
        me_mt_system_oil_received = st.number_input("ME/MT System Oil - Received", min_value=0.0, step=0.01)
        me_mt_system_oil_rob = st.number_input("ME/MT System Oil - ROB", min_value=0.0, step=0.01)
    with col3:
        ae_system_oil_prev_rob = st.number_input("AE System Oil - Prev. ROB", min_value=0.0, step=0.01)
        ae_system_oil_cons = st.number_input("AE System Oil - Cons", min_value=0.0, step=0.01)
        ae_system_oil_received = st.number_input("AE System Oil - Received", min_value=0.0, step=0.01)
        ae_system_oil_rob = st.number_input("AE System Oil - ROB", min_value=0.0, step=0.01)
    with col1:
        ae_system_oil_15_prev_rob = st.number_input("AE System Oil 15TBN - Prev. ROB", min_value=0.0, step=0.01)
        ae_system_oil_15_cons = st.number_input("AE System Oil 15TBN - Cons", min_value=0.0, step=0.01)
        ae_system_oil_15_received = st.number_input("AE System Oil 15TBN - Received", min_value=0.0, step=0.01)
        ae_system_oil_15_rob = st.number_input("AE System Oil 15TBN - ROB", min_value=0.0, step=0.01)
    with col2:
        tg_system_oil_prev_rob = st.number_input("T/O System Oil - Prev. ROB", min_value=0.0, step=0.01)
        tg_system_oil_cons = st.number_input("T/O System Oil - Cons", min_value=0.0, step=0.01)
        tg_system_oil_received = st.number_input("T/O System Oil - Received", min_value=0.0, step=0.01)
        tg_system_oil_rob = st.number_input("T/O System Oil - ROB", min_value=0.0, step=0.01)

# Operations Tab
with tabs[1]:
    st.header("Operations")
    
    st.subheader("Cargo Operations")
    no_cargo_operations = st.checkbox("No Cargo Operations in this port")
    cargo_operation_cargo = st.text_input("Cargo Operations - Cargo")
    cargo_operation_is_critical = st.checkbox("Cargo Operations - Is Critical")
    cargo_operation_qty = st.number_input("Cargo Operations - Qty (MT)", min_value=0.0, step=0.01)
    cargo_operation_vapour_qty = st.number_input("Cargo Operations - Vapour Qty (MT)", min_value=0.0, step=0.01)
    cargo_operation_oil_major_cargo = st.text_input("Cargo Operations - Oil Major Cargo")
    cargo_operation_oil_major = st.text_input("Cargo Operations - Oil Major")
    cargo_operation_basis_final_qty = st.text_input("Cargo Operations - Basis of Final Qty")
    cargo_operation_btb_transfer = st.text_input("Cargo Operations - BTB Transfer Y/N")
    cargo_operation_commenced_date = st.date_input("Cargo Operations - Commenced Date", datetime.now().date())
    cargo_operation_commenced_time = st.time_input("Cargo Operations - Commenced Time", datetime.now().time())
    cargo_operation_completed_date = st.date_input("Cargo Operations - Completed Date", datetime.now().date())
    cargo_operation_completed_time = st.time_input("Cargo Operations - Completed Time", datetime.now().time())
    cargo_operation_action = st.text_input("Cargo Operations - Action")
    
    st.subheader("Ballasting / Deballasting")
    ballasting_commenced_date = st.date_input("Ballasting - Commenced Date", datetime.now().date())
    ballasting_commenced_time = st.time_input("Ballasting - Commenced Time", datetime.now().time())
    ballasting_completed_date = st.date_input("Ballasting - Completed Date", datetime.now().date())
    ballasting_completed_time = st.time_input("Ballasting - Completed Time", datetime.now().time())
    ballasting_quantity = st.number_input("Ballasting - Quantity (MT)", min_value=0.0, step=0.01)
    deballasting_commenced_date = st.date_input("Deballasting - Commenced Date", datetime.now().date())
    deballasting_commenced_time = st.time_input("Deballasting - Commenced Time", datetime.now().time())
    deballasting_completed_date = st.date_input("Deballasting - Completed Date", datetime.now().date())
    deballasting_completed_time = st.time_input("Deballasting - Completed Time", datetime.now().time())
    deballasting_quantity = st.number_input("Deballasting - Quantity (MT)", min_value=0.0, step=0.01)
    
    st.subheader("Tank Cleaning")
    hold_tank_cleaning = st.checkbox("Tank Cleaning - Hold / Tank Cleaning")
    hold_tank_cleaning_commenced_date = st.date_input("Tank Cleaning - Commenced Date", datetime.now().date())
    hold_tank_cleaning_commenced_time = st.time_input("Tank Cleaning - Commenced Time", datetime.now().time())
    hold_tank_cleaning_completed_date = st.date_input("Tank Cleaning - Completed Date", datetime.now().date())
    hold_tank_cleaning_completed_time = st.time_input("Tank Cleaning - Completed Time", datetime.now().time())
    stripping_draining = st.checkbox("Tank Cleaning - Stripping / Draining")
    stripping_draining_remarks = st.text_area("Tank Cleaning - Stripping / Draining Remarks")
    
    st.subheader("Other Operations")
    other_operations_description = st.text_area("Other Operations - Description")
    other_operations_commenced_date = st.date_input("Other Operations - Commenced Date", datetime.now().date())
    other_operations_commenced_time = st.time_input("Other Operations - Commenced Time", datetime.now().time())
    other_operations_completed_date = st.date_input("Other Operations - Completed Date", datetime.now().date())
    other_operations_completed_time = st.time_input("Other Operations - Completed Time", datetime.now().time())
    other_operations_action = st.text_input("Other Operations - Action")

# Emissions in Port Tab
with tabs[2]:
    st.header("Emissions in Port")
    vessel_name = st.text_input("Emissions - Vessel Name")
    voyage_no_emission = st.text_input("Emissions - Voyage No")
    port_emission = st.text_input("Emissions - Port")
    ballast_laden_emission = st.checkbox("Emissions - Ballast/Laden")
    eu_port = st.checkbox("Emissions - EU Port")
    
    col1, col2 = st.columns(2)
    with col1:
        arrival_date = st.date_input("Emissions - Arrival Date", datetime.now().date())
        arrival_time = st.time_input("Emissions - Arrival Time", datetime.now().time())
    with col2:
        departure_date = st.date_input("Emissions - Departure Date", datetime.now().date())
        departure_time = st.time_input("Emissions - Departure Time", datetime.now().time())
    
    total_time_in_port = st.number_input("Emissions - Total Time in Port (hrs)", min_value=0.0, step=0.01)
    total_aggregated_co2_emitted = st.number_input("Emissions - Total Aggregated CO2 Emitted (T CO2)", min_value=0.0, step=0.01)
    
    st.subheader("Consumption (Emission in Port)")
    col1, col2 = st.columns(2)
    with col1:
        fuel_type = st.text_input("Emissions - Fuel Type")
        emission_factor = st.number_input("Emissions - Emission Factor", min_value=0.0, step=0.01)
        rob_at_fwe = st.number_input("Emissions - ROB @ FWE", min_value=0.0, step=0.01)
        bunkered = st.number_input("Emissions - Bunkered", min_value=0.0, step=0.01)
    with col2:
        rob_at_swe = st.number_input("Emissions - ROB @ SWE", min_value=0.0, step=0.01)
        total_fo_cons = st.number_input("Emissions - Total FO Cons", min_value=0.0, step=0.01)
        cargo_heating_cons = st.number_input("Emissions - Cargo Heating Cons", min_value=0.0, step=0.01)
        aggregated_co2_emitted = st.number_input("Emissions - Aggregated CO2 Emitted (MT CO2)", min_value=0.0, step=0.01)

if st.button("Submit"):
    st.write("Form submitted successfully!")
