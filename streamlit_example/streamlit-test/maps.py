import numpy as np
import pandas as pd
import streamlit as st
import json 
import plotly.express as px

#map data 


# Dummy data for French regions with coordinates (approximate regional centers)
france_data = [
    {"region": "Île-de-France", "lat": 48.8566, "lon": 2.3522, "avg_price_sqm": 9450, "transactions": 145000},
    {"region": "Provence-Alpes-Côte d'Azur", "lat": 43.9352, "lon": 6.0679, "avg_price_sqm": 4200, "transactions": 98000},
    {"region": "Auvergne-Rhône-Alpes", "lat": 45.4414, "lon": 4.3872, "avg_price_sqm": 3150, "transactions": 112000},
    {"region": "Nouvelle-Aquitaine", "lat": 45.8336, "lon": 0.8485, "avg_price_sqm": 2980, "transactions": 105000},
    {"region": "Occitanie", "lat": 43.6047, "lon": 1.4442, "avg_price_sqm": 2650, "transactions": 92000},
    {"region": "Bretagne", "lat": 48.2020, "lon": -2.9326, "avg_price_sqm": 2750, "transactions": 78000},
    {"region": "Grand Est", "lat": 48.6996, "lon": 6.1862, "avg_price_sqm": 2100, "transactions": 65000},
    {"region": "Hauts-de-France", "lat": 50.6292, "lon": 3.0573, "avg_price_sqm": 2250, "transactions": 70000},
    {"region": "Normandie", "lat": 49.1829, "lon": -0.3707, "avg_price_sqm": 2400, "transactions": 54000},
    {"region": "Pays de la Loire", "lat": 47.4784, "lon": -0.5632, "avg_price_sqm": 2850, "transactions": 83000},
    {"region": "Bourgogne-Franche-Comté", "lat": 47.2805, "lon": 5.0415, "avg_price_sqm": 1850, "transactions": 41000},
    {"region": "Centre-Val de Loire", "lat": 47.9029, "lon": 1.9093, "avg_price_sqm": 2050, "transactions": 49000},
]

df_france = pd.DataFrame(france_data)


#maps

st.subheader("Map")

map_data = pd.DataFrame(
  np.random.randn(200,2) / [20,30] + [51.06, -1.3],
  columns = ['lat','lon']
)
st.map(map_data)


st.title("🇫🇷 French Regional House Prices Demo")

# Slider filter for max price
max_price = st.slider("Filter by Max Price (€/sqm)", 1500, 10000, 10000, 250)
filtered_df = df_france[df_france["avg_price_sqm"] <= max_price]

fig = px.scatter_map(
    filtered_df,
    lat="lat",
    lon="lon",
    size="transactions",
    color="avg_price_sqm",
    color_continuous_scale="Viridis",
    size_max=40,
    zoom=5,
    center={"lat": 46.6033, "lon": 1.8883},
    map_style="open-street-map",
    hover_name="region",
    hover_data={"lat": False, "lon": False, "avg_price_sqm": ":,€", "transactions": ":,d"},
    labels={"avg_price_sqm": "Price €/sqm", "transactions": "Volume"},
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Data and time input")
d_o_b = st.date_input("Input data of birth")
time = st.time_input("Choose your preferred time")
