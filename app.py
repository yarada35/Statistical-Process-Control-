import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

# --- ARCHITECTURE & INTERFACE MATRIX ---
st.set_page_config(page_title="Horizon Addis Tyre - SPC Production Center", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #121212; color: #FFFFFF; }
    div[data-testid="stSidebar"] { background-color: #1E1E1E; }
    h1, h2, h3, h4 { color: #FFFFFF !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMetric { background-color: #1E1E1E; padding: 10px; border-radius: 5px; border: 1px solid #333333; }
    div.stButton > button:first-child { background-color: #FF4B4B; color: white; border-radius: 4px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🏭 HORIZON ADDIS TYRE S.C.")
st.subheader("Statistical Process Control (SPC) Operational Dashboard")
st.markdown("---")

# --- INITIALIZATION DECK & CALCULATION ENGINE ---
if 'dataset' not in st.session_state:
    # Pre-loading structural engineering vectors from your baseline files (n=5)
    np.random.seed(42)
    base_samples = []
    for i in range(1, 21):
        # Defaulting around baseline targets
        measurements = np.random.normal(11.0137, 0.0395, 5)
        base_samples.append([i] + list(measurements))
    st.session_state.dataset = pd.DataFrame(base_samples, columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])

# --- LINE 1: PROCESS METRIC SPECIFICATIONS (INDICATED AT THE TOP) ---
st.markdown("### 📊 Engineering Variable Configuration & Constants")
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1: usl = st.number_input("USL (Upper Specification)", value=11.4948, format="%.4f")
with c2: target = st.number_input("Target Value (Center)", value=11.1600, format="%.4f")
with c3: lsl = st.number_input("LSL (Lower Specification)", value=10.8252, format="%.4f")
with c4: d2 = st.number_input("Shewhart d2 (n=5)", value=2.3260, format="%.4f")
with c5: A2 = st.number_input("Shewhart A2 (n=5)", value=0.5770, format="%.4f")
with c6: D4 = st.number_input("Shewhart D4 (n=5)", value=2.1140, format="%.4f")

# Core Statistical Calculations Engine
df = st.session_state.dataset.copy()
df['Mean'] = df[['X1', 'X2', 'X3', 'X4', 'X5']].mean(axis=1)
df['Range'] = df[['X1', 'X2', 'X3', 'X4', 'X5']].max(axis=1) - df[['X1', 'X2', 'X3', 'X4', 'X5']].min(axis=1)

grand_mean = df['Mean'].mean()
average_range = df['Range'].mean()

# Core Shewhart Limits
ucl_x = grand_mean + (A2 * average_range)
lcl_x = grand_mean - (A2 * average_range)
ucl_r = D4 * average_range
lcl_r = 0.0  # For n=5, D3 = 0

# Capability Index Matrix
estimated_sigma = average_range / d2 if average_range > 0 else 0.001
cp = (usl - lsl) / (6 * estimated_sigma) if estimated_sigma > 0 else 0
cpk = min((usl - grand_mean)/(3 * estimated_sigma), (grand_mean - lsl)/(3 * estimated_sigma)) if estimated_sigma > 0 else 0

st.markdown("---")

# --- LINE 2: PARALLEL SAMPLE DATA ENTRY SHEET (HORIZONTAL ROW LAYOUT) ---
st.markdown("### 📥 Active Live Stream Entry Card (Excel Simulation Row)")
with st.form(key='data_stream_entry', clear_on_submit=True):
    col_s, col_x1, col_x2, col_x3, col_x4, col_x5 = st.columns(6)
    
    next_sample_id = int(df['Sample'].max() + 1)
    col_s.markdown(f"**Next Sample ID**\n### `{next_sample_id}`")
    
    # Render fields side-by-side to mimic an industrial row input grid
    in_x1 = col_x1.number_input("Point X1", value=float(df.iloc[-1]['X1']), format="%.4f")
    in_x2 = col_x2.number_input("Point X2", value=float(df.iloc[-1]['X2']), format="%.4f")
    in_x3 = col_x3.number_input("Point X3", value=float(df.iloc[-1]['X3']), format="%.4f")
    in_x4 = col_x4.number_input("Point X4", value=float(df.iloc[-1]['X4']), format="%.4f")
    in_x5 = col_x5.number_input("Point X5", value=float(df.iloc[-1]['X5']), format="%.4f")
    
    submit_data = st.form_submit_button(label="⚡ Commit Live Entry Row to System Engine")
    
    if submit_data:
        new_vector = pd.DataFrame([[next_sample_id, in_x1, in_x2, in_x3, in_x4, in_x5]], 
                                  columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])
        st.session_state.dataset = pd.concat([st.session_state.dataset, new_vector], ignore_index=True)
        st.rerun()

st.markdown("---")

# --- LINE 3: LIVE RE-CALCULATED META METRICS ---
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Grand Mean (X̄̄)", f"{grand_mean:.4f}")
m2.metric("Mean Range (R̄)", f"{average_range:.4f}")
m3.metric("X̄ UCL / LCL", f"{ucl_x:.4f} / {lcl_x:.4f}")
m4.metric("R UCL", f"{ucl_r:.4f}")
m5.metric("Process Cp", f"{cp:.3f}")
m6.metric("Process Cpk", f"{cpk:.3f}")

st.markdown("---")

# --- LINE 4: PARALLEL INTERACTIVE CHARTS VIEW (SIDE-BY-SIDE PLOTS) ---
st.markdown("### 📊 Parallel Control Charts & Process Capability Comparison")
chart_col1, chart_col2, chart_col3 = st.columns([1.5, 1.5, 1.2])

# --- PANEL A: X-BAR PROCESS CHART ---
with chart_col1:
    fig_x = go.Figure()
    # Trendlines
    fig_x.add_trace(go.Scatter(x=df['Sample'], y=df['Mean'], mode='lines+markers', name='Subgroup X̄', line=dict(color='#FFFF00', width=2)))
    # Limits Lines
    fig_x.add_shape(type="line", x0=df['Sample'].min(), y0=grand_mean, x1=df['Sample'].max(), y1=grand_mean, line=dict(color="white", width=2))
    fig_x.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_x, x1=df['Sample'].max(), y1=ucl_x, line=dict(color="red", dash="dash"))
    fig_x.add_shape(type="line", x0=df['Sample'].min(), y0=lcl_x, x1=df['Sample'].max(), y1=lcl_x, line=dict(color="red", dash="dash"))
    
    # Flag Anomalies (Out of limits points highlighted in bright red)
    df['OOC_X'] = (df['Mean'] > ucl_x) | (df['Mean'] < lcl_x)
    ooc_points = df[df['OOC_X']]
    fig_x.add_trace(go.Scatter(x=ooc_points['Sample'], y=ooc_points['Mean'], mode='markers', marker=dict(color='red', size=10, symbol='triangle-up'), name='OOC Alarm'))
    
    fig_x.update_layout(title="<b>X-Bar Process Control Chart</b>", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_x, use_container_width=True)

# --- PANEL B: RANGE (R) CHART ---
with chart_col2:
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatter(x=df['Sample'], y=df['Range'], mode='lines+markers', name='Subgroup R', line=dict(color='#00FFFF', width=2)))
    fig_r.add_shape(type="line", x0=df['Sample'].min(), y0=average_range, x1=df['Sample'].max(), y1=average_range, line=dict(color="white", width=2))
    fig_r.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_r, x1=df['Sample'].max(), y1=ucl_r, line=dict(color="red", dash="dash"))
    
    fig_r.update_layout(title="<b>R-Chart (Range Variability)</b>", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_r, use_container_width=True)

