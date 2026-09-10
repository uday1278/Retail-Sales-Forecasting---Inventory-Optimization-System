
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Retail Sales Forecasting Dashboard",
    page_icon="📈",
    layout="wide"
)

# -------------------- SESSION STATE --------------------
if "prediction" not in st.session_state:
    st.session_state.prediction = 40.3
    st.session_state.stock = 150.0
    st.session_state.reorder = 282.1
    st.session_state.order_qty = 132.1

# -------------------- LOAD MODEL --------------------
try:
    model = joblib.load("models/retail_forecast_model.pkl")
except:
    model = None

# -------------------- CSS --------------------
st.markdown("""
<style>
.main {
    background-color: #F3F6FB;
}

.block-container {
    padding-top: 1.2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-bottom: 1rem;
    max-width: 100%;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1 {
    margin: 0;
}

.hero {
    background: linear-gradient(135deg, #1E3A8A, #2563EB);
    padding: 40px 30px;
    border-radius: 24px;
    text-align: center;
    color: white;
    margin-bottom: 22px;
}

.hero-title {
    font-size: 46px;
    font-weight: 700;
    margin-bottom: 10px;
}

.hero-sub {
    font-size: 20px;
    opacity: 0.92;
}

.kpi-card {
    background: linear-gradient(135deg, #1E3A5F, #3B5C84);
    border-radius: 24px;
    padding: 28px 20px;
    color: white;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.10);
}

.kpi-title {
    font-size: 15px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 8px;
}

.kpi-sub {
    font-size: 14px;
    opacity: 0.92;
}

.blue {
    background: linear-gradient(135deg, #1E3A5F, #2F5D8C);
}

.green {
    background: linear-gradient(135deg, #1F5F5B, #2F7D78);
}

.orange {
    background: linear-gradient(135deg, #8A5A2B, #B7793E);
}

.purple {
    background: linear-gradient(135deg, #4B5563, #6B7280);
}

.section-box {
    background: white;
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-top: 8px;
}

.section-title {
    font-size: 34px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 20px;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #1E3A8A, #2563EB);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.9rem;
    font-size: 18px;
    font-weight: 600;
    margin-top: 12px;
}

.stButton > button:hover {
    color: white;
    border: none;
}

[data-testid="stImage"] img {
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HERO --------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">📈 Retail Sales Forecasting & Inventory Dashboard</div>
        <div class="hero-sub">AI-driven demand prediction and inventory optimization</div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------- KPI CARDS --------------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Forecast Sales</div>
            <div class="kpi-value">{st.session_state.prediction:.1f}</div>
            <div class="kpi-sub">Expected units to sell</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Current Stock</div>
            <div class="kpi-value">{st.session_state.stock:.1f}</div>
            <div class="kpi-sub">Units available</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Reorder Point</div>
            <div class="kpi-value">{st.session_state.reorder:.1f}</div>
            <div class="kpi-sub">Minimum safe inventory</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Recommended Order</div>
            <div class="kpi-value">{st.session_state.order_qty:.1f}</div>
            <div class="kpi-sub">Units to purchase</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------- MAIN CONTENT --------------------
left, right = st.columns([1, 1])

with left:
    
    st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        price = st.number_input("Price", value=20.0)
        promo = st.selectbox("Promotion", [0, 1])
        weekday = st.selectbox("Weekday", [1, 2, 3, 4, 5, 6, 7])
        month = st.selectbox("Month", [1,2,3,4,5,6,7,8,9,10,11,12])
        lag_1 = st.number_input("Previous Day Sales", value=40.0)

    with c2:
        current_stock = st.number_input("Current Stock", value=150.0)
        day = st.number_input("Day", min_value=1, max_value=31, value=15)
        year = st.number_input("Year", min_value=2019, max_value=2030, value=2022)
        lag_7 = st.number_input("Sales 7 Days Ago", value=42.0)
        rolling_mean_7 = st.number_input("7-Day Average Sales", value=41.0)

    if st.button("Predict Sales & Inventory"):
        if model is not None:
            input_df = pd.DataFrame({
                "price": [price],
                "promo": [promo],
                "weekday": [weekday],
                "month": [month],
                "day": [day],
                "year": [year],
                "lag_1": [lag_1],
                "lag_7": [lag_7],
                "rolling_mean_7": [rolling_mean_7]
            })

            prediction = float(model.predict(input_df)[0])
        else:
            prediction = 40.3

        reorder = prediction * 7
        order_qty = max(0, reorder - current_stock)

        st.session_state.prediction = prediction
        st.session_state.stock = current_stock
        st.session_state.reorder = reorder
        st.session_state.order_qty = order_qty

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    
    st.markdown('<div class="section-title">Model Performance</div>', unsafe_allow_html=True)

    try:
        st.image("images/actual_vs_predicted.png", use_container_width=True)
    except:
        st.info("Place actual_vs_predicted.png inside the images folder.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="background:#EFF6FF;padding:18px;border-radius:16px;border-left:6px solid #2563EB;">
            <div style="font-size:18px;font-weight:700;color:#1E3A8A;margin-bottom:8px;">Inventory Recommendation</div>
            <div style="font-size:15px;color:#334155;line-height:1.8;">
                Maintain approximately <b>{st.session_state.reorder:.0f}</b> units in stock.<br>
                Recommended purchase quantity: <b>{st.session_state.order_qty:.0f}</b> units.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
    "<p style='text-align:center; color:#64748b; margin-top:20px;'>Built using Streamlit, Machine Learning and Inventory Analytics</p>",
    unsafe_allow_html=True
)
