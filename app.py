import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

# --- ARCHITECTURE & INTERFACE MATRIX (COMPACT FONT CONFIGURATION) ---
st.set_page_config(page_title="Horizon Addis Tyre - SPC Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Global Compact Font Size */
    html, body, [class*="css"], .stMarkdown, p, label {
        font-size: 13px !important;
        font-family: 'Courier New', monospace !important;
        color: #FFFFFF !important;
    }
    .main { background-color: #121212; color: #FFFFFF; }
    
    /* High-Visibility Value Block Custom Cards */
    .metric-card {
        background-color: #1E1E1E;
        padding: 8px 12px;
        border-radius: 4px;
        border: 1px solid #333333;
        margin-bottom: 10px;
    }
    .metric-label { font-size: 11px; color: #AAAAAA; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value-yellow { font-size: 18px; font-weight: bold; color: #FFFF00; }
    .metric-value-cyan { font-size: 18px; font-weight: bold; color: #00FFFF; }
    .metric-value-red { font-size: 18px; font-weight: bold; color: #FF4B4B; }
    .metric-value-white { font-size: 18px; font-weight: bold; color: #FFFFFF; }
    
    /* Form Custom Framing */
    div[data-testid="stForm"] {
        background-color: #161616 !important;
        border: 1px solid #444444 !important;
        padding: 10px !important;
    }
    div.stButton > button:first-child { 
        background-color: #FF4B4B !important; 
        color: white !important; 
        font-weight: bold;
        font-size: 12px !important;
        padding: 4px 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏭 HORIZON ADDIS TYRE S.C.")
st.markdown("**Statistical Process Control (SPC) Technical Analysis Dashboard**")

# --- INITIALIZATION DECK & CALCULATION ENGINE ---
if 'dataset' not in st.session_state:
    np.random.seed(42)
    base_samples = []
    for i in range(1, 21):
        measurements = np.random.normal(11.0137, 0.0395, 5)
        base_samples.append([i] + list(measurements))
    st.session_state.dataset = pd.DataFrame(base_samples, columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])

# --- PANEL 1: ENGINEERING CONFIGURATION VARIABLES BAR (TOP) ---
st.markdown("### 🛠️ Process Specification Standards & Formulas")
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: usl = st.number_input("USL (Upper Spec)", value=11.4948, format="%.4f")
with c2: target = st.number_input("Target Value", value=11.1600, format="%.4f")
with c3: lsl = st.number_input("LSL (Lower Spec)", value=10.8252, format="%.4f")
with c4: d2 = st.number_input("Shewhart d2", value=2.3260, format="%.4f")
with c5: A2 = st.number_input("Shewhart A2", value=0.5770, format="%.4f")
with c6: D4 = st.number_input("Shewhart D4", value=2.1140, format="%.4f")

# Data Math Vector Processing
df = st.session_state.dataset.copy()
df['Mean'] = df[['X1', 'X2', 'X3', 'X4', 'X5']].mean(axis=1)
df['Range'] = df[['X1', 'X2', 'X3', 'X4', 'X5']].max(axis=1) - df[['X1', 'X2', 'X3', 'X4', 'X5']].min(axis=1)

grand_mean = df['Mean'].mean()
average_range = df['Range'].mean()

ucl_x = grand_mean + (A2 * average_range)
lcl_x = grand_mean - (A2 * average_range)
ucl_r = D4 * average_range
lcl_r = 0.0

estimated_sigma = average_range / d2 if average_range > 0 else 0.001
cp = (usl - lsl) / (6 * estimated_sigma) if estimated_sigma > 0 else 0
cpk = min((usl - grand_mean)/(3 * estimated_sigma), (grand_mean - lsl)/(3 * estimated_sigma)) if estimated_sigma > 0 else 0

st.markdown("---")

# --- PANEL 2: HIGH-CONTRAST METRICS INDICATOR MATRIX ---
st.markdown("### 📈 Live Process Control Calculation Array")
m1, m2, m3, m4, m5, m6 = st.columns(6)

with m1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Grand Mean (X̄̄)</div><div class="metric-value-white">{grand_mean:.4f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Mean Range (R̄)</div><div class="metric-value-cyan">{average_range:.4f}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">X̄ UCL / LCL</div><div class="metric-value-red">{ucl_x:.4f} / {lcl_x:.4f}</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Range UCL</div><div class="metric-value-red">{ucl_r:.4f}</div></div>', unsafe_allow_html=True)
with m5:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Capability Cp</div><div class="metric-value-yellow">{cp:.3f}</div></div>', unsafe_allow_html=True)
with m6:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Capability Cpk</div><div class="metric-value-yellow">{cpk:.3f}</div></div>', unsafe_allow_html=True)

# --- PANEL 3: PARALLEL SPLIT FOR ROW INPUT AND UNBROKEN FEED TABLE ---
st.markdown("---")
layout_col1, layout_col2 = st.columns([1.2, 1.8])

with layout_col1:
    st.markdown("### 📥 Sample Row Entry Grid")
    with st.form(key='data_stream_entry', clear_on_submit=True):
        next_sample_id = int(df['Sample'].max() + 1)
        st.markdown(f"**Target Sample Sequential Index:** `{next_sample_id}`")
        
        in_x1 = st.number_input("Point X1", value=float(df.iloc[-1]['X1']), format="%.4f")
        in_x2 = st.number_input("Point X2", value=float(df.iloc[-1]['X2']), format="%.4f")
        in_x3 = st.number_input("Point X3", value=float(df.iloc[-1]['X3']), format="%.4f")
        in_x4 = st.number_input("Point X4", value=float(df.iloc[-1]['X4']), format="%.4f")
        in_x5 = st.number_input("Point X5", value=float(df.iloc[-1]['X5']), format="%.4f")
        
        submit_data = st.form_submit_button(label="⚡ Commit Entry to Matrix")
        if submit_data:
            new_vector = pd.DataFrame([[next_sample_id, in_x1, in_x2, in_x3, in_x4, in_x5]], 
                                      columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])
            st.session_state.dataset = pd.concat([st.session_state.dataset, new_vector], ignore_index=True)
            st.rerun()

with layout_col2:
    st.markdown("### 📋 Persistent Subgroup Storage Log (Always Visible)")
    # Forces raw storage values visibility alongside data entry card
    formatted_df = df.copy()
    st.dataframe(
        formatted_df.style.format("{:.4f}", subset=['X1', 'X2', 'X3', 'X4', 'X5', 'Mean', 'Range']), 
        height=280, 
        use_container_width=True
    )

st.markdown("---")

# --- PANEL 4: SIDE-BY-SIDE PRODUCTION PLOTS ---
st.markdown("### 📊 Live Diagnostic Control Graphs")
chart_col1, chart_col2, chart_col3 = st.columns([1.4, 1.4, 1.2])

with chart_col1:
    fig_x = go.Figure()
    fig_x.add_trace(go.Scatter(x=df['Sample'], y=df['Mean'], mode='lines+markers', name='Mean', line=dict(color='#FFFF00', width=1.5)))
    fig_x.add_shape(type="line", x0=df['Sample'].min(), y0=grand_mean, x1=df['Sample'].max(), y1=grand_mean, line=dict(color="white", width=1.5))
    fig_x.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_x, x1=df['Sample'].max(), y1=ucl_x, line=dict(color="red", dash="dash", width=1))
    fig_x.add_shape(type="line", x0=df['Sample'].min(), y0=lcl_x, x1=df['Sample'].max(), y1=lcl_x, line=dict(color="red", dash="dash", width=1))
    fig_x.update_layout(title="<b>X-Bar Chart</b>", title_font_size=12, paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white", height=260, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_x, use_container_width=True)

with chart_col2:
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatter(x=df['Sample'], y=df['Range'], mode='lines+markers', name='Range', line=dict(color='#00FFFF', width=1.5)))
    fig_r.add_shape(type="line", x0=df['Sample'].min(), y0=average_range, x1=df['Sample'].max(), y1=average_range, line=dict(color="white", width=1.5))
    fig_r.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_r, x1=df['Sample'].max(), y1=ucl_r, line=dict(color="red", dash="dash", width=1))
    fig_r.update_layout(title="<b>R-Chart</b>", title_font_size=12, paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white", height=260, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_r, use_container_width=True)

with chart_col3:
    fig_spec = go.Figure()
    flattened_values = df[['X1', 'X2', 'X3', 'X4', 'X5']].values.flatten()
    fig_spec.add_trace(go.Histogram(x=flattened_values, histnorm='probability density', marker_color='#444444', opacity=0.7))
    
    xmin, xmax = min(flattened_values.min(), lsl), max(flattened_values.max(), usl)
    x_axis = np.linspace(xmin, xmax, 100)
    y_axis = norm.pdf(x_axis, grand_mean, estimated_sigma)
    fig_spec.add_trace(go.Scatter(x=x_axis, y=y_axis, mode='lines', line=dict(color='#FFA500', width=1.5)))
    
    fig_spec.add_vline(x=lsl, line_dash="dot", line_color="red")
    fig_spec.add_vline(x=usl, line_dash="dot", line_color="red")
    fig_spec.add_vline(x=target, line_color="green")
    fig_spec.update_layout(title="<b>Process Curve vs Specs</b>", title_font_size=12, paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white", height=260, margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
    st.plotly_chart(fig_spec, use_container_width=True)
