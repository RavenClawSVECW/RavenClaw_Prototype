# 🛢️ Oil Spill Detection & Vessel Source Attribution Dashboard

## 📌 Overview

The **Oil Spill Detection & Vessel Source Attribution Dashboard** is an interactive web-based interface designed to visualize and analyze oil spills using **satellite imagery and AIS vessel tracking data**.

The dashboard brings the complete analysis into one place.

It allows the user to:

* View detected oil spills
* View spill coordinates and boundaries
* View spill area and estimated age
* View the estimated spill origin
* Visualize vessel locations
* Reconstruct historical vessel trajectories
* Compare vessel movements with the spill
* View spatial and temporal analysis
* View vessel association scores
* Rank candidate vessels
* View predicted spill movement
* Generate alerts and response information

### Core idea

```text
Satellite Data
      +
AIS Vessel Data
      ↓
   Analysis
      ↓
Interactive Dashboard
      ↓
Map + Vessel Tracks + Scores + Alerts
```

> **Important:** A vessel association score indicates how strongly the available evidence connects a vessel with the suspected spill origin. It does not, by itself, prove that the vessel caused the spill.

---

# 📑 Table of Contents

1. [System Architecture](#-system-architecture)
2. [Dashboard Architecture](#-dashboard-architecture)
3. [Features](#-features)
4. [Dashboard Workflow](#-dashboard-workflow)
5. [Input Data](#-input-data)
6. [Dashboard Components](#-dashboard-components)
7. [Vessel Trajectory Visualization](#-vessel-trajectory-visualization)
8. [Association Scoring](#-association-scoring)
9. [Output](#-output)
10. [Project Structure](#-project-structure)
11. [Requirements](#-requirements)
12. [Installation](#-installation)
13. [Running the Dashboard](#-running-the-dashboard)
14. [Using the Dashboard](#-using-the-dashboard)
15. [Example Workflow](#-example-workflow)
16. [Troubleshooting](#-troubleshooting)
17. [Future Improvements](#-future-improvements)

---

# 🏗️ System Architecture

The complete system follows this workflow:

```text
                    SATELLITE IMAGE
                          │
                          ▼
                 OIL SPILL DETECTION
                          │
                          ▼
              SPILL BOUNDARY + LOCATION
                          │
                          ▼
            SPILL AREA / AGE / MOVEMENT
                          │
                          ▼
                  ESTIMATED ORIGIN
                          │
                          │
                          ▼
                    AIS DATA
                          │
                          ▼
                CANDIDATE VESSELS
                          │
                          ▼
             TRAJECTORY RECONSTRUCTION
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
           Spatial     Temporal    Direction
           Analysis    Analysis    Analysis
              │           │           │
              └───────────┼───────────┘
                          ▼
                  ASSOCIATION SCORE
                          │
                          ▼
                  VESSEL RANKING
                          │
                          ▼
                 DASHBOARD DISPLAY
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
             MAP       ANALYTICS     ALERTS
```

---

# 🖥️ Dashboard Architecture

The dashboard acts as the **visualization and decision-support layer** of the project.

```text
┌─────────────────────────────────────────────┐
│                  DASHBOARD                  │
├─────────────────────────────────────────────┤
│                                             │
│  Data Input / Upload                        │
│       │                                     │
│       ▼                                     │
│  Data Processing                            │
│       │                                     │
│       ▼                                     │
│  Analysis Results                           │
│       │                                     │
│  ┌────┼─────────┬────────────┐              │
│  ▼    ▼         ▼            ▼              │
│ Map  Spill   Vessels     Analytics          │
│      Info    & Tracks                       │
│  │    │         │            │              │
│  └────┴─────────┴────────────┘              │
│               │                             │
│               ▼                             │
│       Scores + Ranking                      │
│               │                             │
│               ▼                             │
│         Alerts / Report                     │
└─────────────────────────────────────────────┘
```

---

# ✨ Features

## 1. Oil Spill Visualization

The dashboard displays:

* Spill location
* Spill boundary
* Spill area
* Detection date/time
* Estimated spill age
* Estimated movement direction
* Estimated origin

---

## 2. Interactive Map

The map provides a geographical view of the incident.

It can display:

* Oil-spill polygon
* Spill origin
* Vessel positions
* Vessel trajectories
* Predicted spill movement
* Relevant geographic areas

The user can zoom, pan and inspect individual objects.

---

## 3. Vessel Tracking

The dashboard displays AIS vessel information such as:

* MMSI
* Vessel name, if available
* Vessel type
* Latitude
* Longitude
* Speed
* Course
* Timestamp

---

## 4. Historical Vessel Trajectory

Instead of displaying only the current position of a vessel, the dashboard plots its historical movement.

Example:

```text
                       OIL SPILL
                           ●
                          /
                         /
                        ●
                       /
                      ●
                     /
                    ●
                   /
                🚢
```

This helps determine whether the vessel passed through or near the estimated spill origin.

---

## 5. Spatial Analysis

The dashboard can display:

* Minimum distance from spill origin
* Closest approach
* Trajectory proximity
* Whether the vessel entered the origin zone

Example:

```text
Vessel A → 1.8 km
Vessel B → 8.4 km
Vessel C → 22.1 km
```

---

## 6. Temporal Analysis

The dashboard compares vessel timestamps with the estimated spill-release window.

Example:

```text
Estimated release:
04 Sept 08:00–12:00 UTC

Vessel A:
09:15 UTC  ✓

Vessel B:
18:00 UTC  ✗
```

---

## 7. Direction Analysis

The dashboard compares:

```text
Spill movement direction
          +
Vessel course
          +
Vessel trajectory
```

For example:

```text
Spill:   North-East ↗
Vessel:  045°       ↗
```

Direction is treated as supporting evidence rather than proof.

---

# 🛤️ Vessel Trajectory Visualization

Trajectory reconstruction is one of the major features.

AIS data contains multiple positions:

```text
Time       Latitude   Longitude
--------------------------------
08:00      14.20      81.10
08:10      14.21      81.12
08:20      14.23      81.14
08:30      14.24      81.16
08:40      14.25      81.18
```

The dashboard connects these points chronologically.

```text
08:40 ●
     /
08:30 ●
    /
08:20 ●
   /
08:10 ●
  /
08:00 ●
```

The reconstructed trajectory can then be compared with the estimated spill origin.

---

# 📊 Association Scoring

The dashboard combines multiple pieces of evidence.

A conceptual scoring model is:

```text
Association Score
        =
Time Compatibility
+
Distance Compatibility
+
Trajectory Compatibility
+
Direction Compatibility
+
Duration Near Origin
```

Example:

| Vessel   | Time | Distance | Trajectory | Direction | Score |
| -------- | ---: | -------: | ---------: | --------: | ----: |
| Vessel A |   95 |       94 |         98 |        88 |    92 |
| Vessel B |   80 |       70 |         65 |        72 |    71 |
| Vessel C |   45 |       50 |         40 |        55 |    47 |

The dashboard presents this information visually so that the user can understand **why a vessel received a particular score**.

---

# 🏆 Vessel Ranking

Candidate vessels are displayed according to their association scores.

```text
┌──────┬──────────┬─────────────┐
│ Rank │ Vessel   │ Score       │
├──────┼──────────┼─────────────┤
│  1   │ Vessel A │ 92 / 100    │
│  2   │ Vessel B │ 71 / 100    │
│  3   │ Vessel C │ 47 / 100    │
└──────┴──────────┴─────────────┘
```

The highest-ranked vessel is the **strongest candidate for further investigation**, not automatically the confirmed source.

---

# 🗺️ Main Dashboard Layout

A recommended dashboard layout is:

```text
┌────────────────────────────────────────────────────┐
│       OIL SPILL SOURCE ATTRIBUTION SYSTEM          │
├────────────────────────────────────────────────────┤
│                                                    │
│  Spill Status │ Area │ Detection Time │ Age        │
│                                                    │
├───────────────────────────────┬────────────────────┤
│                               │                    │
│                               │ Spill Information  │
│                               │                    │
│        INTERACTIVE MAP        │ Origin             │
│                               │ Area               │
│        🛢️ Spill              │ Age                │
│        🚢 Vessels             │ Direction          │
│        ─ Trajectories         │                    │
│                               │                    │
├───────────────────────────────┴────────────────────┤
│                  VESSEL ANALYSIS                    │
├────────────┬────────────┬────────────┬─────────────┤
│ Vessel     │ Distance   │ Time       │ Score       │
├────────────┼────────────┼────────────┼─────────────┤
│ Vessel A   │ 1.8 km     │ 1.2 hrs    │ 92          │
│ Vessel B   │ 8.4 km     │ 9 hrs      │ 71          │
│ Vessel C   │ 22.1 km    │ 18 hrs     │ 47          │
├─────────────────────────────────────────────────────┤
│                    🚨 ALERT                         │
└─────────────────────────────────────────────────────┘
```

---

# 📥 Input Data

The dashboard may accept the following data.

## Satellite Data

Depending on your implementation:

```text
.tif
.jp2
.png
.jpg
```

Example:

```text
data/satellite/spill_image.tif
```

---

## AIS Data

Typical AIS CSV:

```csv
MMSI,timestamp,latitude,longitude,speed,course
123456789,2026-09-04T08:00:00,14.20,81.10,10.5,45
123456789,2026-09-04T08:10:00,14.21,81.12,10.6,45
123456789,2026-09-04T08:20:00,14.23,81.14,10.7,44
```

Required information generally includes:

* Vessel identifier
* Timestamp
* Latitude
* Longitude

Optional information:

* Speed
* Course
* Vessel type
* Vessel name

---

# 📤 Dashboard Output

The dashboard should provide:

### Spill information

```text
Spill detected
Location
Area
Age
Direction
Estimated origin
```

### Vessel information

```text
Vessel ID
Location
Speed
Course
Historical trajectory
Distance from origin
Time compatibility
```

### Analysis

```text
Spatial score
Temporal score
Trajectory score
Direction score
Overall association score
```

### Final visualization

```text
Interactive map
Vessel ranking
Alerts
Incident information
```

---

# 📂 Recommended Project Structure

```text
dashboard/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── app.py
│
├── data/
│   ├── satellite/
│   ├── ais/
│   └── processed/
│
├── assets/
│   ├── images/
│   └── icons/
│
├── src/
│   ├── spill_analysis/
│   ├── ais_processing/
│   ├── trajectory/
│   ├── spatial_analysis/
│   ├── temporal_analysis/
│   └── scoring/
│
├── outputs/
│   ├── maps/
│   ├── reports/
│   └── results/
│
└── tests/
```

**Your actual project may have a different structure. Keep the structure in this README synchronized with the real files.**

---

# ⚙️ Requirements

Typical requirements are:

```text
Python 3.10+
```

Possible Python packages:

```text
streamlit
pandas
numpy
geopandas
shapely
folium
plotly
rasterio
opencv-python
scikit-learn
```

The exact dependencies should be taken from the project's actual `requirements.txt`.

---

# 💻 Installation

## Step 1 — Open the Project

Open the dashboard folder in VS Code.

```text
VS Code
   ↓
File
   ↓
Open Folder
   ↓
Dashboard project folder
```

---

## Step 2 — Open Terminal

In VS Code:

```text
Terminal → New Terminal
```

---

## Step 3 — Create Virtual Environment

Windows:

```bash
python -m venv venv
```

---

## Step 4 — Activate Environment

Windows Command Prompt:

```bash
venv\Scripts\activate
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, you should see:

```text
(venv)
```

in the terminal.

---

# 📦 Step 5 — Install Dependencies

```bash
pip install --upgrade pip
```

Then:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Dashboard

The exact command depends on the framework used by your actual dashboard.

## If the dashboard uses Streamlit

If your entry file is `app.py`:

```bash
streamlit run app.py
```

If it is `dashboard.py`:

```bash
streamlit run dashboard.py
```

The terminal will display something similar to:

```text
Local URL:
http://localhost:8501
```

Open that address in your browser.

---

## If the dashboard uses Flask

The command may be:

```bash
python app.py
```

The terminal will provide the local address.

---

## If the dashboard uses another framework

Use the project's actual entry point and instructions.

> **Do not copy all three commands. Only use the command corresponding to your project's framework and entry file.**

---

# 🚀 Using the Dashboard

After starting the application:

### Step 1

Open the dashboard in the browser.

### Step 2

Upload/select the satellite image or spill information.

### Step 3

Upload/select the AIS dataset.

### Step 4

Start the analysis.

### Step 5

The dashboard processes the data.

### Step 6

View the detected spill on the map.

### Step 7

View candidate vessels and their historical trajectories.

### Step 8

Inspect spatial and temporal analysis.

### Step 9

View association scores and vessel ranking.

### Step 10

View alerts and predicted spill movement.

---

# 🔄 Complete Dashboard Data Flow

```text
USER
 │
 │ Uploads data
 ▼
DASHBOARD
 │
 ├───────────────┐
 ▼               ▼
Satellite       AIS
Data            Data
 │               │
 └───────┬───────┘
         ▼
    DATA PROCESSING
         │
         ▼
    SPILL ANALYSIS
         │
         ▼
    ORIGIN ESTIMATION
         │
         ▼
 TRAJECTORY RECONSTRUCTION
         │
         ▼
 ┌───────┼────────┐
 ▼       ▼        ▼
Spatial Temporal Direction
 │       │        │
 └───────┼────────┘
         ▼
   ASSOCIATION SCORE
         │
         ▼
   VESSEL RANKING
         │
         ▼
    DASHBOARD UI
         │
 ┌───────┼─────────┐
 ▼       ▼         ▼
MAP   ANALYTICS   ALERT
```

---

# 🚨 Alert System

The dashboard can display an alert such as:

```text
🚨 OIL SPILL DETECTED

Location:
14.24° N, 81.17° E

Area:
18.7 km²

Estimated movement:
North-East

Candidate requiring investigation:
Vessel A

Association score:
92 / 100
```

The alert provides information for **further investigation and response**.

---

# 🧪 Example Dashboard Scenario

Suppose the satellite detects an oil spill.

The system estimates:

```text
Spill location:
14.24° N, 81.17° E

Estimated release window:
04 Sept 08:00–12:00 UTC
```

AIS data shows:

```text
Vessel A:
Passed origin at 09:15 UTC

Vessel B:
Passed origin at 18:00 UTC

Vessel C:
Passed origin at 03:00 UTC
```

The system reconstructs their trajectories and calculates their spatial and temporal compatibility.

The dashboard could then display:

```text
Vessel A → 92/100
Vessel B → 71/100
Vessel C → 47/100
```

The map allows the user to visually verify the trajectories.

---

# 🧩 Dashboard Modules

| Module                    | Purpose                              |
| ------------------------- | ------------------------------------ |
| Data Upload               | Accept satellite/AIS data            |
| Spill Detection           | Identify potential oil spill         |
| Spill Analysis            | Extract spill characteristics        |
| Origin Estimation         | Estimate probable source region      |
| AIS Processing            | Process vessel positions             |
| Trajectory Reconstruction | Build historical vessel paths        |
| Spatial Analysis          | Calculate geographic relationships   |
| Temporal Analysis         | Compare relevant timestamps          |
| Direction Analysis        | Compare movement directions          |
| Scoring                   | Calculate association scores         |
| Ranking                   | Rank candidate vessels               |
| Map                       | Visualize all geographic information |
| Alerts                    | Display important events             |

---

# 🛠️ Troubleshooting

## `python is not recognized`

Check whether Python is installed:

```bash
python --version
```

If it is not recognized, install Python and enable **Add Python to PATH** during installation.

---

## `pip is not recognized`

Try:

```bash
python -m pip install -r requirements.txt
```

---

## `ModuleNotFoundError`

For example:

```text
ModuleNotFoundError: No module named 'streamlit'
```

Run:

```bash
pip install -r requirements.txt
```

---

## Dashboard does not start

Check:

1. Virtual environment is activated.
2. Dependencies are installed.
3. You are in the correct project directory.
4. You are using the correct entry-point file.
5. The required data/model files exist.

---

## Map is empty

Check:

* Latitude values
* Longitude values
* AIS timestamps
* Coordinate reference system
* Spill coordinates
* Date/time filtering

---

## No candidate vessels appear

Check:

* AIS file exists.
* AIS contains latitude/longitude.
* AIS timestamps are valid.
* AIS data overlaps the spill's time window.
* The geographic search radius is appropriate.

---

# 🔐 Data and API Configuration

If the dashboard uses external APIs, store credentials in environment variables rather than directly inside source code.

Example:

```text
API_KEY=your_key_here
AIS_API_KEY=your_key_here
```

Do not commit secret keys to GitHub.

Add sensitive files to `.gitignore`.

---

# 🎯 Hackathon Demo Flow

For a live hackathon demonstration, use this sequence:

```text
1. Open Dashboard
        ↓
2. Show Satellite Spill
        ↓
3. Show Spill Information
        ↓
4. Show Estimated Origin
        ↓
5. Load AIS Data
        ↓
6. Show Candidate Vessels
        ↓
7. Display Historical Trajectories
        ↓
8. Show Spatial + Temporal Analysis
        ↓
9. Show Association Scores
        ↓
10. Show Vessel Ranking
        ↓
11. Show Predicted Spill Movement
        ↓
12. Show Alert
```

### One-line explanation during the demo

> **“The dashboard takes the satellite-detected spill and AIS vessel history, reconstructs vessel trajectories, compares where and when each vessel was near the suspected origin, calculates an association score, and presents the results visually for investigation and response.”**

---

# 🚀 Future Dashboard Improvements

Future versions can include:

* Real-time AIS streaming
* Automatic satellite-image acquisition
* Multiple satellite sources
* Weather and ocean-current layers
* Real-time spill-drift prediction
* Automatic email/SMS alerts
* Historical incident database
* Advanced trajectory visualization
* 3D ocean visualization
* Mobile-responsive dashboard
* PDF incident-report generation
* Role-based access for authorities

---

# 📌 Summary

The dashboard serves as the **central visualization and decision-support interface** of the oil-spill source-attribution system.

The complete process is:

```text
SATELLITE
    ↓
SPILL DETECTION
    ↓
SPILL ORIGIN ESTIMATION
    ↓
AIS DATA
    ↓
VESSEL TRAJECTORIES
    ↓
SPATIAL + TEMPORAL + DIRECTION ANALYSIS
    ↓
ASSOCIATION SCORING
    ↓
VESSEL RANKING
    ↓
INTERACTIVE MAP
    ↓
ALERT + RESPONSE INFORMATION
```

### Core principle

> **“We don't simply identify the nearest vessel. We reconstruct vessel movement and combine spatial, temporal and trajectory evidence to identify vessels that have the strongest association with the detected spill.”**

---

##
