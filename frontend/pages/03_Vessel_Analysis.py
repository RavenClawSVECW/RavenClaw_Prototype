import streamlit as st,plotly.express as px
st.title("🚢 Vessel Analysis")
d=st.session_state.get("analysis")
if d is None: st.warning("Analyze the files first.");st.stop()
st.dataframe(d[["Rank","Vessel","MMSI","Type","Distance (km)","Probability","Risk","Proximity Score","Time Score","Direction Score","Speed Score"]],use_container_width=True,hide_index=True)
sel=st.selectbox("Inspect vessel",d.Vessel);q=d[d.Vessel==sel].iloc[0]
st.subheader("🧩 Evidence Breakdown")
st.plotly_chart(px.bar(x=[q["Proximity Score"],q["Time Score"],q["Direction Score"],q["Speed Score"]],y=["Proximity","Time","Direction","Speed"],orientation="h",range_x=[0,100]),use_container_width=True)
