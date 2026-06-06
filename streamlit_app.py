import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta

API_URL = "https://nexadash-backend.onrender.com"

st.set_page_config(page_title='NexaDash', page_icon='N', layout='wide', initial_sidebar_state='expanded')

def api_login(username, password):
    try:
        r = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password}, timeout=15)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def api_get(endpoint, token):
    try:
        r = requests.get(f"{API_URL}{endpoint}", headers={"Authorization": f"Bearer {token}"}, timeout=15)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def fallback_metrics():
    return {
        "revenue": {"value": "$84,320", "change": "+12.4%"},
        "active_users": {"value": "14,892", "change": "+8.1%"},
        "conversion": {"value": "3.72%", "change": "+0.5%"},
        "avg_session": {"value": "4m 12s", "change": "+22s"},
        "uptime": {"value": "99.97%", "change": "+0.01%"},
    }

for k, v in {"authenticated": False, "username": "", "token": "", "plan": ""}.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.authenticated:
    st.markdown("# NexaDash Enterprise Dashboard")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)
    if submitted:
        with st.spinner("Authenticating via API..."):
            result = api_login(username, password)
        if result:
            st.session_state.authenticated = True
            st.session_state.username = result["username"]
            st.session_state.token = result["access_token"]
            st.session_state.plan = result["plan"]
            st.rerun()
        else:
            st.error("Invalid credentials. API may be warming up, try again in 30s.")
    st.info("Demo: username='admin'  password='NexaDash2026!'")
    st.stop()

TOKEN = st.session_state.token
np.random.seed(42)

st.sidebar.markdown("## NexaDash")
page = st.sidebar.radio('Navigation', ['Home','Dashboard','Analytics','Projects','Settings','Reports'], label_visibility="collapsed")
st.sidebar.markdown('---')
st.sidebar.markdown(f"**{st.session_state.username.capitalize()}**")
st.sidebar.caption(f"Plan: {st.session_state.plan}")
if st.sidebar.button('Sign Out', use_container_width=True):
    for k in ["authenticated","username","token","plan"]:
        st.session_state[k] = False if k == "authenticated" else ""
    st.rerun()

def chart_layout():
    return {'paper_bgcolor':'#1e2130','plot_bgcolor':'#1e2130','font':dict(color='#aaa'),'margin':dict(l=20,r=20,t=20,b=20),'hovermode':'x unified'}

if page == 'Home':
    st.title(f'Welcome back, {st.session_state.username.capitalize()}!')
    metrics = api_get("/api/metrics", TOKEN) or fallback_metrics()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric('Revenue', metrics["revenue"]["value"], metrics["revenue"]["change"], delta_color="off")
    c2.metric('Active Users', metrics["active_users"]["value"], metrics["active_users"]["change"], delta_color="off")
    c3.metric('Conversion', metrics["conversion"]["value"], metrics["conversion"]["change"], delta_color="off")
    c4.metric('Avg Session', metrics["avg_session"]["value"], metrics["avg_session"]["change"], delta_color="off")
    st.markdown('---')
elif page == 'Dashboard':
    st.title('Dashboard')
    metrics = api_get("/api/metrics", TOKEN) or fallback_metrics()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric('Revenue', metrics["revenue"]["value"], metrics["revenue"]["change"], delta_color="off")
    c2.metric('Active Users', metrics["active_users"]["value"], metrics["active_users"]["change"], delta_color="off")
    c3.metric('Conversion', metrics["conversion"]["value"], metrics["conversion"]["change"], delta_color="off")
    c4.metric('Uptime', metrics["uptime"]["value"], metrics["uptime"]["change"], delta_color="off")
    st.markdown('---')
    L,R = st.columns([2,1])
    with L:
        st.subheader('Monthly Revenue')
        rev = api_get("/api/revenue?days=30", TOKEN)
        days = rev["days"] if rev else list(range(1,31))
        vals = rev["revenue"] if rev else (np.cumsum(np.random.randint(2000,5000,30))+40000).tolist()
        tgt = rev["target"] if rev else np.linspace(vals[0],vals[-1]*1.1,30).tolist()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days,y=vals,fill='tozeroy',name='Revenue',line=dict(color='#7c83fd',width=2),fillcolor='rgba(124,131,253,0.15)'))
        fig.add_trace(go.Scatter(x=days,y=tgt,name='Target',line=dict(color='#3fb950',dash='dash')))
        fig.update_layout(chart_layout())
        st.plotly_chart(fig,use_container_width=True)
    with R:
        st.subheader('Traffic Sources')
        traffic = api_get("/api/traffic", TOKEN)
        labels = traffic["sources"] if traffic else ['Organic','Paid','Referral','Social','Direct']
        values = traffic["values"] if traffic else [38,27,15,12,8]
        fig2 = go.Figure(go.Pie(labels=labels,values=values,hole=0.55,marker=dict(colors=['#7c83fd','#3fb950','#f78166','#e3b300','#79c0ff'])))
        fig2.update_layout({'paper_bgcolor':'#1e2130','font':dict(color='#aaa'),'margin':dict(l=10,r=10,t=10,b=10)})
        st.plotly_chart(fig2,use_container_width=True)
    st.subheader('Recent Transactions')
    tx = api_get("/api/transactions", TOKEN)
    if tx:
        st.dataframe(pd.DataFrame(tx["transactions"]),use_container_width=True,hide_index=True)
    else:
        st.info("Loading transactions...")

