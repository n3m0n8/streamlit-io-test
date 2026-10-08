"""Streamlit page displaying the two machine-learning experiments in ml.py.

Keep data creation, fitting, and figure-building in ml.py. This page focuses
on explaining the models and displaying charts and interactive predictions.
Start the full application with `streamlit run main_streamlit.py`.
"""

# IMPORTS --------------------------------------------------------------------
# Streamlit builds the page, and pandas is not needed here because ml.py
# already returns its results as DataFrames.
import streamlit as st

# Import the functions we wrote in ml.py. This is a useful beginner example
# of splitting a larger project into small reusable modules.
from ml import run_linear_regression, run_logistic_regression


# PAGE HEADING ---------------------------------------------------------------
st.title("🤖 Machine Learning Playground")
st.write(
    "Two small examples show how machine-learning models find patterns in "
    "made-up student data. Read the comments in **ml.py** for the calculations "
    "and in **ml_visuals.py** for how these graphs appear on the page."
)
st.info("All values and outcomes are synthetic. These are learning demos, not student assessments.")


# MODEL 1: LINEAR REGRESSION --------------------------------------------------
st.header("1. Linear regression · predicting a number")
st.write(
    "**Question:** Can we predict an exam score from hours of revision? "
    "The dots show invented observations, and the straight line is the "
    "model's best-fitting prediction."
)

# Calling the function runs the example and returns a dictionary of results.
linear = run_linear_regression()

# st.plotly_chart can display a Plotly figure built in a DIFFERENT Python file.
st.plotly_chart(linear["figure"], use_container_width=True)

# Columns make two small metrics sit side by side.
metric_one, metric_two = st.columns(2)
metric_one.metric("Training R²", f"{linear['training_r2']:.2f}")
metric_two.metric("Approximate points gained per hour", f"{linear['slope']:.1f}")

# A slider lets the visitor give a NEW input to the trained linear model.
hours_for_score = st.slider(
    "Try a revision time (hours)", 0.0, 10.0, 5.0, 0.5, key="linear_hours"
)

# .predict expects a 2D input: [[5.0]] means one learner, one feature.
estimated_score = float(linear["model"].predict([[hours_for_score]])[0])
st.success(f"Predicted exam score: **{estimated_score:.1f} / 100**")

with st.expander("View the linear regression dummy data"):
    st.dataframe(linear["data"], use_container_width=True, hide_index=True)

st.caption(
    "R² here describes fit on the same data used to train the model. "
    "A serious evaluation would also use held-out test data."
)

st.divider()


# MODEL 2: LOGISTIC REGRESSION ------------------------------------------------
st.header("2. Logistic regression · predicting a yes/no outcome")
st.write(
    "**Question:** How likely is an imaginary learner to pass, based on "
    "revision hours? The dots show made-up outcomes (0 = fail, 1 = pass), "
    "while the S-shaped curve estimates the probability of passing."
)

# As before, ml.py takes care of generating data and fitting the model.
logistic = run_logistic_regression()
st.plotly_chart(logistic["figure"], use_container_width=True)

st.metric("Training classification accuracy", f"{logistic['training_accuracy']:.0%}")

# This slider is independent of the linear regression slider above.
hours_for_pass = st.slider(
    "Try another revision time (hours)", 0.0, 10.0, 5.0, 0.5,
    key="logistic_hours",
)

# predict_proba returns [P(fail), P(pass)] for each input example.
probability_of_pass = float(
    logistic["model"].predict_proba([[hours_for_pass]])[0, 1]
)

# The default decision rule chooses 'pass' at probability >= 0.5.
classification = "Pass (1)" if probability_of_pass >= 0.5 else "Fail (0)"

result_left, result_right = st.columns(2)
result_left.metric("Estimated pass probability", f"{probability_of_pass:.1%}")
result_right.metric("Predicted class (50% cutoff)", classification)

with st.expander("View the logistic regression dummy data"):
    st.dataframe(logistic["data"], use_container_width=True, hide_index=True)

st.caption(
    "Training accuracy measures predictions on the model's own training "
    "examples, so it may be optimistic. These probabilities are illustrative."
)

st.divider()
st.markdown(
    "**What to remember:** Linear regression predicts a **continuous number** "
    "such as a score. Logistic regression predicts a **class probability**, "
    "which can be converted into a **yes/no class** using a cutoff."
)
