"""Map examples for beginners using st.map and Plotly's scatter_map.

This is a Streamlit PAGE, not an app entry point. Start the app with:
    streamlit run main_streamlit.py
"""

# IMPORTS --------------------------------------------------------------------
# NumPy is used to generate the first map's random points.
import numpy as np

# pandas stores map coordinates and regional statistics in table form.
import pandas as pd

# Plotly Express is a high-level library for interactive plots and maps.
import plotly.express as px

# Streamlit provides the controls and displays the maps in a browser.
import streamlit as st


# SECTION 1: A SIMPLE STREAMLIT MAP ------------------------------------------
st.title("🌍 Learning to build maps")
st.write(
    "Compare Streamlit's quick built-in map with a more configurable "
    "interactive Plotly map. All values on this page are for demonstration."
)

st.subheader("1. A simple map with `st.map()`")

# random.default_rng(seed=...) makes the points reproducible. Every learner
# will see the same map, even when Streamlit reruns the page.
rng = np.random.default_rng(seed=42)

# np.random.normal creates a collection of values around a chosen mean.
# We center the example points near 51.06°N, 1.30°W (southern England).
# NumPy returns two arrays, one for latitude and one for longitude.
latitudes = rng.normal(loc=65.06, scale=0.05, size=200)
longitudes = rng.normal(loc=-19.30, scale=0.035, size=200)

# A DataFrame with columns named 'lat' and 'lon' is all st.map needs.
map_data = pd.DataFrame({"lat": latitudes, "lon": longitudes})

# st.map automatically builds a map and places one point for each row.
st.map(map_data)

with st.expander("Show five example coordinates"):
    # .head(5) means 'the first five rows' of the DataFrame.
    st.dataframe(map_data.head(5), hide_index=True, use_container_width=True)

st.divider()


# SECTION 2: AN INTERACTIVE FRENCH REGIONS MAP -------------------------------
st.subheader("2. French regional house prices with Plotly")
st.caption(
    "Teaching-only example: the prices, transaction counts, and map markers "
    "below are illustrative, not official property market statistics. "
    "Coordinates are approximate regional reference points."
)

# A Python list of dictionaries is an easy way to write a small dataset.
# Each dictionary represents a French region with four attributes:
# region = label; lat/lon = map location; avg_price_sqm = invented price;
# transactions = invented total used to determine marker size.
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

# Convert the records to a DataFrame because Plotly understands pandas tables.
df_france = pd.DataFrame(france_data)

# Streamlit sliders rerun the script when their value changes.
# This one selects the highest price the learner wants to see.
max_price = st.slider(
    "Show regions with an average price at or below (€ per m²)",
    min_value=1500,
    max_value=10000,
    value=10000,
    step=250,
)

# Filter only the rows that satisfy the condition. The <= symbol means 'less
# than or equal to'. This is a useful first example of pandas filtering.
filtered_df = df_france[df_france["avg_price_sqm"] <= max_price]

# Always tell the learner how many regions remain after the filter.
st.caption(f"Showing {len(filtered_df)} of {len(df_france)} regions.")

if filtered_df.empty:
    st.warning("No regions match the selected price. Increase the maximum.")
else:
    # Plotly's scatter_map draws an interactive circular marker for each row.
    # lat/lon point to the columns containing geographical coordinates.
    # size controls circle sizes; color controls their colour on the map.
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
        hover_data={
            "lat": False,            # Hide coordinates in hover tooltips.
            "lon": False,
            "avg_price_sqm": ":,.0f",  # Format a price with separators.
            "transactions": ":,d",    # Show transaction count as an integer.
        },
        labels={
            "avg_price_sqm": "Price (€ / m²)",
            "transactions": "Transactions",
        },
    )

    # Remove unused margins and set a comfortable map height.
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=550)

    # Plotly figures need st.plotly_chart to appear in a Streamlit app.
    st.plotly_chart(fig, use_container_width=True)

    # An optional data table shows which points correspond to which values.
    with st.expander("View the regional dataset"):
        st.dataframe(
            filtered_df[["region", "avg_price_sqm", "transactions"]],
            hide_index=True,
            use_container_width=True,
        )

st.divider()

# SECTION 3: DIFFERENT TYPES OF INPUT ----------------------------------------
st.subheader("3. Try date and time inputs")
st.write("These last two widgets demonstrate how Streamlit collects a date and time.")

# Both widgets return Python date/time objects we can use in an application.
chosen_date = st.date_input("Choose a date")
chosen_time = st.time_input("Choose a time")

# This string demonstrates how to display Python values back on the page.
st.info(f"You chose **{chosen_date}** at **{chosen_time.strftime('%H:%M')}**.")