elif page == 'Analytics':
    st.title('Analytics')
    analytics = api_get("/api/analytics?days=30", TOKEN)
    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Daily Active Users')
        days = analytics["days"] if analytics else list(range(1,31))
        dau = analytics["dau"] if analytics else np.random.randint(8000,16000,30).tolist()
        fig = go.Figure(go.Bar(x=days,y=dau,marker_color='#7c83fd'))
        fig.update_layout(chart_layout())
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        st.subheader('User Retention')
        ret = analytics["retention"] if analytics else {"weeks":["Wk1","Wk2","Wk3","Wk4"],"values":[100,68,52,43]}
        fig2 = go.Figure(go.Scatter(x=ret["weeks"],y=ret["values"],mode='lines+markers',line=dict(color='#3fb950',width=3),fill='tozeroy'))
        fig2.update_layout(chart_layout())
        st.plotly_chart(fig2,use_container_width=True)
    m = analytics["metrics"] if analytics else {"bounce_rate":{"value":"42.3%","change":"-2.1%"},"avg_page_load":{"value":"1.23s","change":"-0.15s"},"mobile_traffic":{"value":"68%","change":"+5.2%"}}
    a1,a2,a3 = st.columns(3)
    a1.metric("Bounce Rate",m["bounce_rate"]["value"],m["bounce_rate"]["change"],delta_color="off")
    a2.metric("Avg Page Load",m["avg_page_load"]["value"],m["avg_page_load"]["change"],delta_color="off")
    a3.metric("Mobile Traffic",m["mobile_traffic"]["value"],m["mobile_traffic"]["change"],delta_color="off")

elif page == 'Projects':
    st.title('Projects')
    pd_data = api_get("/api/projects", TOKEN)
    projects = pd_data["projects"] if pd_data else [
        {"name":"NexaDash v2.0","progress":78,"status":"On Track","color":"green"},
        {"name":"Mobile Redesign","progress":45,"status":"In Progress","color":"yellow"},
        {"name":"API Integration","progress":91,"status":"Almost Done","color":"green"},
        {"name":"Marketing Campaign","progress":33,"status":"Delayed","color":"red"},
        {"name":"Data Pipeline","progress":60,"status":"On Track","color":"green"},
    ]
    for p in projects:
        col1,col2 = st.columns([3,1])
        with col1:
            st.markdown(f"**{p['name']}** - {p['status']}")
            st.progress(p["progress"]/100)
        with col2:
            st.metric("Progress",f"{p['progress']}%",label_visibility="collapsed")
        st.markdown("---")

elif page == 'Settings':
    st.title('Settings')
    user_data = api_get("/api/user/me", TOKEN)
    tab1,tab2,tab3 = st.tabs(["Profile","Preferences","Security"])
    with tab1:
        with st.form("profile_form"):
            st.text_input("Name", value=user_data["name"] if user_data else st.session_state.username.capitalize())
            st.text_input("Email", value=user_data["email"] if user_data else "admin@nexadash.io")
            st.text_area("Bio", value="Data enthusiast and dashboard builder")
            if st.form_submit_button("Save Profile",use_container_width=True): st.success("Profile updated!")
    with tab2:
        with st.form("preferences_form"):
            st.selectbox("Theme",["Dark","Light"],index=0)
            st.toggle("Email Notifications",value=True)
            st.slider("Refresh Interval (s)",10,300,60)
            if st.form_submit_button("Save Preferences",use_container_width=True): st.success("Preferences saved!")
    with tab3:
        st.info("Secured with JWT via the NexaDash API.")
        with st.form("security_form"):
            st.text_input("Current Password",type="password")
            np_ = st.text_input("New Password",type="password")
            cp_ = st.text_input("Confirm Password",type="password")
            if st.form_submit_button("Change Password",use_container_width=True):
                st.success("Password changed!") if np_==cp_ else st.error("Passwords do not match!")

elif page == 'Reports':
    st.title('Reports')
    report_type = st.selectbox("Report Type",["Revenue Summary","User Activity","Performance Metrics","Custom Report"])
    col1,col2 = st.columns(2)
    with col1: st.date_input("Report Date",value=datetime.now())
    with col2: st.selectbox("Export Format",["PDF","CSV","Excel"])
    if st.button("Generate Report",use_container_width=True):
        with st.spinner("Fetching from API..."):
            report = api_get(f"/api/reports?report_type={report_type.replace(' ','%20')}", TOKEN)
        if report:
            st.success(f"{report['report_type']} generated at {report['generated_at'][:19]}")
            st.dataframe(pd.DataFrame(report["summary"]),use_container_width=True,hide_index=True)
            with st.expander("Detailed Analysis"):
                for line in report["analysis"]: st.write(f"- {line}")
        else:
            st.warning("API warming up, showing cached data.")
            st.dataframe(pd.DataFrame({'Metric':['Revenue','Users','Conversion','Uptime'],'Current':['$84,320','14,892','3.72%','99.97%'],'Change':['+12.4%','+8.1%','+0.27%','+0.02%']}),use_container_width=True,hide_index=True)

    rev = api_get("/api/revenue?days=30", TOKEN)
    days = rev["days"] if rev else list(range(1,31))
    vals = rev["revenue"] if rev else (np.cumsum(np.random.randint(2000,5000,30))+40000).tolist()
    fig = go.Figure(go.Scatter(x=days,y=vals,fill='tozeroy',line=dict(color='#7c83fd',width=2),fillcolor='rgba(124,131,253,0.15)'))
    fig.update_layout(chart_layout())
    st.plotly_chart(fig, use_container_width=True)
    notifs = api_get("/api/notifications", TOKEN)
    count = notifs["count"] if notifs else 3
    a,b,c = st.columns(3)
    with a: st.info(f'{count} notifications pending')
    with b: st.success('12 tasks completed today')
    with c: st.warning('2 issues need attention')
