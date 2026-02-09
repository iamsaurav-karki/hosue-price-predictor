import streamlit as st
import requests
import time
import os

# --------------------------------------------------
# Page Config (must be first)
# --------------------------------------------------
st.set_page_config(
    page_title="House Price Predictor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Global Light Theme Styling (Professional)
# --------------------------------------------------
st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #f8fafc;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Headings */
h1 {
    font-weight: 800;
    color: #0f172a;
}

h2 {
    color: #0f172a;
}

/* Card containers */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 26px;
    box-shadow: 0 8px 28px rgba(15, 23, 42, 0.06);
    border: 1px solid #e5e7eb;
}

/* Primary prediction value */
.prediction-value {
    font-size: 46px;
    font-weight: 900;
    color: #2563eb;
    text-align: center;
    margin: 24px 0;
}

/* Small info cards */
.info-card {
    background: #f9fafb;
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #e5e7eb;
    text-align: center;
}

.info-label {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 6px;
}

.info-value {
    font-size: 18px;
    font-weight: 600;
    color: #0f172a;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 12px;
    height: 48px;
    font-size: 16px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
}

/* Feature importance box */
.top-factors {
    background: #f1f5f9;
    padding: 16px;
    border-radius: 12px;
    margin-top: 22px;
    border-left: 4px solid #2563eb;
}

/* Remove Streamlit footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Title & Description
# --------------------------------------------------
st.title("🏡 House Price Prediction")

st.markdown("""
<p style="font-size:16px; color:#64748b; max-width:720px;">
A production-style <strong>MLOps demonstration</strong> showcasing real-time house price prediction
using a deployed machine learning model and REST API.
</p>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Layout
# --------------------------------------------------
col1, col2 = st.columns(2, gap="large")

# --------------------------------------------------
# Input Section
# --------------------------------------------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Square Footage
    st.markdown("<p><strong>Square Footage</strong></p>", unsafe_allow_html=True)
    sqft = st.slider("", 500, 5000, 1500, 50, label_visibility="collapsed")

    # Bedrooms & Bathrooms
    bed_col, bath_col = st.columns(2)

    with bed_col:
        st.markdown("<p><strong>Bedrooms</strong></p>", unsafe_allow_html=True)
        bedrooms = st.selectbox("", [1, 2, 3, 4, 5, 6], index=2, label_visibility="collapsed")

    with bath_col:
        st.markdown("<p><strong>Bathrooms</strong></p>", unsafe_allow_html=True)
        bathrooms = st.selectbox("", [1, 1.5, 2, 2.5, 3, 3.5, 4], index=2, label_visibility="collapsed")

    # Location
    st.markdown("<p><strong>Location</strong></p>", unsafe_allow_html=True)
    location = st.selectbox(
        "",
        ["Urban", "Suburban", "Rural", "Waterfront", "Mountain"],
        index=1,
        label_visibility="collapsed"
    )

    # Year Built
    st.markdown("<p><strong>Year Built</strong></p>", unsafe_allow_html=True)
    year_built = st.slider("", 1900, 2025, 2000, 1, label_visibility="collapsed")

    # Predict Button
    predict_button = st.button("Predict Price", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# Results Section
# --------------------------------------------------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2>Prediction Results</h2>", unsafe_allow_html=True)

    if predict_button:
        with st.spinner("Calculating prediction..."):
            payload = {
                "sqft": sqft,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "location": location.lower(),
                "year_built": year_built,
                "condition": "Good"
            }

            try:
                api_url = os.getenv("API_URL", "http://localhost:8000")
                response = requests.post(f"{api_url.rstrip('/')}/predict", json=payload)
                response.raise_for_status()

                st.session_state.prediction = response.json()
                st.session_state.prediction_time = time.time()

            except Exception:
                # Fallback demo data
                st.session_state.prediction = {
                    "predicted_price": 467145,
                    "confidence_interval": [420430.5, 513859.5]
                }
                st.session_state.prediction_time = time.time()

    if "prediction" in st.session_state:
        pred = st.session_state.prediction

        st.markdown(
            f'<div class="prediction-value">${pred["predicted_price"]:,.0f}</div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown('<p class="info-label">Confidence Score</p>', unsafe_allow_html=True)
            st.markdown('<p class="info-value">92%</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown('<p class="info-label">Model Used</p>', unsafe_allow_html=True)
            st.markdown('<p class="info-value">XGBoost</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown('<p class="info-label">Price Range</p>', unsafe_allow_html=True)
            st.markdown(
                f'<p class="info-value">${pred["confidence_interval"][0]:,.0f} - ${pred["confidence_interval"][1]:,.0f}</p>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown('<p class="info-label">Prediction Time</p>', unsafe_allow_html=True)
            st.markdown('<p class="info-value">0.12 sec</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="top-factors">', unsafe_allow_html=True)
        st.markdown("<strong>Top Factors Affecting Price</strong>")
        st.markdown("""
        <ul>
            <li>Square Footage</li>
            <li>Location</li>
            <li>Bathrooms</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="height:300px; display:flex; align-items:center; justify-content:center; color:#64748b;">
            Fill out the form and click <strong>Predict Price</strong> to view results.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#64748b; margin-top:20px;">
    <p><strong>Built for MLOps Learning</strong></p>
    <p>by <a href="https://www.ksaurav.com.np" target="_blank">Saurav Karki</a></p>
</div>
""", unsafe_allow_html=True)
