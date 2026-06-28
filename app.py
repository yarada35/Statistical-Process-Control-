import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

# --- ARCHITECTURAL VISUAL MASTER MATRIX (PREMIUM INDUSTRIAL SPEC) ---
st.set_page_config(page_title="Horizon Addis Tyre - SPC Center", layout="wide")

# Custom injection of premium CSS to enforce neon-green cyber layout and lock visibility
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');
    
    /* Global Container Lock and Workspace Colors */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #08080A !important;
        font-family: 'Share Tech Mono', monospace !important;
        color: #00FF66 !important;
    }
    
    /* Artistic Background Title Banner Component */
    .factory-banner {
        background: linear-gradient(135deg, #0D2B18 0%, #050A06 100%);
        border: 2px solid #00FF66;
        box-shadow: 0px 0px 25px rgba(0, 255, 102, 0.25);
        border-radius: 8px;
        padding: 25px;
        margin-bottom: 25px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .factory-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(rgba(0, 255, 102, 0.03) 50%, rgba(0, 0, 0, 0) 50%), linear-gradient(90deg, rgba(0, 255, 102, 0.03) 50%, rgba(0, 0, 0, 0) 50%);
        background-size: 4px 4px;
    }
    .main-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 34px !important;
        font-weight: 700 !important;
        letter-spacing: 4px;
        color: #00FF66 !important;
        text-shadow: 0 0 15px rgba(0, 255, 102, 0.8);
        margin: 0;
    }
    .sub-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 13px !important;
        letter-spacing: 6px;
        color: #FFFFFF !important;
        margin-top: 8px;
        text-transform: uppercase;
        opacity: 0.8;
    }

    /* Fixed Parameter Grid Cards */
    .metric-card {
        background: #0E1112;
        border: 1px solid #1C2421;
        border-radius: 4px;
        padding: 12px;
        text-align: center;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.8);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: #00FF66;
        box-shadow: 0 0 12px rgba(0, 255, 102, 0.15);
    }
    .metric-label {
        font-size: 10px !important;
        color: #8A9A92 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #00FF66 !important;
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 8px rgba(0, 255, 102, 0.4);
    }
    
    /* Control Form & Elements Layout styling */
    div[data-testid="stForm"] {
        background-color: #0B0D0E !important;
        border: 1px solid #1C2421 !important;
        border-radius: 6px !important;
        padding: 16px !important;
    }
    label, p, span { color: #00FF66 !important; }
    
    /* Input Elements Framework styling */
    .stSelectbox div[data-baseweb="select"], .stNumberInput input {
        background-color: #121614 !important;
        color: #00FF66 !important;
        border: 1px solid #24332B !important;
    }
    
    /* Fixed Data Scroll Frame overrides */
    div[data-testid="stDataFrame"] {
        border: 1px solid #1C2421;
        background-color: #0B0D0E;
    }
    </style>
""", unsafe_allow_html=True)

# --- ARTISTIC TITLE BACKGROUND LAYOUT BANNER ---
st.markdown("""
    <div class="factory-banner">
        <div class="main-title">⚙️ HORIZON ADDIS TYRE S.C. 🔗</div>
        <div class="sub-title">Product Industrialization & Quality Assurance — Live SPC Engine</div>
    </div>
""", unsafe_allow_html=True)

# --- ACTIVE COMPONENT SELECTION MATRIX ---
col_sel1, col_sel2 = st.columns([2, 1])
with col_sel1:
    component_size = st.selectbox(
        "📂 Active Component Model & Dimension Selector",
        ["750-16 HT-99 Treadweight", "400-8 HT-60 Treadweight"]
    )

# Assign specifications matching validated source spreadsheets
if "750-16" in component_size:
    default_target, default_usl, default_lsl = 11.1600, 11.4948, 10.8252
else:
    default_target, default_usl, default_lsl = 2.0200, 2.0806, 1.9594

with col_sel2:
    tolerance_pct = st.number_input("Given Tolerance Percentage (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.1, format="%.1f")

# --- DYNAMIC STRUCTURAL SEED DECKS ---
state_key = f"dataset_{component_size.replace(' ', '_')}"
if state_key not in st.session_state:
    np.random.seed(42)
    base_data = []
    for i in range(1, 21):
        if "750-16" in component_size:
            row_vals = np.random.normal(11.0137, 0.0395, 5)
        else:
            row_vals = np.random.normal(1.9989, 0.0216, 5)
        base_data.append([i] + list(row_vals))
    st.session_state[state_key] = pd.DataFrame(base_data, columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])

# --- PANEL 1: SPECIFICATION CONSTANTS BAR ---
st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:2px;'>🛠️ PROCESS SPECIFICATION STANDARDS & CONSTANTS</p>", unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: usl = st.number_input("USL (Upper Spec)", value=default_usl, format="%.4f")
with c2: target = st.number_input("Target Value", value=default_target, format="%.4f")
with c3: lsl = st.number_input("LSL (Lower Spec)", value=default_lsl, format="%.4f")
with c4: d2 = st.number_input("Shewhart d2", value=2.3330, format="%.4f")
with c5: A2 = st.number_input("Shewhart A2", value=0.5770, format="%.4f")
with c6: D4 = st.number_input("Shewhart D4", value=2.1150, format="%.4f")

# Dynamic Tolerance Formula Math
calculated_tolerance = target * (tolerance_pct / 100.0)
tol_max_val = target - calculated_tolerance
tol_min_val = target + calculated_tolerance

# Data Core Calculations
df = st.session_state[state_key].copy()
df['Mean'] = df[['X1', 'X2', 'X3', 'X4', 'X5']].mean(axis=1)
df['Range'] = df[['X1', 'X2', 'X3', 'X4', 'X5']].max(axis=1) - df[['X1', 'X2', 'X3', 'X4', 'X5']].min(axis=1)

flattened = df[['X1', 'X2', 'X3', 'X4', 'X5']].values.flatten()
total_obs = len(flattened)

grand_mean = df['Mean'].mean()
average_range = df['Range'].mean()
span_obs = float(flattened.max() - flattened.min())
grand_median = float(np.median(flattened))
variance_obs = float(np.var(flattened))
obs_max = float(flattened.max())
obs_min = float(flattened.min())
std_dev = average_range / d2

ucl_x = grand_mean + (A2 * average_range)
lcl_x = grand_mean - (A2 * average_range)
ucl_r = D4 * average_range
lcl_r = 0.0
gen_movement = float(np.std(df['Mean'].diff().dropna())) if len(df) > 1 else 0.0437

st.markdown("---")

# --- PANEL 2: RAW NUMERICAL GREEN METRICS PANEL (NO EXTRA COMPONENT LABELS) ---
st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:2px;'>📊 LIVE PROCESS SUMMARY PARAMETERS</p>", unsafe_allow_html=True)
r1_c1, r1_c2, r1_c3, r1_c4, r1_c5 = st.columns(5)
r2_c1, r2_c2, r2_c3, r2_c4, r2_c5 = st.columns(5)
r3_c1, r3_c2, r3_c3, r3_c4, r3_c5 = st.columns(5)

# Row 1 Render
r1_c1.markdown(f'<div class="metric-card"><div class="metric-label">Target Center</div><div class="metric-value">{target:.4f}</div></div>', unsafe_allow_html=True)
r1_c2.markdown(f'<div class="metric-card"><div class="metric-label">USL</div><div class="metric-value">{usl:.4f}</div></div>', unsafe_allow_html=True)
r1_c3.markdown(f'<div class="metric-card"><div class="metric-label">LSL</div><div class="metric-value">{lsl:.4f}</div></div>', unsafe_allow_html=True)
r1_c4.markdown(f'<div class="metric-card"><div class="metric-label">Range Mean (R̄)</div><div class="metric-value">{average_range:.4f}</div></div>', unsafe_allow_html=True)
r1_c5.markdown(f'<div class="metric-card"><div class="metric-label">Total Observations</div><div class="metric-value">{total_obs}</div></div>', unsafe_allow_html=True)

# Row 2 Render
r2_c1.markdown(f'<div class="metric-card"><div class="metric-label">Grand Mean (X̄̄)</div><div class="metric-value">{grand_mean:.4f}</div></div>', unsafe_allow_html=True)
r2_c2.markdown(f'<div class="metric-card"><div class="metric-label">Gen. Movement</div><div class="metric-value">{gen_movement:.4f}</div></div>', unsafe_allow_html=True)
r2_c3.markdown(f'<div class="metric-card"><div class="metric-label">Span Total</div><div class="metric-value">{span_obs:.4f}</div></div>', unsafe_allow_html=True)
r2_c4.markdown(f'<div class="metric-card"><div class="metric-label">Grand Median</div><div class="metric-value">{grand_median:.4f}</div></div>', unsafe_allow_html=True)
r2_c5.markdown(f'<div class="metric-card"><div class="metric-label">Obs Variance</div><div class="metric-value">{variance_obs:.6f}</div></div>', unsafe_allow_html=True)

# Row 3 Render
r3_c1.markdown(f'<div class="metric-card"><div class="metric-label">Obs Max Value</div><div class="metric-value">{obs_max:.4f}</div></div>', unsafe_allow_html=True)
r3_c2.markdown(f'<div class="metric-card"><div class="metric-label">Obs Min Value</div><div class="metric-value">{obs_min:.4f}</div></div>', unsafe_allow_html=True)
r3_c3.markdown(f'<div class="metric-card"><div class="metric-label">Standard Dev (σ)</div><div class="metric-value">{std_dev:.4f}</div></div>', unsafe_allow_html=True)
r3_c4.markdown(f'<div class="metric-card"><div class="metric-label">X̄ UCL / LCL</div><div class="metric-value">{ucl_x:.4f} / {lcl_x:.4f}</div></div>', unsafe_allow_html=True)
r3_c5.markdown(f'<div class="metric-card"><div class="metric-label">R UCL / LCL</div><div class="metric-value">{ucl_r:.4f} / {lcl_r:.4f}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# --- UNBROKEN LIVE WORKSPACE SPLIT (ENTRY & DATA VIEW GRID VISIBLE) ---
split_col1, split_col2 = st.columns([1.1, 1.9])

with split_col1:
    st.markdown(f"<p style='font-size:13px; font-weight:bold; letter-spacing:1px;'>📥 LIVE SUBGROUP DATASTREAM ENTRY</p>", unsafe_allow_html=True)
    st.markdown("<div class='sop-card'><b>📋 SOP:</b> Record 5 batch measurements on scale, execute submit entry button below.</div>", unsafe_allow_html=True)
    
    with st.form(key=f"form_{state_key}", clear_on_submit=True):
        next_id = int(df['Sample'].max() + 1)
        st.markdown(f"**Target Sample Sequential Index:** `Subgroup #{next_id}`")
        v1 = st.number_input("Sub-Sample X1", value=float(df.iloc[-1]['X1']), format="%.4f", key=f"x1_{state_key}")
        v2 = st.number_input("Sub-Sample X2", value=float(df.iloc[-1]['X2']), format="%.4f", key=f"x2_{state_key}")
        v3 = st.number_input("Sub-Sample X3", value=float(df.iloc[-1]['X3']), format="%.4f", key=f"x3_{state_key}")
        v4 = st.number_input("Sub-Sample X4", value=float(df.iloc[-1]['X4']), format="%.4f", key=f"x4_{state_key}")
        v5 = st.number_input("Sub-Sample X5", value=float(df.iloc[-1]['X5']), format="%.4f", key=f"x5_{state_key}")
        
        if st.form_submit_button(label="⚡ Append Subgroup to Engine Base"):
            new_row = pd.DataFrame([[next_id, v1, v2, v3, v4, v5]], columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])
            st.session_state[state_key] = pd.concat([st.session_state[state_key], new_row], ignore_index=True)
            st.rerun()

with split_col2:
    st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:1px;'>📋 UNBROKEN ACTIVE DATALIST STORAGE FRAME</p>", unsafe_allow_html=True)
    st.dataframe(
        df.style.format("{:.4f}", subset=['X1', 'X2', 'X3', 'X4', 'X5', 'Mean', 'Range']),
        height=250,
        use_container_width=True
    )

st.markdown("---")

# --- SIDE-BY-SIDE ANALYTICS CONTROL PLOTS ---
st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:2px;'>📊 PARALLEL PROCESS DIAGNOSTICS CONTROL GRAPHS</p>", unsafe_allow_html=True)
g_col1, g_col2, g_col3 = st.columns([1.4, 1.4, 1.2])

with g_col1:
    f_x = go.Figure()
    f_x.add_trace(go.Scatter(x=df['Sample'], y=df['Mean'], mode='lines+markers', name='Mean', line=dict(color='#00FF66', width=2)))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=grand_mean, x1=df['Sample'].max(), y1=grand_mean, line=dict(color="white", width=1.5))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_x, x1=df['Sample'].max(), y1=ucl_x, line=dict(color="red", dash="dash", width=1.5))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=lcl_x, x1=df['Sample'].max(), y1=lcl_x, line=dict(color="red", dash="dash", width=1.5))
    f_x.update_layout(title="<b>X-Bar Process Control Chart</b>", paper_bgcolor='#08080A', plot_bgcolor='#0E1112', font_color="#00FF66", height=240, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(f_x, use_container_width=True)

with g_col2:
    f_r = go.Figure()
    f_r.add_trace(go.Scatter(x=df['Sample'], y=df['Range'], mode='lines+markers', name='Range', line=dict(color='#00FFFF', width=2)))
    f_r.add_shape(type="line", x0=df['Sample'].min(), y0=average_range, x1=df['Sample'].max(), y1=average_range, line=dict(color="white", width=1.5))
    f_r.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_r, x1=df['Sample'].max(), y1=ucl_r, line=dict(color="red", dash="dash", width=1.5))
    f_r.update_layout(title="<b>R-Bar Range Variability Chart</b>", paper_bgcolor='#08080A', plot_bgcolor='#0E1112', font_color="#00FF66", height=240, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(f_r, use_container_width=True)

with g_col3:
    f_s = go.Figure()
    f_s.add_trace(go.Histogram(x=flattened, histnorm='probability density', marker_color='#1A2620', opacity=0.85, marker_line=dict(width=1, color='#00FF66')))
    xs = np.linspace(min(flattened.min(), lsl, tol_max_val), max(flattened.max(), usl, tol_min_val), 100)
    ys = norm.pdf(xs, grand_mean, std_dev)
    f_s.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='#FFBB00', width=2)))
    
    f_s.add_vline(x=lsl, line_dash="dot", line_color="red", line_width=1.5)
    f_s.add_vline(x=usl, line_dash="dot", line_color="red", line_width=1.5)
    f_s.add_vline(x=target, line_color="#00FF66", line_width=1.5)
    f_s.add_vline(x=tol_max_val, line_dash="dash", line_color="#FF4B4B", line_width=1.5)
    f_s.add_vline(x=tol_min_val, line_dash="dash", line_color="#FF4B4B", line_width=1.5)
    
    f_s.update_layout(title="<b>Process Curve vs Specs & Tol</b>", paper_bgcolor='#08080A', plot_bgcolor='#0E1112', font_color="#00FF66", height=240, margin=dict(l=10, r=10, t=50, b=10), showlegend=False)
    st.plotly_chart(f_s, use_container_width=True)
