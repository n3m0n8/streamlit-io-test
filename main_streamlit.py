"""Entry point for a beginner-friendly, multi-page Streamlit learning app.

Start the whole app by running:
    streamlit run main_streamlit.py

This file teaches three ideas:
1. Setting up a Streamlit application and its navigation.
2. Reading JSON data and building a simple data dashboard.
3. Using common Streamlit widgets, charts, layouts, and chat messages.
"""

# IMPORTS --------------------------------------------------------------------
# json is included with Python. It lets us read data stored in a .json file.
import json

# Path helps locate our JSON file relative to THIS script, not the terminal's
# current working directory. This makes the project easier to move or share.
from pathlib import Path

# numpy provides useful tools for creating example numbers.
import numpy as np

# pandas turns lists of records into DataFrames (spreadsheet-like tables).
import pandas as pd

# streamlit (commonly nicknamed "st") creates the web interface from Python.
import streamlit as st


# PAGE CONFIGURATION ----------------------------------------------------------
# This MUST come before any other st.* command that builds the interface.
# A wide layout gives our charts a little more room.
st.set_page_config(
    page_title="Explore Streamlit | Learning Lab",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# LOADING SAMPLE DATA ---------------------------------------------------------
@st.cache_data
# st.cache_data saves the result after the first run. Streamlit reruns scripts
# when widgets change, so caching avoids reopening an unchanged file each time.
def load_products() -> pd.DataFrame:
    """Read the supplied dummy2.json file and return its products as a table."""

    # __file__ refers to main_streamlit.py, wherever the folder is stored.
    file_path = Path(__file__).resolve().parent / "dummy2.json"

    # 'with' automatically closes the file as soon as we finish reading it.
    with file_path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    # The uploaded JSON contains a 'products' list, NOT sales/time-series keys.
    # Each dictionary in this list becomes one row in our pandas DataFrame.
    products = pd.DataFrame(raw_data["products"])

    # Convert columns we want to graph into numeric values for safety.
    # If a number cannot be read, errors='coerce' changes it to a missing value.
    for column in ["price", "rating", "stock"]:
        products[column] = pd.to_numeric(products[column], errors="coerce")

    return products


# DASHBOARD PAGE --------------------------------------------------------------
# The function below describes one PAGE of the app. Putting the dashboard
# inside a function is important: when the learner visits Home or Maps, these
# dashboard elements will not also appear under the selected page.
def show_dashboard() -> None:
    """Display example charts, filters, inputs, and a tiny echo chatbot."""

    st.title("📊 Data Dashboard")
    st.write(
        "Explore charts and interactive widgets using the product records "
        "supplied in `dummy2.json`."
    )

    # First, fetch the source data. @st.cache_data keeps this efficient.
    products = load_products()

    # SIDEBAR FILTERS --------------------------------------------------------
    # Widgets return values that Python can use just like ordinary variables.
    st.sidebar.header("🔎 Dashboard filters")

    # The list of categories is created from the JSON instead of being typed
    # manually, so it will adjust if the data is changed later.
    categories = sorted(products["category"].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox(
        "Product category", ["All categories"] + categories
    )

    # A slider returns an integer between min_value and max_value.
    min_stock = st.sidebar.slider(
        "Minimum stock level", min_value=0, max_value=100, value=0
    )

    # This button gives the learner another way to interact with the sidebar.
    show_raw_data = st.sidebar.checkbox("Show the product data", value=False)

    # Make an independent copy to avoid changing our original cached data.
    filtered = products.copy()

    # Use the selected values to filter the data BEFORE making charts.
    if selected_category != "All categories":
        filtered = filtered[filtered["category"] == selected_category]
    filtered = filtered[filtered["stock"] >= min_stock]

    # This is a useful example of a formatted string, or 'f-string'.
    st.sidebar.info(
        f"Category: **{selected_category}**  \n"
        f"Minimum stock: **{min_stock}**"
    )

    # DASHBOARD METRICS ------------------------------------------------------
    # st.columns arranges content horizontally; st.metric highlights a value.
    first, second, third = st.columns(3)
    first.metric("Products shown", len(filtered))
    second.metric("Average price", f"${filtered['price'].mean():,.2f}" if not filtered.empty else "—")
    third.metric("Average rating", f"{filtered['rating'].mean():.2f} / 5" if not filtered.empty else "—")

    if show_raw_data:
        # st.dataframe is scrollable and lets the learner sort its columns.
        st.dataframe(
            filtered[["title", "category", "price", "rating", "stock"]],
            use_container_width=True,
            hide_index=True,
        )

    # Display a friendly message instead of showing broken charts if a learner
    # chooses filters that produce zero rows.
    if filtered.empty:
        st.warning("No products meet those filters. Try lowering the stock level.")
    else:
        st.subheader("📦 Explore the product data")
        st.caption("All four charts below update when you use the sidebar filters.")

        # groupby collects products into categories; mean gives the average.
        price_by_category = (
            filtered.groupby("category")["price"].mean().sort_values()
        )

        # The 'with' statement puts each chart INSIDE its chosen column.
        chart_left, chart_right = st.columns(2)
        with chart_left:
            st.markdown("**Horizontal bar chart · average price by category**")
            st.bar_chart(price_by_category, horizontal=True)

        with chart_right:
            st.markdown("**Scatter chart · price versus customer rating**")
            st.scatter_chart(
                filtered, x="price", y="rating", color="category"
            )

        # A bar chart is not the only way to view values: here we show the
        # product prices against their IDs as a simple line chart.
        chart_left, chart_right = st.columns(2)
        with chart_left:
            st.markdown("**Line chart · product prices by product ID**")
            st.line_chart(filtered.sort_values("id").set_index("id")["price"])

        with chart_right:
            st.markdown("**Area chart · stock by category**")
            total_stock = filtered.groupby("category")["stock"].sum()
            st.area_chart(total_stock)

    st.divider()

    # GENERATED EXAMPLE DATA -------------------------------------------------
    # Not every demonstration needs a JSON file. In this section we create a
    # reproducible set of numbers to teach data generation and a 2x2 layout.
    st.subheader("🧪 Four-chart layout with generated data")
    st.write("These charts use a separate, made-up numerical dataset.")

    # A seeded random number generator gives us the SAME values on every rerun.
    # This is useful for teaching because the charts do not change unpredictably.
    rng = np.random.default_rng(seed=42)

    # A DataFrame is a collection of named columns, similar to a spreadsheet.
    demo_data = pd.DataFrame(
        {
            "time_step": range(1, 51),
            "metric_a": rng.normal(size=50).cumsum(),
            "metric_b": rng.normal(size=50).cumsum() + 20,
            "metric_c": rng.integers(10, 100, size=50),
            "metric_d": rng.uniform(0, 100, size=50),
        }
    )

    # expander hides extra detail until a learner wants to inspect it.
    with st.expander("View the generated dataset"):
        st.dataframe(demo_data, use_container_width=True, hide_index=True)

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown("**1. Line trend**")
        st.line_chart(demo_data.set_index("time_step")["metric_a"])
    with row1_col2:
        st.markdown("**2. Bar comparison**")
        st.bar_chart(demo_data.set_index("time_step")["metric_b"])

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.markdown("**3. Area volume**")
        st.area_chart(demo_data.set_index("time_step")["metric_c"])
    with row2_col2:
        st.markdown("**4. Scatter distribution**")
        st.scatter_chart(demo_data, x="time_step", y="metric_d")

    st.divider()

    # TEXT INPUTS AND CHOICE WIDGETS ----------------------------------------
    st.subheader("💬 Experiment with input widgets")
    name = st.text_input("What's your name?", placeholder="Your name")
    feedback = st.text_area("Write some feedback about the dashboard")
    choice = st.radio(
        "Choose your favourite chart",
        ["Line", "Bar", "Area", "Scatter"],
        horizontal=True,
    )

    # Only show the greeting when the learner has entered something.
    if name.strip():
        st.success(f"Welcome, {name.strip()}! You selected the {choice.lower()} chart.")
    if feedback.strip():
        # We display feedback locally; this example does not save or send it.
        st.caption(f"Preview of your feedback: {feedback.strip()}")

    st.divider()

    # SESSION STATE AND CHAT -------------------------------------------------
    st.subheader("🤖 A tiny echo chatbot")
    st.caption(
        "The bot simply repeats what you type. This demonstrates Streamlit's "
        "chat widgets; it is not connected to an AI service."
    )

    # Session state preserves values across widget-triggered reruns.
    # We use a unique key so this chat can coexist with other app features.
    if "dashboard_messages" not in st.session_state:
        st.session_state.dashboard_messages = []

    # Render all messages already stored in session state.
    for message in st.session_state.dashboard_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # The ':=' operator both receives the new message and checks if one exists.
    if prompt := st.chat_input("Ask the echo bot something"):
        st.session_state.dashboard_messages.append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        # A real AI app would call a model here; ours just mirrors the input.
        response = f"Echo: {prompt}"
        st.session_state.dashboard_messages.append(
            {"role": "assistant", "content": response}
        )
        with st.chat_message("assistant"):
            st.markdown(response)

    st.divider()
    st.caption(
        "Learning tip: edit a chart or widget in main_streamlit.py, "
        "save the file, then see the browser update automatically."
    )


# MULTI-PAGE NAVIGATION -------------------------------------------------------
# st.Page accepts either a separate Python file or a function defined here.
# Home, Maps and ML Visuals have their own files. The dashboard lives in the
# show_dashboard() function above, so this file stays the app's entry point.
pages = [
    st.Page("home.py", title="Home", icon="🏠", default=True),
    st.Page(show_dashboard, title="Data Dashboard", icon="📊"),
    st.Page("maps.py", title="Maps", icon="🌍"),
    st.Page("ml_visuals.py", title="Machine Learning", icon="🤖"),
]

# st.navigation builds the page selector in the sidebar.
selected_page = st.navigation(pages)

# Only the selected page runs, preventing different pages from overlapping.
selected_page.run()
