import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="NexaDash", page_icon="", layout="wide")

st.markdown("""
>style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background-color: #0f1117; }
.block-container { padding-top: 1.5rem; }
.metric-card {
    background: linear-gradient(135deg, #1e2130, #252840);
        border-radius: 12px;
            padding: 20px;
                border: 1px solid #2d3250;
                    text-align: center;
                    }
                    .metric-value { font-size: 2rem; font-weight: 700; color: #7c83fd; }
                    .metric-label { font-size: 0.85rem; color: #8892b0; margin-top: 4px; }
                    .metric-delta { font-size: 0.8rem; color: #3fb950; margin-top: 6px; }
                    >/style>
                    """, unsafe_allow_html=True)

pages = ["Home", "Dashboard", "Analytics", "Projects", "Settings"]
page = st.sidebar.radio("Navigation", pages, index=1)
st.sidebar.markdown("---")
st.sidebar.markdown("**Logged in as:** Hass")
st.sidebar.markdown("**Plan:** Pro")

days = list(range(1, 31))
np.random.seed(42)

if page == "Home":
              st.title("Welcome back, Hass ")
              st.markdown("Here's a quick overview of your workspace.")
              col1, col2, col3, col4 = st.columns(4)
              metrics = [
                  ("Total Revenue", "$84,320", "+12.4%"),
                  ("Active Users", "14,892", "+8.1%"),
                  ("Conversion Rate", "3.72%", "+0.5%"),
                  ("Avg. Session", "4m 12s", "+22s"),
              ]
              for col, (label, value, delta) in zip([col1, col2, col3, col4], metrics):
                                with col:
                                                      st.markdown(f"""
                                                                  >div class="metric-card">
                                                                                  >div class="metric-value">{value}>/div>
                                                                                                  >div class="metric-label">{label}>/div>
                                                                                                                  >div class="metric-delta">{delta} this month>/div>
                                                                                                                              >/div>
                                                                                                                                          """, unsafe_allow_html=True)

elif page == "Dashboard":
              st.title("Dashboard")
              st.markdown("Live performance overview")
              col1, col2, col3, col4 = st.columns(4)
              metrics = [
                  ("Total Revenue", "$84,320", "+12.4%"),
                  ("Active Users", "14,892", "+8.1%"),
                  ("Conversion Rate", "3.72%", "+0.5%"),
                  ("Avg. Session", "4m 12s", "+22s"),
              ]
              for col, (label, value, delta) in zip([col1, col2, col3, col4], metrics):
                                with col:
                                                      st.markdown(f"""
                                                                  >div class="metric-card">
                                                                                  >div class="metric-value">{value}>/div>
                                                                                                  >div class="metric-label">{label}>/div>
                                                                                                                  >div class="metric-delta">{delta} vs last month>/div>
                                                                                                                              >/div>
                                                                                                                                          """, unsafe_allow_html=True)
                                              st.markdown("---")
                            col_left, col_right = st.columns([2, 1])
    with col_left:
                      st.subheader("Monthly Revenue")
                      rev = np.cumsum(np.random.randint(2000, 5000, 30)) + 40000
                      fig = go.Figure()
                      fig.add_trace(go.Scatter(x=days, y=rev, mode="lines", fill="tozeroy", name="Revenue", line=dict(color="#7c83fd", width=2), fillcolor="rgba(124,131,253,0.15)"))
                      target = np.linspace(rev[0], rev[-1] * 1.1, 30)
                      fig.add_trace(go.Scatter(x=days, y=target, mode="lines", name="Target", line=dict(color="#3fb950", width=1, dash="dash")))
                      fig.update_layout(paper_bgcolor="#1e2130", plot_bgcolor="#1e2130", font=dict(color="#8892b0"), margin=dict(l=20, r=20, t=20, b=20), legend=dict(bgcolor="#1e2130"), xaxis=dict(gridcolor="#2d3250"), yaxis=dict(gridcolor="#2d3250"))
                      st.plotly_chart(fig, use_container_width=True)
                  with col_right:
                                    st.subheader("Traffic Sources")
                                    labels = ["Organic", "Paid", "Referral", "Social", "Direct"]
                                    values = [38, 27, 15, 12, 8]
                                    fig2 = go.Figure(go.Pie(labels=labels, values=values, hole=0.55, marker=dict(colors=["#7c83fd", "#3fb950", "#f78166", "#e3b341", "#58a6ff"])))
                                    fig2.update_layout(paper_bgcolor="#1e2130", font=dict(color="#8892b0"), margin=dict(l=10, r=10, t=10, b=10), showlegend=True, legend=dict(bgcolor="#1e2130"))
                                    st.plotly_chart(fig2, use_container_width=True)
                                st.subheader("Recent Transactions")
    df = pd.DataFrame({"Date": ["May 10", "May 9", "May 9", "May 8", "May 7"], "User": ["Alice M.", "Bob K.", "Carol T.", "Dan R.", "Eve S."], "Plan": ["Pro", "Team", "Pro", "Starter", "Team"], "Amount": ["$49", "$149", "$49", "$19", "$149"], "Status": ["Paid", "Paid", "Paid", "Pending", "Paid"]})
    st.dataframe(df, use_container_width=True)

