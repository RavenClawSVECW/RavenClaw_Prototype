import json
import pandas as pd
import glob
import math


# ==========================================
# 1. LOAD SPILL INFORMATION
# ==========================================

with open("spill_input.json", "r") as file:
    spill = json.load(file)

spill_lat = spill["latitude"]
spill_lon = spill["longitude"]

detection_time = pd.to_datetime(
    spill["detection_time"],
    utc=True
)


# ==========================================
# 2. LOAD AIS DATA
# ==========================================

csv_files = glob.glob("AIS_*.csv")

if not csv_files:
    print("ERROR: AIS CSV file not found.")
    exit()

csv_file = csv_files[0]

ais = pd.read_csv(csv_file)

ais["BaseDateTime"] = pd.to_datetime(
    ais["BaseDateTime"],
    utc=True
)

ais = ais.sort_values(
    ["MMSI", "BaseDateTime"]
).reset_index(drop=True)


print("==========================================")
print("      MARINE OIL SPILL ANALYSIS")
print("==========================================")

print("\nSpill Location:")
print("Latitude:", spill_lat)
print("Longitude:", spill_lon)
print("Detection Time:", detection_time)

print("\nAIS Records:", len(ais))
print("Unique Vessels:", ais["MMSI"].nunique())


# ==========================================
# 3. DISTANCE FUNCTION
# ==========================================

def distance_km(lat1, lon1, lat2, lon2):

    R = 6371.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


# ==========================================
# 4. CALCULATE DISTANCE FROM SPILL
# ==========================================

ais["Distance_km"] = ais.apply(
    lambda row: distance_km(
        spill_lat,
        spill_lon,
        row["LAT"],
        row["LON"]
    ),
    axis=1
)


# ==========================================
# 5. CALCULATE TIME BEFORE SPILL
# ==========================================

ais["HoursBeforeSpill"] = (
    detection_time - ais["BaseDateTime"]
).dt.total_seconds() / 3600


# Only AIS positions before spill detection

ais = ais[
    ais["HoursBeforeSpill"] >= 0
].copy()


# ==========================================
# 6. ANALYZE EACH VESSEL
# ==========================================

results = []


for (mmsi, name, vessel_type), group in ais.groupby(
    ["MMSI", "VesselName", "VesselType"]
):

    group = group.sort_values("BaseDateTime")

    # --------------------------------------
    # Closest position
    # --------------------------------------

    closest_row = group.loc[
        group["Distance_km"].idxmin()
    ]

    closest_distance = float(
        closest_row["Distance_km"]
    )

    closest_time = closest_row["BaseDateTime"]

    hours_before = (
        detection_time - closest_time
    ).total_seconds() / 3600

    average_distance = float(
        group["Distance_km"].mean()
    )

    record_count = len(group)

    average_speed = float(
        group["SOG"].mean()
    )


    # ======================================
    # 7. CLOSE POSITIONS
    # ======================================

    close_positions = group[
        group["Distance_km"] <= 3
    ]

    close_count = len(close_positions)


    # ======================================
    # 8. MOVEMENT ANALYSIS
    # ======================================

    movement_score = 0

    if len(group) >= 2:

        first_distance = float(
            group.iloc[0]["Distance_km"]
        )

        last_distance = float(
            group.iloc[-1]["Distance_km"]
        )

        # Vessel moved closer to spill

        if last_distance < first_distance:
            movement_score += 20

        # Vessel came very close

        if closest_distance <= 1:
            movement_score += 20

        elif closest_distance <= 3:
            movement_score += 15

        elif closest_distance <= 5:
            movement_score += 10


    # ======================================
    # 9. DISTANCE SCORE
    # ======================================

    distance_score = 100 * math.exp(
        -closest_distance / 5
    )


    # ======================================
    # 10. TIME SCORE
    # ======================================

    time_score = 100 * math.exp(
        -hours_before / 48
    )


    # ======================================
    # 11. PRESENCE SCORE
    # ======================================

    presence_score = min(
        100,
        record_count / 30 * 100
    )


    # ======================================
    # 12. FINAL RISK SCORE
    # ======================================

    risk_score = (
        distance_score * 0.40
        + time_score * 0.30
        + presence_score * 0.10
        + movement_score
    )

    risk_score = min(
        100,
        risk_score
    )


    results.append({

        "MMSI": int(mmsi),

        "VesselName": str(name),

        "VesselType": int(vessel_type),

        "ClosestDistance": closest_distance,

        "AverageDistance": average_distance,

        "HoursBeforeSpill": hours_before,

        "AISRecords": record_count,

        "AverageSpeed": average_speed,

        "ClosestTime": closest_time,

        "ClosePositions": close_count,

        "MovementScore": movement_score,

        "RiskScore": risk_score
    })


