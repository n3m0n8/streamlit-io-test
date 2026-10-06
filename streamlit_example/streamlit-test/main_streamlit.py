import numpy as np
import pandas as pd
import streamlit as st
import json 
import plotly.express as px


pg = st.navigation(
    [
        st.Page("home.py", title="Home", icon="🏠"),
        st.Page("maps.py", title="Maps", icon="🌍"),
    ]
)
pg.run()


# 1. Page Configuration (Wide layout works best for multi-chart dashboards)
st.set_page_config(page_title="Multi-Graph Dashboard", layout="wide")

# Title
st.title("📊 Analytical Dashboard Scaffolding")

#  ---------------------------------------------------------


with open("../dummyData/dummy2.json") as f:
    data = json.load(f)

df_bar = pd.DataFrame(data["regional_performance"])
df_time = pd.DataFrame(data["time_series_volume"])
df_scatter = pd.DataFrame(data["scatter_distribution"])

st.subheader("Horizontal Bar Chart")
st.bar_chart(df_bar.set_index("region")["sales"], horizontal=True)

st.subheader("Line Trend & Area Volume")
st.line_chart(df_time.set_index("date")[["revenue", "cost"]])
st.area_chart(df_time.set_index("date")["volume"])

st.subheader("Scatter Distribution")
st.scatter_chart(df_scatter, x="spend", y="satisfaction", color="segment")



# 2. Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("🔍 Filter Controls")

selected_category = st.sidebar.selectbox(
    "Select Category", ["All", "Region A", "Region B", "Region C"]
)
date_range = st.sidebar.date_input("Date Range", [])
slider_value = st.sidebar.slider("Activity Threshold", 0, 100, 50)

# Mock filter notification in sidebar
st.sidebar.info(f"Active Filter: **{selected_category}** | Threshold: **{slider_value}**")

# ---------------------------------------------------------
# 3. Dummy Data Generation (Replace with your actual data source)
# ---------------------------------------------------------
np.random.seed(42)
df = pd.DataFrame(
    {
        "time_step": range(1, 51),
        "metric_a": np.random.randn(50).cumsum(),
        "metric_b": np.random.randn(50).cumsum() + 20,
        "metric_c": np.random.randint(10, 100, 50),
        "metric_d": np.random.rand(50) * 100,
    }
)

st.table(df)

# ---------------------------------------------------------
# 4. Four-Section Layout (2x2 Grid)
# ---------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
  st.subheader("Section 1: Line Trend")
  st.line_chart(df.set_index("time_step")["metric_a"])

with row1_col2:
  st.subheader("Section 2: Bar Comparison")
  st.bar_chart(df.set_index("time_step")["metric_b"])

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
  st.subheader("Section 3: Area Volume")
  st.area_chart(df.set_index("time_step")["metric_c"])

with row2_col2:
  st.subheader("Section 4: Scatter Distribution")
  st.scatter_chart(df, x="time_step", y="metric_d")

st.subheader("Text Input")
name = st.text_input("Please enter your name")
feeback = st.text_area("write your feedback")

st.subheader("Selectors")
choice = st.radio("Select an option", [
                                        "Option 1",
                                        "Option 2",
                                        "Option 3"
                                      ]
                  )

                     
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = f"Echo: {prompt}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.caption("Tip: Replace native Streamlit charts with Plotly (`st.plotly_chart`) or Altair if you need interactive tooltips and custom styling.")
