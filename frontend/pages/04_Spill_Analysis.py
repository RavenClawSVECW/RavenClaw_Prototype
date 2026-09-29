import streamlit as st,folium
from streamlit_folium import st_folium
st.title("🛢️ Spill Analysis")
s=st.session_state.get("spill")
if s is None: st.warning("Upload spill JSON first.");st.stop()
c=s.get("center",{});lat=float(c.get("latitude",s.get("latitude",0)));lon=float(c.get("longitude",s.get("longitude",0)))
a,b,c,d=st.columns(4);a.metric("Area",str(s.get("spill_area_km2","N/A"))+" km²");b.metric("Age",str(s.get("estimated_age_hours","N/A"))+" hrs");c.metric("Direction",s.get("spread_direction","N/A"));d.metric("Confidence",str(round(float(s.get("confidence",0))*100))+"%")
m=folium.Map([lat,lon],zoom_start=8,tiles="OpenStreetMap");folium.Marker([lat,lon],tooltip="Detected Spill",icon=folium.Icon(color="red")).add_to(m)
x=s.get("boundary",{})
if all(k in x for k in ["latitude_min","latitude_max","longitude_min","longitude_max"]): folium.Rectangle([[float(x["latitude_min"]),float(x["longitude_min"])],[float(x["latitude_max"]),float(x["longitude_max"])]],color="red",fill=True,fill_opacity=.18).add_to(m)
st_folium(m,height=500,use_container_width=True);st.json(s)
