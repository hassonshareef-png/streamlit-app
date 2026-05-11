import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

st.set_page_config(page_title="NexaDash", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")
np.random.seed(42)

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}
.stApp{background:#0f1117;}
section[data-testid="stSidebar"]{background:#161b27!important;border-right:1px solid #252d3d;}
section[data-testid="stSidebar"] *{color:#c9d1d9!important;}
.logo{font-size:1.5rem;font-weight:700;color:#58a6ff!important;display:block;text-align:center;padding:0.5rem 0 1.5rem;}
.card{background:#161b27;border:1px solid #252d3d;border-radius:12px;padding:1.2rem 1.4rem;margin-bottom:1rem;}
.ct{font-size:.75rem;font-weight:600;color:#8b949e;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.3rem;}
.cv{font-size:1.9rem;font-weight:700;color:#f0f6fc;line-height:1.1;}
.cd{font-size:.8rem;margin-top:.25rem;}
.up{color:#3fb950;} .dn{color:#f85149;}
.sh{font-size:1.2rem;font-weight:700;color:#f0f6fc;margin:1rem 0 .6rem;border-left:4px solid #58a6ff;padding-left:.7rem;}
.badge{display:inline-block;padding:.2rem .6rem;border-radius:999px;font-size:.7rem;font-weight:600;}
.bb{background:#1f3a5f;color:#58a6ff;} .bg{background:#1a3a2a;color:#3fb950;}
.br{background:#3d1a1a;color:#f85149;} .bp{background:#2d1f5e;color:#a371f7;}
.hero{background:linear-gradient(135deg,#1f3a5f,#0f1117 60%,#2d1f5e);border:1px solid #252d3d;border-radius:16px;padding:2.2rem;margin-bottom:1.4rem;}
.hero h1{font-size:2.2rem;font-weight:800;color:#f0f6fc;margin:0 0 .3rem;}
.hero p{color:#8b949e;margin:0;}
.ac{color:#58a6ff;}
.stbl{width:100%;border-collapse:collapse;font-size:.86rem;color:#c9d1d9;}
.stbl th{background:#21262d;color:#8b949e;padding:.55rem .7rem;text-align:left;font-size:.7rem;text-transform:uppercase;}
.stbl td{padding:.55rem .7rem;border-bottom:1px solid #21262d;}
.stbl tr:hover td{background:#21262d;}
.ai{display:flex;gap:.7rem;padding:.65rem 0;border-bottom:1px solid #21262d;}
.at{font-size:.86rem;color:#c9d1d9;} .atm{font-size:.73rem;color:#6e7681;margin-top:2px;}
hr{border-color:#252d3d;margin:1rem 0;}
</style>""", unsafe_allow_html=True)

CL = dict(paper_bgcolor="#161b27",plot_bgcolor="#161b27",
          font=dict(family="Inter",color="#8b949e",size=11),
          margin=dict(l=8,r=8,t=28,b=8),
          xaxis=dict(gridcolor="#21262d",zerolinecolor="#21262d"),
          yaxis=dict(gridcolor="#21262d",zerolinecolor="#21262d"))

with st.sidebar:
    st.markdown('<span class="logo">⚡ NexaDash</span>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("", ["🏠  Home","📊  Dashboard","📈  Analytics","🗂️  Projects","⚙️  Settings"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f'<div style="font-size:.75rem;color:#6e7681;text-align:center;">Last synced: {datetime.now().strftime("%b %d, %H:%M")}</div>', unsafe_allow_html=True)

if "Home" in page:
    st.markdown('<div class="hero"><h1>Welcome back, <span class="ac">Hass</span> 👋</h1><p>Here\'s what\'s happening across your workspace today.</p></div>', unsafe_allow_html=True)
    kpis=[("Total Revenue","$284,920","+12.4%",True),("Active Users","14,382","+8.1%",True),("Open Tickets","37","-5",True),("Uptime","99.97%","-0.01%",False)]
    for col,(t,v,d,u) in zip(st.columns(4),kpis):
        col.markdown(f'<div class="card"><div class="ct">{t}</div><div class="cv">{v}</div><div class="cd {"up" if u else "dn"}">{"▲" if u else "▼"} {d} vs last month</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    c1,c2=st.columns([2,1])
    with c1:
        st.markdown('<div class="sh">Revenue Overview</div>', unsafe_allow_html=True)
        days=pd.date_range(end=datetime.today(),periods=30)
        rev=np.cumsum(np.random.normal(9500,2200,30)).clip(min=0)
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=days,y=rev,mode="lines",name="Actual",line=dict(color="#58a6ff",width=2.5),fill="tozeroy",fillcolor="rgba(88,166,255,0.08)"))
        fig.add_trace(go.Scatter(x=days,y=np.linspace(rev[0],rev[-1]*1.1,30),mode="lines",name="Target",line=dict(color="#3fb950",width=1.5,dash="do
elif "Dashboard" in page:
    st.markdown('<div class="sh">📊 Dashboard</div>', unsafe_allow_html=True)
    for col,(t,v,d,u) in zip(st.columns(3),[("Monthly Active Users","14,382","+8.1%",True),("Conversion Rate","3.84%","+0.6%",True),("Avg Session","4m 32s","-0:12",False)]):
        col.markdown(f'<div class="card"><div class="ct">{t}</div><div class="cv">{v}</div><div class="cd {"up" if u else "dn"}">{ "▲" if u else "▼"} {d}</div></div>', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="sh">Users by Country</div>', unsafe_allow_html=True)
        df=pd.DataFrame({"Country":["USA","UK","Germany","Canada","Australia","France","India","Brazil"],"Users":[5200,2100,1800,1400,900,850,1300,700]})
        fig=px.bar(df,x="Users",y="Country",orientation="h",color="Users",color_continuous_scale="Blues")
        fig.update_layout(**CL,height=290,coloraxis_showscale=False)
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="sh">Traffic Sources</div>', unsafe_allow_html=True)
        fig=go.Figure(go.Pie(labels=["Organic","Direct","Referral","Social","Email"],values=[38,27,18,12,5],hole=0.55,marker=dict(colors=["#58a6ff","#3fb950","#a371f7","#f0883e","#f85149"],line=dict(color="#161b27",width=2))))
        fig.update_layout(**CL,height=290,legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig,use_container_width=True)
    st.markdown('<div class="sh">Daily Active Users — Last 60 Days</div>', unsafe_allow_html=True)
    days=pd.date_range(end=datetime.today(),periods=60)
    dau=(np.sin(np.linspace(0,3.5*np.pi,60))*1500+np.random.normal(8000,400,60)).clip(min=0)
    fig=go.Figure(go.Scatter(x=days,y=dau,mode="lines",line=dict(color="#a371f7",width=2),fill="tozeroy",fillcolor="rgba(163,113,247,0.08)"))
    fig.update_layout(**CL,height=210)
    st.plotly_chart(fig,use_container_width=True)
elif "Analytics" in page:
    st.markdown('<div class="sh">📈 Analytics</div>', unsafe_allow_html=True)
    tab1,tab2,tab3=st.tabs(["  Revenue  ","  Engagement  ","  Retention  "])
    with tab1:
        mo=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        fig=go.Figure()
        fig.add_trace(go.Bar(x=mo,y=[38,42,39,51,48,62,57,70,64,72,68,80],name="2025",marker_color="rgba(88,166,255,0.35)"))
        fig.add_trace(go.Bar(x=mo[:5],y=[44,49,55,61,None],name="2026",marker_color="#58a6ff"))
        fig.update_layout(**CL,height=300,barmode="group",legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig,use_container_width=True)
    with tab2:
        eng=[120,80,60,45,55,110,320,680,820,790,750,810,870,900,860,780,710,820,910,850,720,580,390,220]
        fig=go.Figure(go.Bar(x=list(range(24)),y=eng,marker_color=["#58a6ff" if e==max(eng) else "#1f3a5f" for e in eng]))
        fig.update_layout(**CL,height=280,xaxis_title="Hour of Day",yaxis_title="Sessions")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('<div class="card"><b style="color:#f0f6fc;">Peak hour:</b> <span class="badge bb">2:00 PM</span> with 910 sessions</div>', unsafe_allow_html=True)
    with tab3:
        fig=go.Figure(go.Scatter(x=["Wk 1","Wk 2","Wk 3","Wk 4","Wk 5","Wk 6"],y=[100,68,52,44,39,35],mode="lines+markers",line=dict(color="#3fb950",width=2.5),marker=dict(size=8,color="#3fb950")))
        fig.add_hline(y=30,line_dash="dot",line_color="#f85149",annotation_text="Industry avg 30%",annotation_font_color="#f85149")
        fig.update_layout(**CL,height=290,yaxis_title="Retention %",yaxis_range=[0,110])
        st.plotly_chart(fig,use_container_width=True)
elif "Projects" in page:
    st.markdown('<div class="sh">🗂️ Projects</div>', unsafe_allow_html=True)
    bm={"In Progress":"bb","Completed":"bg","Planning":"bp","In Review":"br"}
    for nm,dp,st_,pc,cl in [("Platform Redesign","UI/UX","In Progress",72,"#58a6ff"),("API v3 Migration","Engineering","In Progress",45,"#a371f7"),("Mobile App Launch","Product","Planning",18,"#f0883e"),("Data Warehouse","Data","Completed",100,"#3fb950"),("Security Audit Q2","Security","In Review",88,"#f85149"),("Marketing Dashboard","Marketing","Planning",10,"#f0883e")]:
        st.markdown(f'<div class="card" style="margin-bottom:.5rem;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem;"><div><span style="font-weight:600;color:#f0f6fc;">{nm}</span><span style="color:#6e7681;font-size:.76rem;margin-left:.5rem;">· {dp}</span></div><span class="badge {bm[st_]}">{st_}</span></div><div style="background:#21262d;border-radius:999px;height:5px;overflow:hidden;"><div style="width:{pc}%;height:100%;background:{cl};border-radius:999px;"></div></div><div style="font-size:.73rem;color:#6e7681;margin-top:.25rem;">{pc}% complete</div></div>', unsafe_allow_html=True)
elif "Settings" in page:
    st.markdown('<div class="sh">⚙️ Settings</div>', unsafe_allow_html=True)
    with st.form("sf"):
        st.subheader("Profile")
        c1,c2=st.columns(2)
        c1.text_input("Full Name",value="Hass")
        c2.text_input("Email",value="hassonshareef@gmail.com")
        st.selectbox("Role",["Admin","Manager","Analyst","Viewer"])
        st.subheader("Notifications")
        c1,c2=st.columns(2)
        c1.checkbox("Email alerts",value=True); c1.checkbox("Weekly digest",value=True)
        c2.checkbox("Push notifications"); c2.checkbox("SMS alerts")
        st.subheader("Security")
        c1,c2=st.columns(2)
        c1.text_input("Current Password",type="password")
        c2.text_input("New Password",type="password")
        if st.form_submit_button("💾  Save Changes",use_container_width=True):
            st.success("✅ Settings saved successfully!")t")))
        fig.update_layout(**CL,height=240,legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.12))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown('<div class="sh">Activity Feed</div>', unsafe_allow_html=True)
        for dot,txt,t in [("🟢","New signup: alex@email.com","2 min ago"),("🔵","Deploy #482 completed","14 min ago"),("🟡","High CPU on us-east-1","31 min ago"),("🟢","Invoice #1204 paid","1 hr ago"),("🔴","Failed login blocked","2 hr ago")]:
            st.markdown(f'<div class="ai"><span style="margin-top:3px;font-size:.75rem;">{dot}</span><div><div class="at">{txt}</div><div class="atm">{t}</div></div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="sh">Recent Transactions</div>', unsafe_allow_html=True)
    rows=""
    for dt,cu,am,st_,me in [("May 11","Acme Corp","$12,400","Paid","Card"),("May 10","Bright Labs","$6,800","Paid","Wire"),("May 10","SkyNet Inc","$3,200","Pending","Card"),("May 09","DataFlow","$9,500","Paid","Wire"),("May 09","Novatech","$4,100","Refunded","Card")]:
        bc={"Paid":"bg","Pending":"bb","Refunded":"br"}[st_]
        rows+=f'<tr><td>{dt}</td><td>{cu}</td><td style="font-weight:600;color:#f0f6fc;">{am}</td><td><span class="badge {bc}">{st_}</span></td><td>{me}</td></tr>'
    st.markdown(f'<div class="card" style="padding:.7rem;"><table class="stbl"><tr><th>Date</th><th>Customer</th><th>Amount</th><th>Status</th><th>Method</th></tr>{rows}</table></div>', unsafe_allow_html=True)
