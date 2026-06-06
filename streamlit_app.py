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

st.sidebar.markdown("## Menu")
page = st.sidebar.radio('Navigation', ['Home','Dashboard','Analytics','Projects','Pricing','Settings','Reports'], label_visibility="collapsed")
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
        fig2.update_layout(chart_layout()); fig2.update_yaxes(range=[0,110])
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
        icon = {"green":"[ON]","yellow":"[WIP]","red":"[!]"}.get(p["color"],"[?]")
        col1,col2 = st.columns([3,1])
        with col1:
            st.markdown(f"**{icon} {p['name']}** - {p['status']}")
            st.progress(p["progress"]/100)
        with col2:
            st.metric("Progress",f"{p['progress']}%",label_visibility="collapsed")
        st.markdown("---")
elif page == 'Pricing':
    st.title('Choose Your Plan')
    st.markdown('<p style="color:#aaa;font-size:18px;">Unlock the full power of NexaDash. No contracts, cancel anytime.</p>', unsafe_allow_html=True)
    st.markdown('---')
    st.markdown("""
    <style>
    .plan-card{background:#1e2130;border-radius:16px;padding:32px;border:1px solid #30363d;transition:all 0.3s;}
    .plan-card.featured{border:2px solid #7c83fd;box-shadow:0 0 24px rgba(124,131,253,0.25);}
    .plan-title{font-size:26px;font-weight:700;margin-bottom:4px;}
    .plan-price{font-size:48px;font-weight:800;margin:12px 0;}
    .plan-price span{font-size:18px;font-weight:400;color:#aaa;}
    .plan-feature{padding:6px 0;color:#ccc;font-size:15px;}
    .plan-feature::before{content:'+ ';color:#7c83fd;font-weight:700;}
    .plan-badge{background:linear-gradient(135deg,#7c83fd,#bf7cfd);color:white;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;display:inline-block;margin-bottom:12px;}
    </style>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class="plan-card">
          <div class="plan-title" style="color:#7c83fd;">GOD MODE</div>
          <div class="plan-price">$4.99<span>/mo</span></div>
          <hr style="border-color:#30363d;">
          <div class="plan-feature">Full Dashboard Access</div>
          <div class="plan-feature">Real-Time Analytics</div>
          <div class="plan-feature">Project Tracker</div>
          <div class="plan-feature">Revenue Insights</div>
          <div class="plan-feature">Priority Support</div>
          <div class="plan-feature">API Access</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        god_link = "https://buy.stripe.com/3cIbJ1aSzaKdbRq77tc7u01"
        st.markdown(f'<a href="{god_link}" target="_blank" style="display:block;text-align:center;background:linear-gradient(135deg,#7c83fd,#5865f2);color:white;padding:14px;border-radius:10px;font-weight:700;font-size:17px;text-decoration:none;">Subscribe to GOD MODE</a>', unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="plan-card featured">
          <div class="plan-badge">MOST POWERFUL</div><br>
          <div class="plan-title" style="background:linear-gradient(135deg,#bf7cfd,#ff6eb4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">UNIVERSE MODE</div>
          <div class="plan-price" style="background:linear-gradient(135deg,#bf7cfd,#ff6eb4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">$9.99<span style="-webkit-text-fill-color:#aaa;">/mo</span></div>
          <hr style="border-color:#30363d;">
          <div class="plan-feature">Everything in GOD MODE</div>
          <div class="plan-feature">AI-Powered Forecasting</div>
          <div class="plan-feature">Custom Integrations</div>
          <div class="plan-feature">Team Collaboration</div>
          <div class="plan-feature">White-Label Reports</div>
          <div class="plan-feature">Dedicated Account Manager</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        universe_link = "https://buy.stripe.com/14A6oHgcT7y1cVufDZc7u00"
        st.markdown(f'<a href="{universe_link}" target="_blank" style="display:block;text-align:center;background:linear-gradient(135deg,#bf7cfd,#ff6eb4);color:white;padding:14px;border-radius:10px;font-weight:700;font-size:17px;text-decoration:none;">Subscribe to UNIVERSE MODE</a>', unsafe_allow_html=True)
    st.markdown('<br><br>', unsafe_allow_html=True)
    with st.expander('FAQ'):
        st.markdown('**Can I cancel anytime?** Yes, cancel with one click from your billing portal.')
        st.markdown('**Is there a free trial?** Sign in and use the demo dashboard for free before subscribing.')
        st.markdown('**What payment methods?** All major credit/debit cards via Stripe.')
    st.markdown('<p style="text-align:center;color:#555;margin-top:24px;">Secured by Stripe. Your payment info is never stored on our servers.</p>', unsafe_allow_html=True)
elif page == 'Settings':
    st.title('Settings')
    st.subheader('Profile')
    c1,c2 = st.columns(2)
    with c1:
        st.text_input('Display Name', value=st.session_state.username.capitalize())
        st.text_input('Email', value='admin@nexadash.io')
    with c2:
        st.selectbox('Timezone', ['UTC-5 (EST)', 'UTC+0 (GMT)', 'UTC+1 (CET)', 'UTC+8 (SGT)'])
        st.selectbox('Language', ['English', 'Spanish', 'French', 'German'])
    st.markdown('---')
    st.subheader('Notifications')
    st.toggle('Email Alerts', value=True)
    st.toggle('Slack Notifications', value=False)
    st.toggle('Weekly Digest', value=True)
    st.markdown('---')
    st.subheader('API')
    st.code(f'Bearer {TOKEN[:20]}...', language=None)
    st.caption('Keep this token secret.')
    if st.button('Save Settings', type='primary'):
        st.success('Settings saved!')

elif page == 'Reports':
    st.title('Reports')
    reports = api_get("/api/reports", TOKEN)
    reps = reports["reports"] if reports else [
        {"title":"Q1 2026 Revenue Report","date":"2026-04-01","type":"Financial","status":"Ready"},
        {"title":"User Growth Analysis","date":"2026-05-15","type":"Analytics","status":"Ready"},
        {"title":"Infrastructure Audit","date":"2026-05-28","type":"Technical","status":"Processing"},
        {"title":"Marketing ROI","date":"2026-06-01","type":"Marketing","status":"Ready"},
        {"title":"Churn Analysis","date":"2026-06-04","type":"Analytics","status":"Ready"},
    ]
    filter_type = st.selectbox('Filter by Type', ['All','Financial','Analytics','Technical','Marketing'])
    filtered = [r for r in reps if filter_type=='All' or r['type']==filter_type]
    df = pd.DataFrame(filtered)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('---')
    r1,r2,r3 = st.columns(3)
    r1.metric('Total Reports', len(reps))
    r2.metric('Ready', sum(1 for r in reps if r['status']=='Ready'))
    r3.metric('Processing', sum(1 for r in reps if r['status']=='Processing'))
