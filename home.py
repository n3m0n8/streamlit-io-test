"""A welcoming, HTML-enhanced homepage for the Streamlit learning app.

This file is registered as a page in main_streamlit.py.
It demonstrates how st.markdown can display a small amount of HTML/CSS.
"""

from textwrap import dedent

import streamlit as st


# Streamlit mostly uses Python widgets. However, st.markdown also supports
# HTML when unsafe_allow_html=True. Use ONLY trusted, fixed HTML here:
# avoid inserting text supplied by site visitors into HTML strings.
st.markdown(
    dedent("""
    <style>
      .learning-hero {
        padding: 2.3rem 2.4rem;
        border-radius: 20px;
        background: linear-gradient(120deg, #11275b 0%, #174a77 65%, #155c70 100%);
        color: #ffffff;
        margin-bottom: 1.5rem;
      }
      .learning-eyebrow {
        font-size: .79rem;
        font-weight: 750;
        letter-spacing: .13em;
        text-transform: uppercase;
        color: #bbe6f7;
        margin: 0 0 .7rem;
      }
      .learning-hero h1 {
        color: #ffffff !important;
        margin: 0 0 .75rem;
        font-size: clamp(2rem, 4vw, 3rem);
        letter-spacing: -.02em;
        line-height: 1.15;
      }
      .learning-hero p { max-width: 720px; color: #e2eef7; font-size: 1.1rem; }
      .learning-pill {
        display: inline-block;
        background: #ffffff1b;
        border: 1px solid #ffffff45;
        border-radius: 50px;
        padding: .45rem .9rem;
        margin-top: .5rem;
        color: #ffffff;
        font-size: .9rem;
      }
      .learning-card {
        background: #f4f8fc;
        border: 1px solid #dbe6ef;
        border-radius: 15px;
        padding: 1.25rem 1.3rem;
        min-height: 182px;
        margin-bottom: .6rem;
      }
      .learning-card h3 { color: #183350; margin: 0 0 .55rem; font-size: 1.2rem; }
      .learning-card p { color: #36516b; font-size: .97rem; line-height: 1.5; }
      .learning-note {
        border-left: 4px solid #1586a0;
        background: #eef8fb;
        border-radius: 8px;
        padding: 1.0rem 1.15rem;
        color: #274457;
        margin: 1.2rem 0;
      }
      @media (max-width: 650px) {
        .learning-hero { padding: 1.5rem; }
        .learning-hero h1 { font-size: 2rem; }
      }
    </style>

    <section class="learning-hero">
      <div class="learning-eyebrow">Your interactive Python learning lab</div>
      <h1>Welcome to Streamlit! 👋</h1>
      <p>
        Learn how to turn Python code into a friendly, interactive web app.
        Explore charts, play with filters, discover maps, and see simple machine
        learning models in action. No web-design experience required.
      </p>
      <span class="learning-pill">🐍 Python first &nbsp; · &nbsp; 📊 Visual learning &nbsp; · &nbsp; 🧠 Beginner friendly</span>
    </section>
    """),
    unsafe_allow_html=True,
)

st.subheader("Choose something to explore")
st.write("Use the navigation menu on the left to open any of the example pages.")

# st.columns is Streamlit's native layout tool. Each HTML 'card' is rendered
# inside one column, keeping the page simple and responsive.
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        dedent("""
        <div class="learning-card">
          <h3>📊 Data Dashboard</h3>
          <p>Explore tables, bar charts, line charts, scatter plots, dropdowns,
          sliders, text inputs, and an echo chatbot.</p>
        </div>
        """),
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        dedent("""
        <div class="learning-card">
          <h3>🌍 Maps</h3>
          <p>Put latitude and longitude on a map, change regional price
          filters, and interact with Plotly map markers.</p>
        </div>
        """),
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        dedent("""
        <div class="learning-card">
          <h3>🤖 Machine Learning</h3>
          <p>Discover linear regression and logistic regression with
          made-up datasets, model predictions, and interactive graphs.</p>
        </div>
        """),
        unsafe_allow_html=True,
    )

st.markdown(
    dedent("""
    <div class="learning-note">
      <strong>💡 Tip for learners:</strong> Move a slider, try a filter, or type in
      a box. Notice how Streamlit instantly runs your Python code again to update
      the page. Open the matching <code>.py</code> file to see how it works!
    </div>
    """),
    unsafe_allow_html=True,
)

st.subheader("What you'll practise")
st.markdown(
    dedent("""
    - **Build a page:** Use `st.title`, `st.write`, and `st.markdown`.
    - **Collect user input:** Experiment with sliders, select boxes, and text inputs.
    - **Show data:** Convert JSON records to pandas DataFrames and plot charts.
    - **Explore bigger ideas:** Map geographical coordinates and visualise ML predictions.
    """)
)

st.divider()
st.caption("Streamlit Learning Lab • Example data only • Have fun experimenting!")
