
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import hashlib
from datetime import datetime, timedelta

# Page Config
st.set_page_config(
    page_title='NexaDash',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    .metric-increase {
        color: #3fb950;
    }
    .metric-decrease {
        color: #f78166;
    }
</style>
""", unsafe_allow_html=True)

# Authentication - passwords SHA-256 hashed. Default password: NexaDash2026!
USERS = {
    "admin": "99051091580170494132cc07c5bfbd956bdce00ebc0ceded5808316d3efa3ffc",
    "hass": "99051091580170494132cc07c5bfbd956bdce00ebc0ceded5808316d3efa3ffc",
}

USER_PLANS = {
    "admin": "Enterprise",
    "hass": "Pro"
}

def _hash(pw):
    """Hash password using SHA-256"""
    return hashlib.sha256(pw.encode()).hexdigest()

def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.login_time = None
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"

# Initialize session state
init_session_state()

def login_page():
    """Display login page"""
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"]{background:#0f1117;}
            [data-testid="stSidebar"]{display:none;}
            .block-container{max-width:420px;margin:10vh auto;}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# 📊 NexaDash")
    st.markdown("**Sign in to access your dashboard.**")
    st.markdown("---")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)
        
        if submitted:
            if username in USERS and USERS[username] == _hash(password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.login_time = datetime.now()
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")
                st.info("Demo credentials: username='admin', password='NexaDash2026!'")

def render_sidebar():
    """Render sidebar with navigation and user info"""
    st.sidebar.markdown("## Menu")
    page = st.sidebar.radio('Navigation', 
        ['Home', 'Dashboard', 'Analytics', 'Projects', 'Settings', 'Reports'],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown('---')
    
    # User info
    user_col1, user_col2 = st.sidebar.columns([2, 1])
    with user_col1:
        st.sidebar.markdown(f"**{st.session_state.username.capitalize()}**")
        st.sidebar.caption(f"Plan: {USER_PLANS.get(st.session_state.username, 'Pro')}")
    
    with user_col2:
        if st.sidebar.button('🚪 Sign Out', use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.login_time = None
            st.rerun()
    
    return page

def get_chart_template():
    """Return common chart styling"""
    return {
        'paper_bgcolor': '#1e2130',
        'plot_bgcolor': '#1e2130',
        'font': dict(color='#aaa', family='Arial'),
        'margin': dict(l=20, r=20, t=20, b=20),
        'hovermode': 'x unified'
    }

def generate_time_series(days=30, base=40000, noise_range=(2000, 5000)):
    """Generate realistic time series data"""
    return np.cumsum(np.random.randint(noise_range[0], noise_range[1], days)) + base

# Main App Logic
if not st.session_state.authenticated:
    login_page()
    st.stop()

# Authenticated App
np.random.seed(42)

page = render_sidebar()

if page == 'Home':
    st.title(f'👋 Welcome back, {st.session_state.username.capitalize()}!')
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('💰 Revenue', '$84,320', '+12.4%', delta_color="off")
    col2.metric('👥 Active Users', '14,892', '+8.1%', delta_color="off")
    col3.metric('📈 Conversion', '3.72%', '+0.5%', delta_color="off")
    col4.metric('⏱️ Avg Session', '4m 12s', '+22s', delta_color="off")
    
    st.markdown('---')
    
    # Revenue Trend Chart
    st.subheader('💹 Revenue Trend')
    days = list(range(1, 31))
    rev = generate_time_series()
    
    fig = go.Figure(go.Scatter(
        x=days, 
        y=rev, 
        fill='tozeroy', 
        name='Revenue',
        line=dict(color='#7c83fd', width=2),
        fillcolor='rgba(124,131,253,0.15)'
    ))
    fig.update_layout(get_chart_template())
    fig.update_xaxes(gridcolor='#2d3250')
    fig.update_yaxes(gridcolor='#2d3250')
    st.plotly_chart(fig, use_container_width=True)
    
    # Quick Stats
    st.subheader('📊 Quick Stats')
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.info('🔔 **3** notifications pending')
    with stat_col2:
        st.success('✅ **12** tasks completed today')
    with stat_col3:
        st.warning('⚠️ **2** issues need attention')

elif page == 'Dashboard':
    st.title('📋 Dashboard')
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('💰 Revenue', '$84,320', '+12.4%', delta_color="off")
    col2.metric('👥 Active Users', '14,892', '+8.1%', delta_color="off")
    col3.metric('📈 Conversion', '3.72%', '+0.5%', delta_color="off")
    col4.metric('✨ Uptime', '99.97%', '+0.01%', delta_color="off")
    
    st.markdown('---')
    
    # Charts Row
    L, R = st.columns([2, 1])
    
    with L:
        st.subheader('📈 Monthly Revenue')
        days = list(range(1, 31))
        rev = generate_time_series()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=days, 
            y=rev, 
            fill='tozeroy', 
            name='Revenue',
            line=dict(color='#7c83fd', width=2),
            fillcolor='rgba(124,131,253,0.15)'
        ))
        fig.add_trace(go.Scatter(
            x=days, 
            y=np.linspace(rev[0], rev[-1]*1.1, 30),
            name='Target', 
            line=dict(color='#3fb950', dash='dash')
        ))
        fig.update_layout(get_chart_template())
        fig.update_xaxes(gridcolor='#2d3250')
        fig.update_yaxes(gridcolor='#2d3250')
        st.plotly_chart(fig, use_container_width=True)
    
    with R:
        st.subheader('🚀 Traffic Sources')
        fig2 = go.Figure(go.Pie(
            labels=['Organic', 'Paid', 'Referral', 'Social', 'Direct'],
            values=[38, 27, 15, 12, 8],
            hole=0.55,
            marker=dict(colors=['#7c83fd','#3fb950','#f78166','#e3b300','#79c0ff'])
        ))
        fig2.update_layout({
            'paper_bgcolor': '#1e2130',
            'font': dict(color='#aaa'),
            'margin': dict(l=10, r=10, t=10, b=10)
        })
        st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader('💳 Recent Transactions')
    transactions_df = pd.DataFrame({
        'Date': ['May 10', 'May 9', 'May 9', 'May 8', 'May 7'],
        'User': ['Alice M.', 'Bob K.', 'Carol T.', 'Dan R.', 'Eve S.'],
        'Plan': ['Pro', 'Team', 'Pro', 'Starter', 'Team'],
        'Amount': ['$2,450', '$1,980', '$2,450', '$499', '$1,980'],
        'Status': ['✅ Completed', '✅ Completed', '⏳ Processing', '✅ Completed', '✅ Completed']
    })
    st.dataframe(transactions_df, use_container_width=True, hide_index=True)

elif page == 'Analytics':
    st.title('📊 Analytics')
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    st.markdown('---')
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('👥 Daily Active Users')
        days = list(range(1, 31))
        dau = np.random.randint(8000, 16000, 30)
        
        fig = go.Figure(go.Bar(
            x=days, 
            y=dau, 
            marker_color='#7c83fd',
            name='DAU'
        ))
        fig.update_layout(get_chart_template())
        fig.update_xaxes(gridcolor='#2d3250')
        fig.update_yaxes(gridcolor='#2d3250')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader('📉 User Retention')
        fig2 = go.Figure(go.Scatter(
            x=['Wk1', 'Wk2', 'Wk3', 'Wk4'],
            y=[100, 68, 52, 43],
            mode='lines+markers',
            line=dict(color='#3fb950', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            name='Retention %'
        ))
        fig2.update_layout(get_chart_template())
        fig2.update_yaxes(range=[0, 110], gridcolor='#2d3250')
        fig2.update_xaxes(gridcolor='#2d3250')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Additional Analytics
    st.subheader('🔍 Detailed Metrics')
    analytics_col1, analytics_col2, analytics_col3 = st.columns(3)
    
    with analytics_col1:
        st.metric("Bounce Rate", "42.3%", "-2.1%", delta_color="off")
    with analytics_col2:
        st.metric("Avg Page Load", "1.23s", "-0.15s", delta_color="off")
    with analytics_col3:
        st.metric("Mobile Traffic", "68%", "+5.2%", delta_color="off")

elif page == 'Projects':
    st.title('🎯 Projects')
    
    projects = [
        ('NexaDash v2.0', 78, 'On Track', '🟢'),
        ('Mobile Redesign', 45, 'In Progress', '🟡'),
        ('API Integration', 91, 'Almost Done', '🟢'),
        ('Marketing Campaign', 33, 'Delayed', '🔴'),
        ('Data Pipeline', 60, 'On Track', '🟢'),
    ]
    
    for name, pct, status, icon in projects:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{icon} {name}** - {status}")
            st.progress(pct / 100)
        with col2:
            st.metric("Progress", f"{pct}%", label_visibility="collapsed")
        st.markdown("---")

elif page == 'Settings':
    st.title('⚙️ Settings')
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Profile", "Preferences", "Security"])
    
    with tab1:
        st.subheader("Profile Settings")
        with st.form("profile_form"):
            name = st.text_input("Name", value=st.session_state.username.capitalize())
            email = st.text_input("Email", value="hassonshareef@gmail.com")
            bio = st.text_area("Bio", value="Data enthusiast and dashboard builder")
            
            if st.form_submit_button("✅ Save Profile", use_container_width=True):
                st.success("Profile updated successfully!")
    
    with tab2:
        st.subheader("Preferences")
        with st.form("preferences_form"):
            theme = st.selectbox("Theme", ["Dark", "Light"], index=0)
            notifications = st.toggle("Email Notifications", value=True)
            auto_refresh = st.toggle("Auto-refresh Data", value=True)
            refresh_interval = st.slider("Refresh Interval (seconds)", 10, 300, 60)
            
            if st.form_submit_button("✅ Save Preferences", use_container_width=True):
                st.success("Preferences updated successfully!")
    
    with tab3:
        st.subheader("Security")
        st.info("🔒 Your account is secure with 2FA enabled.")
        
        with st.form("security_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("✅ Change Password", use_container_width=True):
                if new_password == confirm_password:
                    st.success("Password changed successfully!")
                else:
                    st.error("Passwords do not match!")

elif page == 'Reports':
    st.title('📄 Reports')
    
    report_type = st.selectbox(
        "Select Report Type",
        ["Revenue Summary", "User Activity", "Performance Metrics", "Custom Report"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        report_date = st.date_input("Report Date", value=datetime.now())
    with col2:
        export_format = st.selectbox("Export Format", ["PDF", "CSV", "Excel"])
    
    if st.button("📥 Generate Report", use_container_width=True):
        st.success(f"✅ {report_type} generated successfully!")
        
        # Sample data
        report_data = pd.DataFrame({
            'Metric': ['Revenue', 'Users', 'Conversion', 'Uptime'],
            'Current': ['$84,320', '14,892', '3.72%', '99.97%'],
            'Previous': ['$75,100', '13,750', '3.45%', '99.95%'],
            'Change': ['+12.4%', '+8.1%', '+0.27%', '+0.02%']
        })
        
        st.dataframe(report_data, use_container_width=True, hide_index=True)
        
        with st.expander("📊 Detailed Analysis"):
            st.write("""
            - Revenue increased significantly due to new enterprise clients
            - User growth is consistent with marketing campaigns
            - Conversion rate improved with recent UI updates
            - System uptime remains excellent with 99.97% availability
            """)