elif page == "Analytics":
    st.title("Analytics")
    st.markdown("Deep-dive metrics and trends")
    col1, col2 = st.columns(2)
    with col1:
                      st.subheader("Daily Active Users")
                      dau = np.random.randint(8000, 16000, 30)
                      fig = go.Figure(go.Bar(x=days, y=dau, marker_color="#7c83fd", marker_line_color="#5a61e0", marker_line_width=1))
                      fig.update_layout(paper_bgcolor="#1e2130", plot_bgcolor="#1e2130", font=dict(color="#8892b0"), margin=dict(l=20, r=20, t=20, b=20), xaxis=dict(gridcolor="#2d3250"), yaxis=dict(gridcolor="#2d3250"))
                      st.plotly_chart(fig, use_container_width=True)
                  with col2:
                                    st.subheader("Retention Rate (%)")
                                    cohorts = ["Week 1", "Week 2", "Week 3", "Week 4"]
                                    retention = [100, 68, 52, 43]
                                    fig2 = go.Figure(go.Scatter(x=cohorts, y=retention, mode="lines+markers", line=dict(color="#3fb950", width=3), marker=dict(size=10, color="#3fb950")))
                                    fig2.update_layout(paper_bgcolor="#1e2130", plot_bgcolor="#1e2130", font=dict(color="#8892b0"), margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(range=[0, 110], gridcolor="#2d3250"), xaxis=dict(gridcolor="#2d3250"))
                                    st.plotly_chart(fig2, use_container_width=True)

elif page == "Projects":
    st.title("Projects")
    st.markdown("Track progress across all active projects")
    projects = [
                      ("NexaDash v2.0", 78, "On Track"),
                      ("Mobile App Redesign", 45, "In Progress"),
                      ("API Integration", 91, "Almost Done"),
                      ("Marketing Campaign", 33, "Delayed"),
                      ("Data Pipeline", 60, "On Track"),
    ]
    for name, pct, status in projects:
                      st.markdown(f"**{name}**  {status} ({pct}%)")
                      st.progress(pct / 100)
                      st.markdown("")

elif page == "Settings":
    st.title("Settings")
    st.markdown("Manage your account preferences")
    with st.form("settings_form"):
                      st.text_input("Display Name", value="Hass")
                      st.text_input("Email", value="hassonshareef@gmail.com")
                      st.selectbox("Theme", ["Dark", "Light", "System"])
                      st.selectbox("Timezone", ["Eastern (UTC-5)", "Pacific (UTC-8)", "UTC"])
                      st.toggle("Email Notifications", value=True)
                      st.toggle("Weekly Digest", value=False)
                      submitted = st.form_submit_button("Save Changes")
                      if submitted:
                                            st.success("Settings saved!")