# ==========================================
# 13. RANK VESSELS
# ==========================================

ranking = pd.DataFrame(results)

ranking = ranking.sort_values(
    "RiskScore",
    ascending=False
).reset_index(drop=True)


# ==========================================
# 14. DISPLAY RANKING
# ==========================================

print("\n==========================================")
print("       FINAL VESSEL RANKING")
print("==========================================")


for i, row in ranking.iterrows():

    if row["RiskScore"] >= 75:
        level = "HIGH"

    elif row["RiskScore"] >= 50:
        level = "MEDIUM"

    else:
        level = "LOW"

    print(
        f"\n#{i + 1} {row['VesselName']}"
    )

    print(
        f"Risk Score: "
        f"{row['RiskScore']:.2f}/100 ({level})"
    )

    print(
        f"Closest Distance: "
        f"{row['ClosestDistance']:.2f} km"
    )

    print(
        f"Hours Before Spill: "
        f"{row['HoursBeforeSpill']:.2f}"
    )

    print(
        f"AIS Records: "
        f"{row['AISRecords']}"
    )

    print(
        f"Close Positions: "
        f"{row['ClosePositions']}"
    )

    print(
        f"Movement Score: "
        f"{row['MovementScore']}"
    )

    print(
        f"Average Speed: "
        f"{row['AverageSpeed']:.2f} knots"
    )


# ==========================================
# 15. MOST LIKELY CANDIDATE
# ==========================================

best = ranking.iloc[0]

print("\n==========================================")
print("        MOST LIKELY CANDIDATE")
print("==========================================")

print("Vessel:", best["VesselName"])
print("MMSI:", best["MMSI"])
print("Vessel Type:", best["VesselType"])

print(
    "Risk Score:",
    f"{best['RiskScore']:.2f}/100"
)

print(
    "Closest Distance:",
    f"{best['ClosestDistance']:.2f} km"
)

print(
    "Closest AIS Time:",
    best["ClosestTime"]
)

print(
    "Hours Before Spill:",
    f"{best['HoursBeforeSpill']:.2f}"
)

print(
    "Movement Score:",
    best["MovementScore"]
)


# ==========================================
# 16. CREATE DASHBOARD JSON
# ==========================================

candidates = []


for i, row in ranking.iterrows():

    candidates.append({

        "rank": int(i + 1),

        "vessel_id": str(
            int(row["MMSI"])
        ),

        "vessel_name": str(
            row["VesselName"]
        ),

        "vessel_type": str(
            int(row["VesselType"])
        ),

        "risk_score": round(
            float(row["RiskScore"]),
            2
        ),

        "closest_distance_km": round(
            float(row["ClosestDistance"]),
            2
        ),

        "hours_before_spill": round(
            float(row["HoursBeforeSpill"]),
            2
        ),

        "ais_records": int(
            row["AISRecords"]
        ),

        "movement_score": int(
            row["MovementScore"]
        )
    })


candidate_output = {

    "spill_id": spill["spill_id"],

    "spill_location": {

        "latitude": spill_lat,

        "longitude": spill_lon
    },

    "detection_time": spill["detection_time"],

    "candidates": candidates
}


with open(
    "candidate_results.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        candidate_output,
        file,
        indent=2
    )


# ==========================================
# 17. FINAL MESSAGE
# ==========================================

print("\n==========================================")
print("       OUTPUT FILES CREATED")
print("==========================================")

print("candidate_results.json")
print("vessels_output.json")

print("\nAnalysis complete.")