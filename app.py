import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

# --- INTERFACE MASTER STYLE MATRIX (PERMANENT HIGH-CONTRAST GREEN SPEC) ---
st.set_page_config(page_title="Horizon Addis Tyre - SPC Center", layout="wide")

st.markdown("""
    <style>
    /* Global Compact Font Size & Typeface */
    html, body, p, label, span, div { 
        font-size: 12px !important; 
        font-family: 'Courier New', monospace !important; 
        color: #00FF00 !important; 
    }
    .main { background-color: #121212; color: #00FF00; }
    
    /* Native Metric Color Force Overrides */
    div[data-testid="stMetricValue"] { 
        font-size: 16px !important; 
        font-weight: bold !important; 
        color: #00FF00 !important; 
    }
    div[data-testid="stMetricLabel"] p { 
        font-size: 11px !important; 
        color: #FFFFFF !important; 
        text-transform: uppercase !important;
    }
    
    /* Document Informational Block Framing */
    .sop-card { 
        background-color: #161616; 
        border-left: 3px solid #00FF00; 
        padding: 8px; 
        margin-bottom: 10px; 
        color: #00FF00 !important;
    }
    .desc-text { 
        font-size: 10px !important; 
        color: #00FF00 !important; 
        font-style: italic; 
        margin-top: 2px; 
        line-height: 1.1; 
    }
    
    div[data-testid="stForm"] { background-color: #151515 !important; border: 1px solid #444444 !important; padding: 12px !important; }
    div.stButton > button:first-child { background-color: #00FF00 !important; color: #121212 !important; font-weight: bold; font-size: 11px !important; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ARRAY ---
st.title("🏭 HORIZON ADDIS TYRE S.C. 🔗")
st.markdown("### Product Industrialization & Quality Assurance — Live SPC Engine")
st.markdown("---")

# --- ACTIVE COMPONENT SELECTION MATRIX ---
col_sel1, col_sel2 = st.columns([2, 1])
with col_sel1:
    component_size = st.selectbox(
        "📂 Active Component Model & Dimension Selector",
        ["750-16 HT-99 Treadweight", "400-8 HT-60 Treadweight"]
    )
    st.markdown("<div class='desc-text'>👉 SUPERVISOR: Choose the active tire size currently running on the extrusion line.</div>", unsafe_allow_html=True)

# Assign structural profiles precisely based on your verified baseline files
if "750-16" in component_size:
    default_target, default_usl, default_lsl = 11.1600, 11.4948, 10.8252
else:
    default_target, default_usl, default_lsl = 2.0200, 2.0806, 1.9594

with col_sel2:
    tolerance_pct = st.number_input("Given Tolerance Percentage (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.1, format="%.1f")
    st.markdown("<div class='desc-text'>👉 SPEC: Allowed margin percentage. Controls threshold bands.</div>", unsafe_allow_html=True)

# --- DYNAMIC STRUCTURAL SEED DECKS ---
state_key = f"dataset_{component_size.replace(' ', '_')}"
if state_key not in st.session_state:
    np.random.seed(42)
    base_data = []
    for i in range(1, 21):
        if "750-16" in component_size:
            row_vals = np.random.normal(11.0137, 0.0395, 5)
        else:
            row_vals = np.random.normal(1.9990, 0.0216, 5)
        base_data.append([i] + list(row_vals))
    st.session_state[state_key] = pd.DataFrame(base_data, columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])

# --- PANEL 1: SPECIFICATION CONSTANTS BAR ---
st.markdown("### 🛠️ Process Specification Standards & Constants")
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

# --- PANEL 2: COMPACT CLEAN CONTROL METRICS BOARD ---
st.markdown("### 📊 Comprehensive Process Parameter Status Board")
r1_c1, r1_c2, r1_c3, r1_c4, r1_c5 = st.columns(5)
r2_c1, r2_c2, r2_c3, r2_c4, r2_c5 = st.columns(5)
r3_c1, r3_c2, r3_c3, r3_c4, r3_c5 = st.columns(5)

# Row 1 Indicators
r1_c1.metric(label="Target Center (A)", value=f"{target:.4f}")
r1_c2.metric(label="USL Limit (B)", value=f"{usl:.4f}")
r1_c3.metric(label="LSL Limit (C)", value=f"{lsl:.4f}")
r1_c4.metric(label="Range Mean R̄ (D)", value=f"{average_range:.4f}")
r1_c5.metric(label="Total Obs (E)", value=str(total_obs))

# Row 2 Indicators
r2_c1.metric(label="Grand Mean X̄̄ (F)", value=f"{grand_mean:.4f}")
r2_c2.metric(label="Gen. Movement (G)", value=f"{gen_movement:.4f}")
r2_c3.metric(label="Span Total (H)", value=f"{span_obs:.4f}")
r2_c4.metric(label="Grand Median (I)", value=f"{grand_median:.4f}")
r2_c5.metric(label="Obs Variance (J)", value=f"{variance_obs:.6f}")

# Row 3 Indicators
r3_c1.metric(label="Obs Max Value (K)", value=f"{obs_max:.4f}")
r3_c2.metric(label="Obs Min Value (L)", value=f"{obs_min:.4f}")
r3_c3.metric(label="Standard Dev σ (M)", value=f"{std_dev:.4f}")
r3_c4.metric(label="X̄ UCL / LCL (N)", value=f"{ucl_x:.3f} / {lcl_x:.3f}")
r3_c5.metric(label="R UCL / LCL (O)", value=f"{ucl_r:.3f} / {lcl_r:.3f}")

st.markdown("---")

# --- UNBROKEN LIVE WORKSPACE SPLIT (ENTRY & DATA VIEW GRID VISIBLE) ---
split_col1, split_col2 = st.columns([1.1, 1.9])

with split_col1:
    st.markdown(f"### 📥 Live Entry Stream Card ({component_size.split(' ')[0]})")
    st.markdown("<div class='sop-card'><b>📋 SUPERVISOR ENTRY SOP:</b> Measure 5 sample points, enter below, and submit.</div>", unsafe_allow_html=True)
    
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
    st.markdown("### 📋 Review Active Feed Storage Grid (Unbroken Parallel View)")
    st.dataframe(
        df.style.format("{:.4f}", subset=['X1', 'X2', 'X3', 'X4', 'X5', 'Mean', 'Range']),
        height=245,
        use_container_width=True
    )

st.markdown("---")

# --- SIDE-BY-SIDE ANALYTICS CONTROL PLOTS ---
st.markdown("### 📊 Parallel Live Diagnostics Control Graphs")
g_col1, g_col2, g_col3 = st.columns([1.4, 1.4, 1.2])

with g_col1:
    f_x = go.Figure()
    f_x.add_trace(go.Scatter(x=df['Sample'], y=df['Mean'], mode='lines+markers', name='Mean', line=dict(color='#00FF00', width=1.5)))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=grand_mean, x1=df['Sample'].max(), y1=grand_mean, line=dict(color="white", width=1.5))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_x, x1=df['Sample'].max(), y1=ucl_x, line=dict(color="red", dash="dash", width=1))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=lcl_x, x1=df['Sample'].max(), y1=lcl_x, line=dict(color="red", dash="dash", width=1))
    f_x.update_layout(title="<b>X-Bar Process Control Chart</b>", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="#00FF00", height=240, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(f_x, use_container_width=True)

with g_col2:
    f_r = go.Figure()
    f_r.add_trace(go.Scatter(x=df['Sample'], y=df['Range'], mode='lines+markers', name='Range', line=dict(color='#00FFFF', width=1.5)))
    f_r.add_shape(type="line", x0=df['Sample'].min(), y0=average_range, x1=df['Sample'].max(), y1=average_range, line=dict(color="white", width=1.5))
    f_r.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_r, x1=df['Sample'].max(), y1=ucl_r, line=dict(color="red", dash="dash", width=1))
    f_r.update_layout(title="<b>R-Bar Range Variability Chart</b>", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="#00FF00", height=240, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(f_r, use_container_width=True)

with g_col3:
    f_s = go.Figure()
    f_s.add_trace(go.Histogram(x=flattened, histnorm='probability density', marker_color='#444444', opacity=0.7))
    xs = np.linspace(min(flattened.min(), lsl, tol_max_val), max(flattened.max(), usl, tol_min_val), 100)
    ys = norm.pdf(xs, grand_mean, std_dev)
    f_s.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='#FFA500', width=1.5)))
    
    f_s.add_vline(x=lsl, line_dash="dot", line_color="red")
    f_s.add_vline(x=usl, line_dash="dot", line_color="red")
    f_s.add_vline(x=target, line_color="green")
    f_s.add_vline(x=tol_max_val, line_dash="dash", line_color="#00FF00")
    f_s.add_vline(x=tol_min_val, line_dash="dash", line_color="#00FF00")
    
    f_s.update_layout(title="<b>Process Curve vs Specs & Tol</b>", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="#00FF00", height=240, margin=dict(l=10, r=10, t=50, b=10), showlegend=False)
    st.plotly_chart(f_s, use_container_width=True)
