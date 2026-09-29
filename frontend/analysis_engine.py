import math
from datetime import datetime,timezone
import pandas as pd
def pt(v):
 try:
  d=datetime.fromisoformat(str(v).replace("Z","+00:00")); return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
 except: return None
def hav(a,b,c,d):
 R=6371;p=math.radians
 x=p(c-a);y=p(d-b);q=math.sin(x/2)**2+math.cos(p(a))*math.cos(p(c))*math.sin(y/2)**2
 return 2*R*math.asin(math.sqrt(q))
def bearing(x):
 return {"N":0,"NORTH":0,"NE":45,"NORTHEAST":45,"NORTH EAST":45,"E":90,"EAST":90,"SE":135,"SOUTHEAST":135,"SOUTH EAST":135,"S":180,"SOUTH":180,"SW":225,"SOUTHWEST":225,"SOUTH WEST":225,"W":270,"WEST":270,"NW":315,"NORTHWEST":315,"NORTH WEST":315}.get(str(x).upper().replace("-"," ").strip())
def ad(a,b):
 d=abs((a-b)%360); return min(d,360-d)
def analyze(vs,s):
 c=s.get("center",{}); slat=float(c.get("latitude",s.get("latitude",0))); slon=float(c.get("longitude",s.get("longitude",0)))
 st=pt(s.get("detection_time")); age=float(s.get("estimated_age_hours",24)); db=bearing(s.get("spread_direction")); drift=float(s.get("estimated_drift_speed_knots",1.8))
 out=[]
 for r in vs:
  try: lat=float(r["latitude"]);lon=float(r["longitude"])
  except: continue
  dist=hav(lat,lon,slat,slon); prox=max(0,min(100,100*(1-dist/50)))
  vt=pt(r.get("timestamp")); delta=abs((st-vt).total_seconds())/3600 if st and vt else None
  time=max(0,min(100,100*(1-abs(delta-age)/max(age,1)))) if delta is not None else 50
  hd=float(r.get("heading",0) or 0); dire=50 if db is None else max(0,100*(1-ad(hd,db)/180))
  sp=float(r.get("speed_knots",r.get("speed",0)) or 0); ss=50 if sp<=0 else max(0,min(100,min(sp,drift*10)/(drift*10)*100))
  typ=str(r.get("vessel_type","")).lower(); ts=100 if "tanker" in typ or "oil" in typ else 60
  score=prox*.35+time*.25+dire*.20+ss*.10+ts*.10
  out.append({"Rank":0,"Vessel":r.get("vessel_name",r.get("name","Unknown")),"MMSI":r.get("mmsi","N/A"),"Type":r.get("vessel_type","Unknown"),"Latitude":lat,"Longitude":lon,"Speed":sp,"Heading":hd,"Distance (km)":round(dist,2),"Time Score":round(time,1),"Direction Score":round(dire,1),"Proximity Score":round(prox,1),"Speed Score":round(ss,1),"Probability":round(score,1)})
 d=pd.DataFrame(out).sort_values("Probability",ascending=False).reset_index(drop=True)
 if len(d): d["Rank"]=range(1,len(d)+1); d["Risk"]=d.Probability.apply(lambda x:"HIGH" if x>=70 else ("MEDIUM" if x>=45 else "LOW"))
 return d
