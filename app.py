import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

# --- INTERFACE MASTER STYLE MATRIX ---
st.set_page_config(page_title="Horizon Addis Tyre - SPC Center", layout="wide")

st.markdown("""
    <style>
    html, body, p, label, span, div { font-size: 12px !important; font-family: 'Courier New', monospace !important; color: #FFFFFF !important; }
    .main { background-color: #121212; color: #FFFFFF; }
    
    /* Variable Summary Grid Design */
    .summary-box {
        background-color: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 4px;
        padding: 6px 10px;
        margin-bottom: 2px;
    }
    .lbl { font-size: 10px !important; color: #888888; text-transform: uppercase; font-weight: bold; }
    .desc-text { font-size: 9px !important; color: #A0A0A0; font-style: italic; margin-top: 2px; line-height: 1.1; }
    .sop-card { background-color: #161616; border-left: 3px solid #FF4B4B; padding: 8px; margin-bottom: 10px; }
    
    .val-y { font-size: 14px !important; font-weight: bold; color: #FFFF00; }
    .val-c { font-size: 14px !important; font-weight: bold; color: #00FFFF; }
    .val-r { font-size: 14px !important; font-weight: bold; color: #FF4B4B; }
    .val-w { font-size: 14px !important; font-weight: bold; color: #FFFFFF; }
    
    div[data-testid="stForm"] { background-color: #151515 !important; border: 1px solid #444444 !important; padding: 12px !important; }
    div.stButton > button:first-child { background-color: #FF4B4B !important; color: white !important; font-weight: bold; font-size: 11px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🏭 HORIZON ADDIS TYRE S.C.")
st.markdown("### Product Industrialization & Quality Assurance — Live SPC Engine")
st.markdown("---")

# --- ACTIVE COMPONENT SELECTION MATRIX ---
col_sel1, col_sel2 = st.columns([2, 1])
with col_sel1:
    component_size = st.selectbox(
        "📂 Active Component Model & Dimension Selector",
        ["750-16 HT-99 Treadweight", "400-8 HT-60 Treadweight", "Custom Specification Size Sheet"]
    )
    st.markdown("<div class='desc-text'>👉 SUPERVISOR: Choose the active tire size currently running on the extrusion line. This loads the correct specification base.</div>", unsafe_allow_html=True)

# Baseline specifications setup matching selected profile
if "750-16" in component_size:
    default_target, default_usl, default_lsl = 11.1600, 11.4948, 10.8252
elif "400-8" in component_size:
    default_target, default_usl, default_lsl = 2.0200, 2.0806, 1.9594
else:
    default_target, default_usl, default_lsl = 10.0000, 10.3000, 9.7000

with col_sel2:
    tolerance_pct = st.number_input("Given Tolerance Percentage (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.1, format="%.1f")
    st.markdown("<div class='desc-text'>👉 SPEC: Allowed customer margin percentage (Standard is 3.0%). Controls the green threshold bands.</div>", unsafe_allow_html=True)

# --- DATA STORAGE MANAGEMENT Deck ---
state_key = f"dataset_{component_size.replace(' ', '_')}"
if state_key not in st.session_state:
    np.random.seed(42)
    base_data = []
    for i in range(1, 21):
        row_vals = np.random.normal(default_target - 0.146, (default_target * 0.0035), 5)
        base_data.append([i] + list(row_vals))
    st.session_state[state_key] = pd.DataFrame(base_data, columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])

# --- PANEL 1: ENGINEERING CONFIGURATION VARIABLES BAR (TOP) ---
st.markdown("### 🛠️ Process Specification Standards & Constants")
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: usl = st.number_input("USL (Upper Spec)", value=default_usl, format="%.4f")
with c2: target = st.number_input("Target Value", value=default_target, format="%.4f")
with c3: lsl = st.number_input("LSL (Lower Spec)", value=default_lsl, format="%.4f")
with c4: d2 = st.number_input("Shewhart d2", value=2.3330, format="%.4f")
with c5: A2 = st.number_input("Shewhart A2", value=0.5770, format="%.4f")
with c6: D4 = st.number_input("Shewhart D4", value=2.1150, format="%.4f")

# Interactive Tolerance Calculations: Max value = Spec - Tol, Min value = Spec + Tol
calculated_tolerance = target * (tolerance_pct / 100.0)
tol_max_val = target - calculated_tolerance
tol_min_val = target + calculated_tolerance

# Data Math Vector Processing
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

# --- PANEL 2: HIGH-CONTRAST METRICS INDICATOR MATRIX WITH LETTER DESCRIPTIONS ---
st.markdown("### 📊 Comprehensive Process Parameter Status Board")
r1_c1, r1_c2, r1_c3, r1_c4, r1_c5 = st.columns(5)
r2_c1, r2_c2, r2_c3, r2_c4, r2_c5 = st.columns(5)
r3_c1, r3_c2, r3_c3, r3_c4, r3_c5 = st.columns(5)

# Row 1 Elements
r1_c1.markdown(f'<div class="summary-box"><div class="lbl">Target Center</div><div class="val-w">{target:.4f}</div><div class="desc-text">A. Nominal design center weight for product blueprint accuracy.</div></div>', unsafe_allow_html=True)
r1_c2.markdown(f'<div class="summary-box"><div class="lbl">USL</div><div class="val-r">{usl:.4f}</div><div class="desc-text">B. Upper Spec Limit. Absolute max value allowed by PI & QA.</div></div>', unsafe_allow_html=True)
r1_c3.markdown(f'<div class="summary-box"><div class="lbl">LSL</div><div class="val-r">{lsl:.4f}</div><div class="desc-text">C. Lower Spec Limit. Absolute min value allowed before scrap.</div></div>', unsafe_allow_html=True)
r1_c4.markdown(f'<div class="summary-box"><div class="lbl">Range Mean (R̄)</div><div class="val-c">{average_range:.4f}</div><div class="desc-text">D. Average internal subgroup spread (Max - Min variance index).</div></div>', unsafe_allow_html=True)
r1_c5.markdown(f'<div class="summary-box"><div class="lbl">Total Observations</div><div class="val-w">{total_obs}</div><div class="desc-text">E. Combined count of individual measurement entries recorded.</div></div>', unsafe_allow_html=True)

# Row 2 Elements
r2_c1.markdown(f'<div class="summary-box"><div class="lbl">Grand Mean (X̄̄)</div><div class="val-w">{grand_mean:.4f}</div><div class="desc-text">F. Double bar process center weight across all recorded data.</div></div>', unsafe_allow_html=True)
r2_c2.markdown(f'<div class="summary-box"><div class="lbl">Gen. Movement</div><div class="val-y">{gen_movement:.4f}</div><div class="desc-text">G. Stepwise standard error change value between subgroups.</div></div>', unsafe_allow_html=True)
r2_c3.markdown(f'<div class="summary-box"><div class="lbl">Span Total</div><div class="val-y">{span_obs:.4f}</div><div class="desc-text">H. Absolute width between single highest and lowest point.</div></div>', unsafe_allow_html=True)
r2_c4.markdown(f'<div class="summary-box"><div class="lbl">Grand Median</div><div class="val-y">{grand_median:.4f}</div><div class="desc-text">I. Midpoint value splitting the sorted observation array.</div></div>', unsafe_allow_html=True)
r2_c5.markdown(f'<div class="summary-box"><div class="lbl">Obs Variance</div><div class="val-y">{variance_obs:.6f}</div><div class="desc-text">J. Statistical variance (Sigma squared) of all active points.</div></div>', unsafe_allow_html=True)

# Row 3 Elements
r3_c1.markdown(f'<div class="summary-box"><div class="lbl">Obs Max Value</div><div class="val-w">{obs_max:.4f}</div><div class="desc-text">K. Highest single raw component measurement found.</div></div>', unsafe_allow_html=True)
r3_c2.markdown(f'<div class="summary-box"><div class="lbl">Obs Min Value</div><div class="val-w">{obs_min:.4f}</div><div class="desc-text">L. Lowest single raw component measurement found.</div></div>', unsafe_allow_html=True)
r3_c3.markdown(f'<div class="summary-box"><div class="lbl">Standard Dev (σ)</div><div class="val-y">{std_dev:.4f}</div><div class="desc-text">M. Estimated process sigma computed via Shewhart R̄/d2 formula.</div></div>', unsafe_allow_html=True)
r3_c4.markdown(f'<div class="summary-box"><div class="lbl">X̄ UCL / LCL</div><div class="val-r">{ucl_x:.4f} / {lcl_x:.4f}</div><div class="desc-text">N. Shewhart control boundaries for subgroup averages.</div></div>', unsafe_allow_html=True)
r3_c5.markdown(f'<div class="summary-box"><div class="lbl">R UCL / LCL</div><div class="val-r">{ucl_r:.4f} / {lcl_r:.4f}</div><div class="desc-text">O. Upper variability boundaries tracking machine stability.</div></div>', unsafe_allow_html=True)

st.markdown("---")

# --- UNBROKEN LIVE WORKSPACE SPLIT (ENTRY & DATA VIEW GRID VISIBLE) ---
split_col1, split_col2 = st.columns([1.1, 1.9])

with split_col1:
    st.markdown(f"### 📥 Live Entry Stream Card ({component_size.split(' ')[0]})")
    
    st.markdown("""
    <div class='sop-card'>
        <b>📋 SUPERVISOR ENTRY SOP:</b><br>
        1. Measure 5 component points from the extrusion strip batch.<br>
        2. Input values sequentially into fields X1 through X5.<br>
        3. Press the red submission button to update charts live.
    </div>
    """, unsafe_allow_html=True)
    
    with st.form(key='horizontal_entry_deck', clear_on_submit=True):
        next_id = int(df['Sample'].max() + 1)
        st.markdown(f"**Target Sample Sequential Index:** `Subgroup #{next_id}`")
        v1 = st.number_input("Sub-Sample X1", value=float(df.iloc[-1]['X1']), format="%.4f")
        v2 = st.number_input("Sub-Sample X2", value=float(df.iloc[-1]['X2']), format="%.4f")
        v3 = st.number_input("Sub-Sample X3", value=float(df.iloc[-1]['X3']), format="%.4f")
        v4 = st.number_input("Sub-Sample X4", value=float(df.iloc[-1]['X4']), format="%.4f")
        v5 = st.number_input("Sub-Sample X5", value=float(df.iloc[-1]['X5']), format="%.4f")
        
        if st.form_submit_button(label="⚡ Append Subgroup to Engine Base"):
            new_row = pd.DataFrame([[next_id, v1, v2, v3, v4, v5]], columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])
            st.session_state[state_key] = pd.concat([st.session_state[state_key], new_row], ignore_index=True)
            st.rerun()

with split_col2:
    st.markdown("### 📋 Review Active Feed Storage Grid (Unbroken Parallel View)")
    st.markdown("<div class='desc-text' style='margin-bottom: 4px;'>👉 NOTE: This table maintains a record of previous entries. Verify row outputs here.</div>", unsafe_allow_html=True)
    st.dataframe(
        df.style.format("{:.4f}", subset=['X1', 'X2', 'X3', 'X4', 'X5', 'Mean', 'Range']),
        height=265,
        use_container_width=True
    )

st.markdown("---")

# --- SIDE-BY-SIDE ANALYTICS CONTROL PLOTS ---
st.markdown("### 📊 Parallel Live Diagnostics Control Graphs")
g_col1, g_col2, g_col3 = st.columns([1.4, 1.4, 1.2])

with g_col1:
    f_x = go.Figure()
    f_x.add_trace(go.Scatter(x=df['Sample'], y=df['Mean'], mode='lines+markers', name='Mean', line=dict(color='#FFFF00', width=1.5)))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=grand_mean, x1=df['Sample'].max(), y1=grand_mean, line=dict(color="white", width=1.5))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_x, x1=df['Sample'].max(), y1=ucl_x, line=dict(color="red", dash="dash", width=1))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=lcl_x, x1=df['Sample'].max(), y1=lcl_x, line=dict(color="red", dash="dash", width=1))
    f_x.update_layout(title="<b>X-Bar Process Control Chart</b><br><span style='font-size:10px; color:#A0A0A0;'>Tracks center weight drift. Yellow line must stay between red dashed limits.</span>", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white", height=240, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(f_x, use_container_width=True)

with g_col2:
    f_r = go.Figure()
    f_r.add_trace(go.Scatter(x=df['Sample'], y=df['Range'], mode='lines+markers', name='Range', line=dict(color='#00FFFF', width=1.5)))
    f_r.add_shape(type="line", x0=df['Sample'].min(), y0=average_range, x1=df['Sample'].max(), y1=average_range, line=dict(color="white", width=1.5))
    f_r.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_r, x1=df['Sample'].max(), y1=ucl_r, line=dict(color="red", dash="dash", width=1))
    f_r.update_layout(title="<b>R-Bar Range Variability Chart</b><br><span style='font-size:10px; color:#A0A0A0;'>Tracks machine uniformity. Cyan line must stay below red upper limit.</span>", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white", height=240, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(f_r, use_container_width=True)

with g_col3:
    f_s = go.Figure()
    f_s.add_trace(go.Histogram(x=flattened, histnorm='probability density', marker_color='#444444', opacity=0.7))
    xs = np.linspace(min(flattened.min(), lsl, tol_max_val), max(flattened.max(), usl, tol_min_val), 100)
    ys = norm.pdf(xs, grand_mean, std_dev)
    f_s.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='#FFA500', width=1.5)))
    
    # Specification Limits
    f_s.add_vline(x=lsl, line_dash="dot", line_color="red")
    f_s.add_vline(x=usl, line_dash="dot", line_color="red")
    f_s.add_vline(x=target, line_color="green")
    
    # Tolerance Limits
    f_s.add_vline(x=tol_max_val, line_dash="dash", line_color="#00FF00")
    f_s.add_vline(x=tol_min_val, line_dash="dash", line_color="#00FF00")
    
    f_s.update_layout(title="<b>Process Curve vs Specs & Tol</b><br><span style='font-size:10px; color:#A0A0A0;'>Histogram distribution must sit inside red spec and green tolerance lines.</span>", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white", height=240, margin=dict(l=10, r=10, t=50, b=10), showlegend=False)
    st.plotly_chart(f_s, use_container_width=True)
