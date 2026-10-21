import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Smart Health Dashboard", page_icon="🏥", layout="wide")

# 2. Custom CSS for Decorative Cards
st.markdown("""
<style>
    .card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .card:hover { transform: translateY(-5px); }
    .card-title { color: #7f8c8d; font-size: 1.1rem; font-weight: 600; text-transform: uppercase; margin-bottom: 10px; }
    .card-value { color: #2c3e50; font-size: 3rem; font-weight: bold; }
    
    /* Normal vs Alert Status Borders */
    .normal-border { border-top: 6px solid #2ecc71; }
    .alert-border { border-top: 6px solid #e74c3c; background-color: #fadbd8; }
    .alert-text { color: #c0392b !important; }
</style>
""", unsafe_allow_html=True)

# 3. Initialize Session State for Data Logging (Graphing)
if 'data_log' not in st.session_state:
    st.session_state.data_log = pd.DataFrame(columns=['Time', 'Heart Rate', 'SpO2', 'Temperature'])

# 4. Main UI Setup
st.title("🏥 Smart Health Monitoring System")
st.markdown("### CSE Core & ECE Prototype | Real-Time Vitals Dashboard")
st.divider()

# Create dynamic placeholders to update seamlessly without flickering
status_banner = st.empty()
col1, col2, col3 = st.columns(3)
hr_metric = col1.empty()
spo2_metric = col2.empty()
temp_metric = col3.empty()

st.markdown("### 📈 Live Vitals Trend")
chart_placeholder = st.empty()

# 5. Real-Time Data Loop
while True:
    # Generate Mock Data
    hr = random.randint(60, 110)
    spo2 = random.randint(88, 100)
    temp = round(random.uniform(36.0, 39.0), 1)
    current_time = datetime.now().strftime("%H:%M:%S")

    # Alert Logic Evaluation
    hr_alert = hr > 100
    spo2_alert = spo2 < 92
    temp_alert = temp > 37.5
    system_alert = hr_alert or spo2_alert or temp_alert

    # Update Status Banner
    if system_alert:
        status_banner.error("⚠️ **CRITICAL ALERT:** Abnormal vital signs detected! Please check the patient.")
    else:
        status_banner.success("✅ **SYSTEM NORMAL:** All vital signs are within safe ranges.")

    # Render Decorative Metric Cards (HTML/CSS Injection)
    hr_class = "alert-border" if hr_alert else "normal-border"
    hr_val_class = "alert-text" if hr_alert else ""
    hr_metric.markdown(f"""
        <div class="card {hr_class}">
            <div class="card-title">❤️ Heart Rate (BPM)</div>
            <div class="card-value {hr_val_class}">{hr}</div>
        </div>
    """, unsafe_allow_html=True)

    spo2_class = "alert-border" if spo2_alert else "normal-border"
    spo2_val_class = "alert-text" if spo2_alert else ""
    spo2_metric.markdown(f"""
        <div class="card {spo2_class}">
            <div class="card-title">💨 Oxygen (SpO2 %)</div>
            <div class="card-value {spo2_val_class}">{spo2}</div>
        </div>
    """, unsafe_allow_html=True)

    temp_class = "alert-border" if temp_alert else "normal-border"
    temp_val_class = "alert-text" if temp_alert else ""
    temp_metric.markdown(f"""
        <div class="card {temp_class}">
            <div class="card-title">🌡️ Temperature (°C)</div>
            <div class="card-value {temp_val_class}">{temp}</div>
        </div>
    """, unsafe_allow_html=True)

    # Update Data Log and Line Chart
    new_data = pd.DataFrame({'Time': [current_time], 'Heart Rate': [hr], 'SpO2': [spo2], 'Temperature': [temp]})
    st.session_state.data_log = pd.concat([st.session_state.data_log, new_data]).tail(30) # Keep last 30 readings
    
    # Plot the chart
    chart_data = st.session_state.data_log.set_index('Time')
    chart_placeholder.line_chart(chart_data, use_container_width=True)

    # Pause before next reading
    time.sleep(2)
