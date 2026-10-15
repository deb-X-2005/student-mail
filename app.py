from pathlib import Path

import joblib
import streamlit as st

from features import make_text
from rules import (
    priority_override,
    guess_topic,
    scam_warnings
)

# Configure the app
st.set_page_config(
    page_title="Student Mail AI",
    page_icon="📬"
)

st.title("📬 Student Mail AI")
st.caption("TF-IDF + Linear SVM Email Classifier")

# Model location
MODEL_PATH = (
    Path(__file__).parent
    / "models"
    / "priority_model.joblib"
)

# Load model once and cache it
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


if not MODEL_PATH.exists():
    st.error("Train the model first!")
    st.stop()


# Create email input form
with st.form("email_form"):

    sender = st.text_input(
        "Sender Email",
        placeholder="notifications@classroom.google.com"
    )

    subject = st.text_input(
        "Email Subject",
        placeholder="Assignment Deadline"
    )

    body = st.text_area(
        "Email Body",
        height=180,
        placeholder="Paste your email here..."
    )

    submit = st.form_submit_button(
        "Classify Email"
    )


# Run prediction after submission
if submit:

    if not (subject.strip() or body.strip()):
        st.warning("Please enter email content.")

    else:
        model = load_model()

        # Prepare input text
        text = make_text(
            sender,
            subject,
            body
        )

        # ML prediction
        svm_priority = model.predict([text])[0]

        # Apply special rules
        override, reason = priority_override(
            sender,
            subject
        )

        final_priority = override or svm_priority

        # Identify topic and warning phrases
        topic = guess_topic(
            sender,
            subject,
            body
        )

        warnings = scam_warnings(
            subject,
            body
        )

        # Display result
        st.subheader("Classification Result")

        st.metric(
            "Final Priority",
            final_priority
        )

        st.write(
            "**SVM Prediction:**",
            svm_priority
        )

        st.write(
            "**Email Category:**",
            topic
        )

        if reason:
            st.info("Priority rule: " + reason)

        if warnings:
            st.warning(
                "Potentially suspicious wording detected."
            )

            for warning in warnings:
                st.write("•", warning)

        else:
            st.info(
                "No listed warning phrases detected. "
                "This does not verify the email is safe."
            )

st.divider()

st.caption(
    "Educational prototype trained on provisional labels. "
    "Sender addresses are not authenticated."
)
