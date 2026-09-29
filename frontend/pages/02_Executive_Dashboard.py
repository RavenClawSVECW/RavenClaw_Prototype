import streamlit as st,folium
from streamlit_folium import st_folium
import plotly.express as px
st.title("📊 Executive Dashboard")
d=st.session_state.get("analysis")
if d is None: st.warning("Analyze the files first."); st.stop()
s=st.session_state.spill;c=s.get("center",{}); lat=float(c.get("latitude",s.get("latitude",d.Latitude.mean())));lon=float(c.get("longitude",s.get("longitude",d.Longitude.mean())))
k=st.columns(5); vals=[("🚢 Vessels",len(d)),("🛢️ Spill Area",str(s.get("spill_area_km2","N/A"))+" km²"),("🔴 High Risk",int((d.Risk=="HIGH").sum())),("🎯 Top Probability",str(d.iloc[0].Probability)+"%"),("🥇 Top Candidate",d.iloc[0].Vessel)]
for x,(l,v) in zip(k,vals): x.metric(l,v)
l,r=st.columns([1.3,1])
with l:
 m=folium.Map([lat,lon],zoom_start=8,tiles="OpenStreetMap");folium.Marker([lat,lon],tooltip="Oil Spill",icon=folium.Icon(color="red")).add_to(m)
 b=s.get("boundary",{})
 if all(x in b for x in ["latitude_min","latitude_max","longitude_min","longitude_max"]): folium.Rectangle([[float(b["latitude_min"]),float(b["longitude_min"])],[float(b["latitude_max"]),float(b["longitude_max"])]],color="red",fill=True,fill_opacity=.15).add_to(m)
 for _,q in d.iterrows(): folium.CircleMarker([q.Latitude,q.Longitude],radius=7,color="red" if q.Risk=="HIGH" else ("orange" if q.Risk=="MEDIUM" else "blue"),fill=True,tooltip=f"{q.Vessel} | {q.Probability}%").add_to(m)
 st_folium(m,height=520,use_container_width=True)
with r:
 st.plotly_chart(px.bar(d.sort_values("Probability"),x="Probability",y="Vessel",orientation="h",range_x=[0,100],text="Probability"),use_container_width=True)
q=d.iloc[0];st.success(f"🥇 {q.Vessel} is the highest-ranked candidate at {q.Probability}%. This is a probabilistic risk score, not proof of causation.")