# --- PANEL C: PROCESS SPECIFICATION GRAPH ---
with chart_col3:
    fig_spec = go.Figure()
    flattened_values = df[['X1', 'X2', 'X3', 'X4', 'X5']].values.flatten()
    
    # Base Raw Histogram Distribution
    fig_spec.add_trace(go.Histogram(x=flattened_values, histnorm='probability density', name='Actual Obs', marker_color='#444444', opacity=0.75))
    
    # Overlay Normal Curve Fit matching calculated data parameters
    xmin, xmax = min(flattened_values.min(), lsl), max(flattened_values.max(), usl)
    x_axis = np.linspace(xmin, xmax, 100)
    y_axis = norm.pdf(x_axis, grand_mean, estimated_sigma)
    fig_spec.add_trace(go.Scatter(x=x_axis, y=y_axis, mode='lines', name='Fit Gaussian', line=dict(color='#FFA500', width=2)))
    
    # Specification Overlay Markers
    fig_spec.add_vline(x=lsl, line_width=3, line_dash="dot", line_color="red", annotation_text="LSL")
    fig_spec.add_vline(x=usl, line_width=3, line_dash="dot", line_color="red", annotation_text="USL")
    fig_spec.add_vline(x=target, line_width=2, line_color="green", annotation_text="Target")
    
    fig_spec.update_layout(title="<b>Process Curve vs Specs</b>", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white", margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
    st.plotly_chart(fig_spec, use_container_width=True)

# --- PANEL 5: AUDIT TRAIL LOG ---
with st.expander("📋 Review Underlying Data Storage Matrix"):
    st.dataframe(df.style.format("{:.4f}", subset=['X1', 'X2', 'X3', 'X4', 'X5', 'Mean', 'Range']), use_container_width=True)
