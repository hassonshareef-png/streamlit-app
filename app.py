import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(page_title='NexaDash', page_icon='📊', layout='wide')
st.markdown('<style>body{background:#0f1117;color:#e0e0e0;}</style>', unsafe_allow_html=True)

page = st.sidebar.radio('Menu', ['Home','Dashboard','Analytics','Projects','Settings'])
st.sidebar.markdown('---')
st.sidebar.markdown('**Hass** Pro Plan')

np.random.seed(42)

if page == 'Home':
    st.title('Welcome back, Hass')
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Revenue', '$84,320', '+12.4%')
    c2.metric('Active Users', '14,892', '+8.1%')
    c3.metric('Conversion', '3.72%', '+0.5%')
    c4.metric('Avg Session', '4m 12s', '+22s')
    st.markdown('---')
    st.subheader('Revenue Trend')
    days = list(range(1, 31))
    rev = np.cumsum(np.random.randint(2000, 5000, 30)) + 40000
    fig = go.Figure(go.Scatter(x=days, y=rev, fill='tozeroy', line=dict(color='#7c83fd', width=2)))
    fig.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130', font=dict(color='#aaa'), margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

elif page == 'Dashboard':
    st.title('Dashboard')
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Revenue', '$84,320', '+12.4%')
    c2.metric('Active Users', '14,892', '+8.1%')
    c3.metric('Conversion', '3.72%', '+0.5%')
    c4.metric('Uptime', '99.97%', '+0.01%')
    st.markdown('---')
    L, R = st.columns([2, 1])
    
    with L:
        st.subheader('Monthly Revenue')
        days = list(range(1, 31))
        rev = np.cumsum(np.random.randint(2000, 5000, 30)) + 40000
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=rev, fill='tozeroy', name='Revenue', line=dict(color='#7c83fd', width=2), fillcolor='rgba(124,131,253,0.15)'))
        fig.add_trace(go.Scatter(x=days, y=np.linspace(rev[0], rev[-1]*1.1, 30), name='Target', line=dict(color='#3fb950', dash='dash')))
        fig.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130', font=dict(color='#aaa'), margin=dict(l=20, r=20, t=20, b=20), xaxis=dict(gridcolor='#2d3250'), yaxis=dict(gridcolor='#2d3250'))
        st.plotly_chart(fig, use_container_width=True)
    
    with R:
        st.subheader('Traffic Sources')
        fig2 = go.Figure(go.Pie(labels=['Organic', 'Paid', 'Referral', 'Social', 'Direct'], values=[38, 27, 15, 12, 8], hole=0.55, marker=dict(colors=['#7c83fd', '#3fb950', '#f78166', '#e3b300', '#79c0ff'])))
        fig2.update_layout(paper_bgcolor='#1e2130', font=dict(color='#aaa'), margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader('Recent Transactions')
    st.dataframe(pd.DataFrame({'Date':['May 10','May 9','May 9','May 8','May 7'],'User':['Alice M.','Bob K.','Carol T.','Dan R.','Eve S.'],'Plan':['Pro','Team','Pro','Starter','Team'],'Amount':['$2,450','$1,980','$2,450','$499','$1,980']}))

elif page == 'Analytics':
    st.title('Analytics')
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader('Daily Active Users')
        days = list(range(1, 31))
        fig = go.Figure(go.Bar(x=days, y=np.random.randint(8000, 16000, 30), marker_color='#7c83fd'))
        fig.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130', font=dict(color='#aaa'), margin=dict(l=20, r=20, t=20, b=20), xaxis=dict(gridcolor='#2d3250'), yaxis=dict(gridcolor='#2d3250'))
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader('User Retention')
        fig2 = go.Figure(go.Scatter(x=['Wk1','Wk2','Wk3','Wk4'], y=[100, 68, 52, 43], mode='lines+markers', line=dict(color='#3fb950', width=3), marker=dict(size=10)))
        fig2.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130', font=dict(color='#aaa'), margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(range=[0, 110], gridcolor='#2d3250'), xaxis=dict(gridcolor='#2d3250'))
        st.plotly_chart(fig2, use_container_width=True)

elif page == 'Projects':
    st.title('Projects')
    for name, pct, status in [('NexaDash v2.0', 78, 'On Track'), ('Mobile Redesign', 45, 'In Progress'), ('API Integration', 91, 'Almost Done'), ('Marketing Campaign', 33, 'Delayed'), ('Data Pipeline', 60, 'On Track')]:
        st.markdown(f'**{name}** _{status}_ ({pct}%)')
        st.progress(pct/100)

elif page == 'Settings':
    st.title('Settings')
    with st.form('s'):
        st.text_input('Name', value='Hass')
        st.text_input('Email', value='hassonshareef@gmail.com')
        st.selectbox('Theme', ['Dark', 'Light'])
        st.toggle('Email Alerts', value=True)
        if st.form_submit_button('Save'):
            st.success('Saved!')
