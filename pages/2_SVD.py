import streamlit as st
import pandas as pd

def create_standardised_vessel_dataset_table():
    # Data for the table
    data = [
        {"IMO Data Number": "IMO0597", "Data Element": "Event type, coded", "ISO Universal ID": "jsmea_voy/VoyageInformation/EventType"},
        {"IMO Data Number": "IMO0598", "Data Element": "Operation type, coded", "ISO Universal ID": "jsmea_voy/VoyageInformation/OperationType"},
        {"IMO Data Number": "IMO0599", "Data Element": "Operation, description", "ISO Universal ID": "jsmea_voy/VoyageInformation/OperationType/Remarks"},
        {"IMO Data Number": "IMO0600", "Data Element": "Elapsed Time", "ISO Universal ID": "jsmea_voy/DateAndTime/ElapsedTime"},
        {"IMO Data Number": "IMO0601", "Data Element": "Ship position when reporting, latitude", "ISO Universal ID": "jsmea_voy/ShipPosition/LAT"},
        {"IMO Data Number": "IMO0602", "Data Element": "Ship position when reporting, longitude", "ISO Universal ID": "jsmea_voy/ShipPosition/LON"},
        {"IMO Data Number": "IMO0603", "Data Element": "Ship reporting date time", "ISO Universal ID": "jsmea_voy/DateAndTime"},
        {"IMO Data Number": "IMO0142", "Data Element": "Ship name", "ISO Universal ID": "jsmea_nav/ShipInformation/ShipName"},
        {"IMO Data Number": "IMO0140", "Data Element": "Ship IMO Number", "ISO Universal ID": "jsmea_nav/ShipInformation/IMONumber"},
        {"IMO Data Number": "IMO0326", "Data Element": "Ship MMSI number", "ISO Universal ID": "jsmea_nav/ShipInformation/MMSINumber"},
        {"IMO Data Number": "IMO0160", "Data Element": "Ship type, coded", "ISO Universal ID": "jsmea_nav/ShipInformation/ShipType"},
        {"IMO Data Number": "IMO0086", "Data Element": "Number of crew", "ISO Universal ID": "jsmea_voy/VoyageInformation/CrewList"},
        {"IMO Data Number": "IMO0191", "Data Element": "Voyage number", "ISO Universal ID": "jsmea_voy/VoyageInformation/VoyageNumber"},
        {"IMO Data Number": "IMO0604", "Data Element": "Voyage remarks", "ISO Universal ID": "jsmea_voy/VoyageInformation/Remarks"},
        {"IMO Data Number": "IMO0605", "Data Element": "Voyage leg identifier", "ISO Universal ID": "jsmea_voy/VoyageInformation/LEG"},
        {"IMO Data Number": "IMO0606", "Data Element": "Voyage leg remarks", "ISO Universal ID": "jsmea_voy/VoyageInformation/LEG/Remarks"},
        {"IMO Data Number": "IMO0111", "Data Element": "Port of departure, coded", "ISO Universal ID": "jsmea_voy/PortInformation/Departure/PortCode"},
        {"IMO Data Number": "IMO0112", "Data Element": "Port of departure, name", "ISO Universal ID": "jsmea_voy/PortInformation/Departure/PortName"},
        {"IMO Data Number": "IMO0108", "Data Element": "Port of arrival, coded", "ISO Universal ID": "jsmea_voy/PortInformation/Arrival/PortCode"},
        {"IMO Data Number": "IMO0109", "Data Element": "Port of arrival, name", "ISO Universal ID": "jsmea_voy/PortInformation/Arrival/PortName"},
        {"IMO Data Number": "IMO0231", "Data Element": "Pilot boarding place name", "ISO Universal ID": "jsmea_voy/PortInformation/Arrival/PBP/Name"},
        {"IMO Data Number": "XMO1111", "Data Element": "Pilot boarding place location", "ISO Universal ID": "jsmea_voy/PortInformation/Arrival/PBP/Location"},
        {"IMO Data Number": "IMO0232", "Data Element": "Berth name", "ISO Universal ID": "jsmea_voy/PortInformation/Arrival/BerthName"},
        {"IMO Data Number": "IMO0541", "Data Element": "Date and time to location in port - estimated", "ISO Universal ID": "jsmea_voy/PortInformation/Arrival/ETA"},
        {"IMO Data Number": "IMO0540", "Data Element": "Date and time to location in port - actual", "ISO Universal ID": "jsmea_voy/PortInformation/Arrival/DateAndTime"},
        {"IMO Data Number": "XMO2222", "Data Element": "Date and time to Pilot Boarding Place - estimated", "ISO Universal ID": "jsmea_voy/PortInformation/Arrival/PBP/ETA"},
        {"IMO Data Number": "XMO3333", "Data Element": "Date and time to Pilot Boarding Place - actual", "ISO Universal ID": "jsmea_voy/PortInformation/Arrival/PBP/DateAndTime"},
        {"IMO Data Number": "XMO4444", "Data Element": "Date and time to VTS - estimated", "ISO Universal ID": "jsmea_voy/PortInformation/Arrival/VTS/ETA"},
        {"IMO Data Number": "XMO5555", "Data Element": "Date and time to VTS - actual", "ISO Universal ID": "jsmea_voy/PortInformation/Arrival/VTS/DateAndTime"},
        {"IMO Data Number": "IMO0518", "Data Element": "Date and time of arrival at next port of call - estimated", "ISO Universal ID": "jsmea_voy/DistanceAndTime/NextPort/DateAndTime"},
        {"IMO Data Number": "XMO6666", "Data Element": "Voyage Time", "ISO Universal ID": "jsmea_voy/DistanceAndTime/VoyageTime"},
        {"IMO Data Number": "IMO0607", "Data Element": "Reason for ship deviation from planned voyage description", "ISO Universal ID": "jsmea_voy/VoyageInformation/ShipDeviation/Remarks"},
        {"IMO Data Number": "IMO0608", "Data Element": "Ship position deviation, latitude", "ISO Universal ID": "jsmea_voy/VoyageInformation/ShipDeviation/LAT"},
        {"IMO Data Number": "IMO0609", "Data Element": "Ship position deviation, longitude", "ISO Universal ID": "jsmea_voy/VoyageInformation/ShipDeviation/LON"},
        {"IMO Data Number": "IMO0610", "Data Element": "Ship deviation start date time", "ISO Universal ID": "jsmea_voy/VoyageInformation/ShipDeviation/Start/DateAndTime"},
        {"IMO Data Number": "IMO0611", "Data Element": "Ship deviation stop date time", "ISO Universal ID": "jsmea_voy/VoyageInformation/ShipDeviation/End/DateAndTime"},
        {"IMO Data Number": "IMO0612", "Data Element": "Distance through water", "ISO Universal ID": "jsmea_voy/DistanceAndTime/ThroughWater/Distance"},
        {"IMO Data Number": "IMO0613", "Data Element": "Distance over ground", "ISO Universal ID": "jsmea_voy/DistanceAndTime/OverGround/Distance"},
        {"IMO Data Number": "IMO0614", "Data Element": "Distance sailed in ice", "ISO Universal ID": "jsmea_voy/DistanceAndTime/ThroughIce/Distance"},
        {"IMO Data Number": "IMO0615", "Data Element": "Distance to next port", "ISO Universal ID": "jsmea_voy/DistanceAndTime/NextPort/Distance"},
        {"IMO Data Number": "XMO7777", "Data Element": "Distance to next waypoint", "ISO Universal ID": "jsmea_voy/DistanceAndTime/NextWaypoint/Distance"},
        {"IMO Data Number": "IMO0333", "Data Element": "Speed over ground", "ISO Universal ID": "jsmea_voy/ShipSpeed/SOG"},
        {"IMO Data Number": "IMO0616", "Data Element": "Speed through water", "ISO Universal ID": "jsmea_voy/ShipSpeed/STW"},
        {"IMO Data Number": "IMO0617", "Data Element": "Speed propeller", "ISO Universal ID": "jsmea_voy/VoyageInformation/PropellerRPM"},
        {"IMO Data Number": "IMO0618", "Data Element": "Speed projected", "ISO Universal ID": "jsmea_voy/ShipSpeed/Projected"},
        {"IMO Data Number": "IMO0619", "Data Element": "Speed order", "ISO Universal ID": "jsmea_voy/ShipSpeed/Ordered"},
        {"IMO Data Number": "XMO8888", "Data Element": "Slip", "ISO Universal ID": "jsmea_voy/VoyageInformation/Slip"},
        {"IMO Data Number": "IMO0332", "Data Element": "Course, over ground", "ISO Universal ID": "jsmea_voy/VoyageInformation/Course"},
        {"IMO Data Number": "IMO0620", "Data Element": "Ship true heading", "ISO Universal ID": "jsmea_voy/VoyageInformation/Heading"},
        {"IMO Data Number": "IMO0357", "Data Element": "Ship draught", "ISO Universal ID": "jsmea_voy/DeadweightMeasurement/Draft"},
        {"IMO Data Number": "IMO0621", "Data Element": "Draught Forward", "ISO Universal ID": "jsmea_voy/DeadweightMeasurement/DraftFore"},
        {"IMO Data Number": "IMO0622", "Data Element": "Draught Aft", "ISO Universal ID": "jsmea_voy/DeadweightMeasurement/DraftAft"},
        {"IMO Data Number": "IMO0376", "Data Element": "Ship actual deadweight tonnage", "ISO Universal ID": "jsmea_voy/DeadweightMeasurement/DWT"},
        {"IMO Data Number": "IMO0452", "Data Element": "Total ballast water onboard", "ISO Universal ID": "jsmea_mac/BallastSystem/BallastWater/Volume"},
        {"IMO Data Number": "IMO0358", "Data Element": "Weather remarks", "ISO Universal ID": "jsmea_wea/WeatherCondition/Remarks"},
        {"IMO Data Number": "IMO0623", "Data Element": "Bad weather hours", "ISO Universal ID": "jsmea_wea/WeatherCondition/BadWeather/Hours"},
        {"IMO Data Number": "IMO0624", "Data Element": "Bad weather distance", "ISO Universal ID": "jsmea_wea/WeatherCondition/BadWeather/Distance"},
        {"IMO Data Number": "IMO0625", "Data Element": "Wind force", "ISO Universal ID": "jsmea_wea/WeatherCondition/Wind/BeaufortScale"},
        {"IMO Data Number": "IMO0359", "Data Element": "Wind speed, coded", "ISO Universal ID": "jsmea_wea/WeatherCondition/Wind/Speed"},
        {"IMO Data Number": "IMO0360", "Data Element": "Wind direction, coded", "ISO Universal ID": "jsmea_wea/WeatherCondition/Wind/Direction"},
        {"IMO Data Number": "IMO0626", "Data Element": "Wind direction, estimated, relative", "ISO Universal ID": "jsmea_wea/WeatherCondition/Wind/Direction/Relative"},
        {"IMO Data Number": "IMO0627", "Data Element": "Wind direction, estimated, true", "ISO Universal ID": "jsmea_wea/WeatherCondition/Wind/Direction/TrueBearing"},
        {"IMO Data Number": "IMO0628", "Data Element": "Air temperature", "ISO Universal ID": "jsmea_wea/WeatherCondition/Temp"},
        {"IMO Data Number": "IMO0629", "Data Element": "Atmospheric pressure", "ISO Universal ID": "jsmea_wea/WeatherCondition/AtmosphericPressure"},
        {"IMO Data Number": "IMO0363", "Data Element": "State of the sea, coded", "ISO Universal ID": "jsmea_wea/SeaState"},
        {"IMO Data Number": "IMO0630", "Data Element": "Sea direction, relative", "ISO Universal ID": "jsmea_wea/SeaState/Direction/Relative"},
        {"IMO Data Number": "IMO0631", "Data Element": "Sea direction, true", "ISO Universal ID": "jsmea_wea/SeaState/Direction/TrueBearing"},
        {"IMO Data Number": "IMO0632", "Data Element": "Sea height", "ISO Universal ID": "jsmea_wea/SeaState/Height"},
        {"IMO Data Number": "IMO0633", "Data Element": "Swell direction, relative", "ISO Universal ID": "jsmea_wea/SeaState/Swell/Direction/Relative"},
        {"IMO Data Number": "IMO0634", "Data Element": "Swell direction, true", "ISO Universal ID": "jsmea_wea/SeaState/Swell/Direction/TrueBearing"},
        {"IMO Data Number": "IMO0635", "Data Element": "Swell height", "ISO Universal ID": "jsmea_wea/SeaState/Swell/Height"},
        {"IMO Data Number": "IMO0636", "Data Element": "Ocean current direction, relative", "ISO Universal ID": "jsmea_wea/SeaState/Current/Direction/Relative"},
        {"IMO Data Number": "IMO0637", "Data Element": "Ocean current direction, true", "ISO Universal ID": "jsmea_wea/SeaState/Current/Direction/TrueBearing"},
        {"IMO Data Number": "IMO0638", "Data Element": "Ocean current direction, weather provider", "ISO Universal ID": "jsmea_wea/SeaState/Current/Direction/WeatherProvider"},
        {"IMO Data Number": "IMO0639", "Data Element": "Fresh water bunkered", "ISO Universal ID": "jsmea_voy/RetentionOfWaterOnBoard/FreshWater/Bunkered"},
        {"IMO Data Number": "IMO0640", "Data Element": "Fresh water produced", "ISO Universal ID": "jsmea_voy/RetentionOfWaterOnBoard/FreshWater/Produced"},
        {"IMO Data Number": "IMO0641", "Data Element": "Fresh water consumed", "ISO Universal ID": "jsmea_voy/RetentionOfWaterOnBoard/FreshWater/Consumed"},
        {"IMO Data Number": "IMO0642", "Data Element": "Technical water produced", "ISO Universal ID": "jsmea_voy/RetentionOfWaterOnBoard/TechnicalWater/Produced"},
        {"IMO Data Number": "IMO0643", "Data Element": "Technical water consumed", "ISO Universal ID": "jsmea_voy/RetentionOfWaterOnBoard/TechnicalWater/Consumed"},
        {"IMO Data Number": "IMO0644", "Data Element": "Wash water consumed", "ISO Universal ID": "jsmea_voy/RetentionOfWaterOnBoard/WashWater/Consumed"},
        {"IMO Data Number": "IMO0645", "Data Element": "Fresh water remaining on board", "ISO Universal ID": "jsmea_voy/RetentionOfWaterOnBoard/FreshWater/ROB"},
        {"IMO Data Number": "IMO0646", "Data Element": "Boiler electricity consumption", "ISO Universal ID": "jsema_mac/BoilerWaterSystem/Power/Consumed"},
        {"IMO Data Number": "IMO0647", "Data Element": "Generator production", "ISO Universal ID": "jsmea_mac/DiesselGeneratorSet/Power/Produced"},
        {"IMO Data Number": "IMO0648", "Data Element": "Offset electricity consumption", "ISO Universal ID": "jsmea_voy/OffsetElectricity/Consumed"},
        {"IMO Data Number": "IMO0649", "Data Element": "Power consumption for plant", "ISO Universal ID": "jsmea_mac/ReLiquefiedSystem/Power/Consumed"},
        {"IMO Data Number": "IMO0022", "Data Element": "Cargo item description of goods", "ISO Universal ID": "jsmea_voy/CargoLoading/CargoLoad/Remarks"},
        {"IMO Data Number": "IMO0024", "Data Element": "Cargo item gross weight", "ISO Universal ID": "jsmea_voy/CargoLoading/CargoLoad/Mass"},
        {"IMO Data Number": "IMO0023", "Data Element": "Cargo item gross volume", "ISO Universal ID": "jsmea_voy/CargoLoading/CargoLoad/Volume"},
        {"IMO Data Number": "IMO0650", "Data Element": "Total number of containers, TEU", "ISO Universal ID": "jsmea_voy/CargoLoading/CargoLoad/TEU"},
        {"IMO Data Number": "IMO0651", "Data Element": "Total number of full containers, TEU", "ISO Universal ID": "jsmea_voy/CargoLoading/CargoLoad/TEU/Full"},
        {"IMO Data Number": "IMO0652", "Data Element": "Total number of full reefer containers, TEU", "ISO Universal ID": "jsmea_voy/CargoLoading/CargoLoad/TEU/Reefer"},
        {"IMO Data Number": "IMO0653", "Data Element": "Total number of vehicles onboard, CEU", "ISO Universal ID": "jsmea_voy/CargoLoading/CargoLoad/CEU"},
        {"IMO Data Number": "IMO0654", "Data Element": "Fuel type, coded", "ISO Universal ID": "jsmea_voy/Bunkered/FuelType"},
        {"IMO Data Number": "IMO0655", "Data Element": "Bunker Delivery Note number", "ISO Universal ID": "jsmea_voy/Bunkered/BDN/Number"},
        {"IMO Data Number": "IMO0656", "Data Element": "Bunker delivery date and time", "ISO Universal ID": "jsmea_voy/Bunkered/BDN/DateAndTime"},
        {"IMO Data Number": "IMO0657", "Data Element": "Fuel bunker received", "ISO Universal ID": "jsmea_voy/Bunkered/BDN/TotalReceived"},
        {"IMO Data Number": "IMO0658", "Data Element": "Fuel, mass", "ISO Universal ID": "jsmea_voy/Bunkered/FuelType/Mass"},
        {"IMO Data Number": "IMO0659", "Data Element": "Fuel, density", "ISO Universal ID": "jsmea_voy/Bunkered/FuelType/Density"},
        {"IMO Data Number": "IMO0660", "Data Element": "Fuel, sulphur content", "ISO Universal ID": "jsmea_voy/Bunkered/FuelType/SulphurContent"},
        {"IMO Data Number": "IMO0661", "Data Element": "Fuel, viscosity", "ISO Universal ID": "jsmea_voy/Bunkered/FuelType/Viscosity"},
        {"IMO Data Number": "IMO0662", "Data Element": "Fuel, water content", "ISO Universal ID": "jsmea_voy/Bunkered/FuelType/WaterContent"},
        {"IMO Data Number": "IMO0663", "Data Element": "Fuel, higher heating value", "ISO Universal ID": "jsmea_voy/Bunkered/FuelType/HighCalorificValue"},
        {"IMO Data Number": "IMO0664", "Data Element": "Fuel, lower heating value", "ISO Universal ID": "jsmea_voy/Bunkered/FuelType/LowCalorificValue"},
        {"IMO Data Number": "IMO0665", "Data Element": "Fuel, grade", "ISO Universal ID": "jsmea_voy/Bunkered/FuelType/Grade"},
        {"IMO Data Number": "IMO0666", "Data Element": "Fuel, bunker port, coded", "ISO Universal ID": "jsmea_voy/Bunkered/BDN/PortCode"},
        {"IMO Data Number": "IMO0667", "Data Element": "Fuel, bunker port, name", "ISO Universal ID": "jsmea_voy/Bunkered/BDN/PortName"},
        {"IMO Data Number": "IMO0668", "Data Element": "Fuel Carbon Dioxide emission", "ISO Universal ID": "jsmea_voy/Bunkered/FuelType/CO2"},
        {"IMO Data Number": "IMO0669", "Data Element": "Total fuel quantity consumed", "ISO Universal ID": "jsmea_voy/Consumption/FuelType/Consumed"},
        {"IMO Data Number": "IMO0670", "Data Element": "Fuel consumed, by M/E", "ISO Universal ID": "jsmea_voy/Consumption/FuelType/Consumed/MainEngine"},
        {"IMO Data Number": "IMO0671", "Data Element": "Fuel consumed, by D/E", "ISO Universal ID": "jsmea_voy/Consumption/FuelType/Consumed/DieselElectricPropulsionSet"},
        {"IMO Data Number": "IMO0672", "Data Element": "Fuel consumed, by D/G", "ISO Universal ID": "jsmea_voy/Consumption/FuelType/Consumed/DieselGeneratorSet"},
        {"IMO Data Number": "IMO0673", "Data Element": "Fuel consumed, by Auxiliary Boiler", "ISO Universal ID": "jsmea_voy/Consumption/FuelType/Consumed/AuxBoiler"},
        {"IMO Data Number": "IMO0674", "Data Element": "Fuel quantity remaining on board", "ISO Universal ID": "jsmea_voy/RetentionOfOilOnBoard/FuelType/Mass"},
        {"IMO Data Number": "IMO0675", "Data Element": "Sludge remaining on board", "ISO Universal ID": "jsmea_voy/RetentionOfOilOnBoard/Sludge/Mass"},
        {"IMO Data Number": "IMO0676", "Data Element": "Cylinder lube oil remaining on board", "ISO Universal ID": "jsmea_voy/RetentionOfOilOnBoard/LubOil/Mass"},
        {"IMO Data Number": "IMO0677", "Data Element": "Cylinder lube oil, feed rate", "ISO Universal ID": "jsmea_oil/LubOil/FeedRate"},
        {"IMO Data Number": "IMO0678", "Data Element": "Cylinder lube oil, consumption", "ISO Universal ID": "jsmea_oil/LubOil/MainEngine/Consumed"},
        {"IMO Data Number": "IMO0679", "Data Element": "Cylinder lube oil, received", "ISO Universal ID": "jsmea_voy/Bunkered/LubOil/Mass"},
    ]

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Streamlit app
    st.title("Standardised Vessel Dataset")

    # Add a search box
    search_term = st.text_input("Search for a Data Element or IMO Data Number:")

    # Filter the dataframe based on the search term
    if search_term:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

    # Display the table
    st.dataframe(df, use_container_width=True)

    # Add a download button for the CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="standardised_vessel_dataset.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    create_standardised_vessel_dataset_table()
