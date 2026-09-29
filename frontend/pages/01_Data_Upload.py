import streamlit as st,json
from analysis_engine import analyze
st.title("📂 Data Upload & Analysis")
a,b=st.columns(2)
with a: vf=st.file_uploader("🚢 Vessel Data JSON",type="json")
with b: sf=st.file_uploader("🛢️ Spill Information JSON",type="json")
if vf and sf:
 try:
  vd=json.load(vf); sd=json.load(sf); rows=vd if isinstance(vd,list) else vd.get("vessels",[])
  if st.button("🔍 ANALYZE DATA",type="primary",use_container_width=True):
   st.session_state.vessels=rows; st.session_state.spill=sd; st.session_state.analysis=analyze(rows,sd); st.success("Analysis completed. Use the sidebar pages.")
 except Exception as e: st.error(str(e))
else: st.warning("Upload both JSON files.")
