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

for k, v in {"authenticated": False, "username": "", "token": "", "plan": "", "login_time": None}.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.authenticated:
    st.markdown("# NexaDash")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)
    if submitted:
        with st.spinner("Authenticating..."):
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

st.sidebar.markdown("## Menu")
page = st.sidebar.radio('Navigation', ['Home','Dashboard','Analytics','Projects','Settings','Reports'], label_visibility="collapsed")
st.sidebar.markdown('---')
st.sidebar.markdown(f"**{st.session_state.username.capitalize()}**")
st.sidebar.caption(f"Plan: {st.session_state.plan}")
if st.sidebar.button('Sign Out', use_container_width=True):
    for k in ["authenticated","username","token","plan"]:
        st.session_state[k] = False if k == "authenticated" else ""
    st.rerun()

def chart_layout():
    return {'paper_bgcolor':'#1e2130','plot_bgcolor':'#1e2130','font':dict(color='#aaa'),'margin':dict(l=20,r=20,t=20,b=20)}

if page == 'Home':
    st.title(f'Welcome back, {st.session_state.username.capitalize()}!')
    metrics = api_get("/api/metrics", TOKEN) or fallback_metrics()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric('Revenue', metrics["revenue"]["value"], metrics["revenue"]["change"], delta_color="off")
    c2.metric('Active Users', metrics["active_users"]["value"], metrics["active_users"]["change"], delta_color="off")
    c3.metric('Conversion', metrics["conversion"]["value"], metrics["conversion"]["change"], delta_color="off")
    c4.metric('Avg Session', metrics["avg_session"]["value"], metrics["avg_session"]["change"], delta_color="off")
    st.markdown('---')
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
