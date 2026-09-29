import streamlit as st
st.title("🚨 Alerts")
d=st.session_state.get("analysis")
if d is None: st.warning("Analyze the files first.");st.stop()
for level,msg in [("HIGH","🔴 Immediate investigation"),("MEDIUM","🟠 Monitor closely"),("LOW","🟢 Low priority")]:
 q=d[d.Risk==level]
 st.subheader(msg)
 if len(q): st.dataframe(q[["Vessel","Probability","Distance (km)","Risk"]],use_container_width=True,hide_index=True)
 else: st.write("No vessels in this category.")
st.info("Alerts are decision-support indicators, not proof of legal responsibility.")
