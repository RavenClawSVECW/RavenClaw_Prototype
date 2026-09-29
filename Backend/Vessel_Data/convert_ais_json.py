import pandas as pd
import glob
import json
import os


# ==========================================
# 1. FIND AIS CSV
# ==========================================

csv_files = glob.glob("AIS_*.csv")

if not csv_files:
    print("ERROR: AIS CSV file not found.")
    print("Make sure your AIS CSV is in the same folder.")
    exit()

csv_file = csv_files[0]

print("Reading:", csv_file)


# ==========================================
# 2. LOAD AIS DATA
# ==========================================

ais = pd.read_csv(csv_file)

print("AIS Records:", len(ais))
print("Unique Vessels:", ais["MMSI"].nunique())


# ==========================================
# 3. CHECK REQUIRED COLUMNS
# ==========================================

required_columns = [
    "MMSI",
    "BaseDateTime",
    "LAT",
    "LON",
    "SOG",
    "COG",
    "VesselName",
    "VesselType"
]

missing_columns = [
    col for col in required_columns
    if col not in ais.columns
]

if missing_columns:
    print("\nERROR: Missing columns:")
    for col in missing_columns:
        print(" -", col)
    exit()


# ==========================================
# 4. SORT AIS DATA
# ==========================================

ais["BaseDateTime"] = pd.to_datetime(
    ais["BaseDateTime"],
    utc=True
)

ais = ais.sort_values(
    ["MMSI", "BaseDateTime"]
)


# ==========================================
# 5. READ OIL SPILL INFORMATION
# ==========================================

if not os.path.exists("spill_input.json"):
    print("ERROR: spill_input.json not found.")
    exit()

with open(
    "spill_input.json",
    "r",
    encoding="utf-8"
) as file:

    spill = json.load(file)


# ==========================================
# 6. CREATE OIL SPILL JSON
# ==========================================

oilspill = {
    "spill_id": spill["spill_id"],
    "latitude": spill["latitude"],
    "longitude": spill["longitude"],
    "detection_time": spill["detection_time"],
    "estimated_age_hours": spill["estimated_age_hours"]
}


with open(
    "oilspill.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        oilspill,
        file,
        indent=2
    )


print("\nCreated: oilspill.json")


# ==========================================
# 7. VESSEL TYPE CONVERSION
# ==========================================

vessel_types = {

    20: "Wing In Ground",

    30: "Fishing Vessel",

    31: "Towing",
    32: "Towing",

    33: "Dredging",
    34: "Diving Operations",
    35: "Military Operations",

    36: "Sailing",
    37: "Pleasure Craft",

    40: "High Speed Craft",

    50: "Pilot Vessel",
    51: "Search and Rescue",
    52: "Tug",
    53: "Port Tender",
    54: "Anti Pollution",
    55: "Law Enforcement",
    56: "Spare",
    57: "Spare",
    58: "Medical Transport",
    59: "Noncombatant Ship",

    60: "Passenger",
    61: "Passenger",
    62: "Passenger",
    63: "Passenger",
    64: "Passenger",
    65: "Passenger",
    66: "Passenger",
    67: "Passenger",
    68: "Passenger",
    69: "Passenger",

    70: "Cargo",
    71: "Cargo",
    72: "Cargo",
    73: "Cargo",
    74: "Cargo",
    75: "Cargo",
    76: "Cargo",
    77: "Cargo",
    78: "Cargo",
    79: "Cargo",

    80: "Tanker",
    81: "Tanker",
    82: "Tanker",
    83: "Tanker",
    84: "Tanker",
    85: "Tanker",
    86: "Tanker",
    87: "Tanker",
    88: "Tanker",
    89: "Tanker",

    90: "Other",
    91: "Other",
    92: "Other",
    93: "Other",
    94: "Other",
    95: "Other",
    96: "Other",
    97: "Other",
    98: "Other",
    99: "Other"
}


# ==========================================
# 8. CREATE VESSEL DATA
# ==========================================

vessels = []


for mmsi, group in ais.groupby("MMSI"):

    first = group.iloc[0]


    # --------------------------------------
    # Vessel Type
    # --------------------------------------

    vessel_type_code = (
        int(first["VesselType"])
        if pd.notna(first["VesselType"])
        else None
    )

    vessel_type = vessel_types.get(
        vessel_type_code,
        "Unknown"
    )


    # --------------------------------------
    # Vessel Name
    # --------------------------------------

    vessel_name = (
        str(first["VesselName"])
        if pd.notna(first["VesselName"])
        else "Unknown"
    )


    # --------------------------------------
    # Vessel ID
    # --------------------------------------

    try:
        vessel_id = str(int(mmsi))
    except:
        vessel_id = str(mmsi)


    vessel = {

        "vessel_id": vessel_id,

        "name": vessel_name,

        "type": vessel_type,

        "trajectory": []
    }


    # ======================================
    # 9. CREATE TRAJECTORY
    # ======================================

    for _, row in group.iterrows():

        # Latitude
        latitude = (
            round(float(row["LAT"]), 6)
            if pd.notna(row["LAT"])
            else None
        )


        # Longitude
        longitude = (
            round(float(row["LON"]), 6)
            if pd.notna(row["LON"])
            else None
        )


        # Speed
        speed = (
            round(float(row["SOG"]), 2)
            if pd.notna(row["SOG"])
            else None
        )


        # Course
        course = (
            round(float(row["COG"]), 2)
            if pd.notna(row["COG"])
            else None
        )


        # Timestamp
        timestamp = (
            row["BaseDateTime"].strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        )


        point = {

            "latitude": latitude,

            "longitude": longitude,

            "speed": speed,

            "course": course,

            "timestamp": timestamp
        }


        vessel["trajectory"].append(point)


    vessels.append(vessel)


# ==========================================
# 10. CREATE VESSELS JSON
# ==========================================

vessels_output = {

    "vessels": vessels

}


with open(
    "vessels2.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        vessels_output,
        file,
        indent=2
    )


print("Created: vessels2.json")


# ==========================================
# 11. FINAL SUMMARY
# ==========================================

print("\n==========================================")
print("       JSON FILES CREATED SUCCESSFULLY")
print("==========================================")

print("\nFiles:")

print("1. oilspill.json")
print("2. vessels2.json")

print("\nAIS Records:", len(ais))

print(
    "Unique Vessels:",
    ais["MMSI"].nunique()
)

print("\nLocation:")
print(
    "oilspill.json ->",
    os.path.abspath("oilspill.json")
)

print(
    "vessels2.json ->",
    os.path.abspath("vessels2.json")
)

print("\nReady for dashboard integration!")