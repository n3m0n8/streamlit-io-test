"""Two small machine-learning experiments, with data made inside this file.

This module contains the *machine-learning work*, not Streamlit widgets.
The ml_visuals.py page imports its functions and shows the results in the app.

The examples use scikit-learn (sklearn), a popular Python ML library:
* Linear regression predicts a number (e.g., an exam score).
* Logistic regression predicts a probability for a yes/no event (e.g., passing).

All student records are synthetic. They are not real learners' data.
"""

# IMPORTS --------------------------------------------------------------------
# NumPy generates numbers and turns 1-D arrays into the 2-D shape sklearn uses.
import numpy as np

# pandas gives meaningful names to our example data columns.
import pandas as pd

# Plotly makes interactive graphs that ml_visuals.py can show with Streamlit.
import plotly.express as px
import plotly.graph_objects as go

# These are two different prediction algorithms from scikit-learn.
from sklearn.linear_model import LinearRegression, LogisticRegression


# EXAMPLE 1: LINEAR REGRESSION ------------------------------------------------
def run_linear_regression():
    """Fit a line to synthetic revision hours and exam scores.

    Returns a dictionary containing the table, trained model, chart, and a
    model-fit score. Returning these results lets other pages reuse the work.
    """

    # Use a random-number generator with a fixed seed. This guarantees that
    # the same dummy dataset appears every time the user opens the page.
    rng = np.random.default_rng(seed=7)

    # Feature = input to a model; target = the answer we want to predict.
    # Here, X (revision hours) is our feature and y (exam score) is our target.
    hours = np.linspace(0.5, 10, num=55)

    # We invent a relationship: more study usually leads to a higher score.
    # The random noise mimics real-world variation between students.
    noise = rng.normal(loc=0, scale=6.5, size=hours.size)
    scores = np.clip(28 + 6.0 * hours + noise, 0, 100)

    # Put the values in a labelled table for charts and easy inspection.
    data = pd.DataFrame({"Hours studied": hours, "Exam score": scores})

    # sklearn requires X as a 2-D table with shape (rows, number_of_features).
    # reshape(-1, 1) converts our array to 55 rows and 1 feature column.
    X = hours.reshape(-1, 1)
    y = scores

    # Create the model, then ask it to learn from the example data.
    model = LinearRegression()
    model.fit(X, y)

    # .predict returns a numeric prediction for each input hour value.
    predicted_scores = model.predict(X)

    # R² measures how closely the fitted line explains the observed values.
    # IMPORTANT: this is the TRAINING score, not a test of future performance.
    training_r2 = model.score(X, y)

    # Draw the actual example observations as individual scatterplot dots.
    fig = px.scatter(
        data,
        x="Hours studied",
        y="Exam score",
        title="Linear regression: fitted line and observed scores",
        opacity=0.72,
    )

    # Add the straight line learned by the model on top of the dot plot.
    fig.add_trace(
        go.Scatter(
            x=hours,
            y=predicted_scores,
            mode="lines",
            name="Model prediction",
            line={"color": "#ed7d31", "width": 3},
        )
    )
    fig.update_layout(legend_title_text="")

    # A dictionary makes the output easy to read, e.g. result['figure'].
    return {
        "data": data,
        "model": model,
        "figure": fig,
        "training_r2": training_r2,
        "slope": float(model.coef_[0]),
        "intercept": float(model.intercept_),
    }


# EXAMPLE 2: LOGISTIC REGRESSION ----------------------------------------------
def run_logistic_regression():
    """Fit a probability curve to synthetic hours studied and pass/fail data."""

    # Make a SEPARATE fixed random generator for this dataset.
    rng = np.random.default_rng(seed=21)

    # 120 imaginary students studied between 0 and 10 hours.
    hours = np.linspace(0, 10, num=120)

    # Logistic regression is intended for class labels, typically 0 and 1.
    # To generate dummy labels, we start with a simple sigmoid curve.
    # exp is the exponential function; the expression maps values into 0..1.
    true_probabilities = 1 / (1 + np.exp(-(-5.2 + 1.05 * hours)))

    # For each example student, use the probability to draw a fake outcome.
    # Passing is 1; failing is 0. The curve generates realistic-ish overlap:
    # two students with the same hours may still have different outcomes.
    passed = rng.binomial(n=1, p=true_probabilities)

    # Turn the inputs and outcomes into a named pandas table.
    data = pd.DataFrame({"Hours studied": hours, "Passed (1=yes)": passed})

    # sklearn once again expects a two-dimensional features array.
    X = hours.reshape(-1, 1)
    y = passed

    # Fit a classifier that learns a probability of belonging to class 1.
    model = LogisticRegression(random_state=21)
    model.fit(X, y)

    # .predict produces a 0 or 1 label, using the model's default cutoff (0.5).
    predicted_labels = model.predict(X)

    # Compare labels with the made-up outcomes to calculate the TRAINING
    # accuracy. Do not treat this in-sample metric as a real-world guarantee.
    training_accuracy = float(np.mean(predicted_labels == y))

    # Create many evenly spaced x-values to draw a SMOOTH probability curve.
    smooth_hours = np.linspace(0, 10, num=250)

    # .predict_proba returns columns for class 0 and class 1. [:, 1] selects
    # the chance of 'Passed = 1', which is the probability we want to plot.
    pass_probabilities = model.predict_proba(smooth_hours.reshape(-1, 1))[:, 1]

    # Plot actual pass/fail labels: all y-values will be exactly 0 or 1.
    fig = px.scatter(
        data,
        x="Hours studied",
        y="Passed (1=yes)",
        title="Logistic regression: probability of passing",
        opacity=0.50,
    )

    # Overlay the S-shaped probability prediction (not a straight line).
    fig.add_trace(
        go.Scatter(
            x=smooth_hours,
            y=pass_probabilities,
            mode="lines",
            name="Predicted probability of passing",
            line={"color": "#ed7d31", "width": 3},
        )
    )

    # This horizontal guideline marks 50% probability: the usual decision
    # cutoff for choosing class 0 (fail) versus class 1 (pass).
    fig.add_hline(
        y=0.5,
        line_dash="dash",
        line_color="gray",
        annotation_text="50% cutoff",
        annotation_position="bottom right",
    )
    fig.update_yaxes(range=[-0.08, 1.08])
    fig.update_layout(legend_title_text="")

    return {
        "data": data,
        "model": model,
        "figure": fig,
        "training_accuracy": training_accuracy,
    }


# OPTIONAL COMMAND-LINE DEMO -------------------------------------------------
# This block is not run when ml.py is imported by ml_visuals.py.
# Learners can also run `python ml.py` to inspect just the numerical results.
if __name__ == "__main__":
    linear_result = run_linear_regression()
    logistic_result = run_logistic_regression()

    print("LINEAR REGRESSION")
    print(f"Training R²: {linear_result['training_r2']:.3f}")
    print(f"Slope: {linear_result['slope']:.2f}")
    print("\nLOGISTIC REGRESSION")
    print(f"Training accuracy: {logistic_result['training_accuracy']:.1%}")
