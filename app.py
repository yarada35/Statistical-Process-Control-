import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

# --- ARCHITECTURAL VISUAL MASTER MATRIX (PREMIUM INDUSTRIAL SPEC) ---
st.set_page_config(page_title="Horizon Addis Tyre - SPC Center", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0A0A0C !important;
        font-family: 'Share Tech Mono', monospace !important;
        color: #00FF66 !important;
    }
    
    /* Artistic Background Title Banner Component */
    .factory-banner {
        background: linear-gradient(135deg, #0D2B18 0%, #040805 100%);
        border: 2px solid #00FF66;
        box-shadow: 0px 0px 25px rgba(0, 255, 102, 0.25);
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 25px;
        text-align: center;
    }
    .main-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        letter-spacing: 3px;
        color: #00FF66 !important;
        text-shadow: 0 0 15px rgba(0, 255, 102, 0.7);
        margin: 0;
    }
    .sub-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 12px !important;
        letter-spacing: 5px;
        color: #FFFFFF !important;
        margin-top: 6px;
        text-transform: uppercase;
        opacity: 0.8;
    }

    /* Lateral Table Layout Framework */
    .lateral-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 12px;
        margin-bottom: 15px;
    }
    .lateral-cell {
        background: #0F1214;
        border: 1px solid #1F2A25;
        border-radius: 4px;
        padding: 12px 15px;
        width: 20%;
        vertical-align: top;
        box-shadow: inset 0 0 12px rgba(0,0,0,0.9);
    }
    .cell-label {
        font-size: 11px !important;
        color: #8A9A92 !important;
        text-transform: uppercase;
        font-weight: bold;
    }
    .cell-value {
        font-size: 19px !important;
        font-weight: bold !important;
        color: #00FF66 !important;
        font-family: 'Orbitron', sans-serif !important;
        margin: 4px 0;
        text-shadow: 0 0 8px rgba(0, 255, 102, 0.4);
    }
    .cell-desc {
        font-size: 10px !important;
        color: #FF3333 !important;
        font-weight: bold;
        line-height: 1.2;
        margin-top: 4px;
    }
    
    /* High-Contrast Supervisor Input Form styling */
    div[data-testid="stForm"] {
        background-color: #111513 !important; 
        border: 2px solid #00FF66 !important; 
        border-radius: 6px !important;
        padding: 18px !important;
    }
    div[data-testid="stForm"] label p {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
    
    .stSelectbox div[data-baseweb="select"], .stNumberInput input {
        background-color: #1A221E !important;
        color: #00FF66 !important;
        border: 1px solid #00FF66 !important;
    }
    
    div.stButton > button:first-child { 
        background-color: #00FF66 !important; 
        color: #0A0A0C !important; 
        font-weight: 900 !important; 
        border: none !important;
        width: 100% !important;
    }
    
    .sop-card { 
        background-color: #161212; 
        border-left: 3px solid #FF3333; 
        padding: 10px; 
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- ARTISTIC TITLE BACKGROUND LAYOUT BANNER ---
st.markdown("""
    <div class="factory-banner">
        <div class="main-title">⛓️ HORIZON ADDIS TYRE S.C. ⚙️ 🔗</div>
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
    for i in range(1, 16):
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

# Dynamic Calculations Core
calculated_tolerance = target * (tolerance_pct / 100.0)
tol_max_val = target - calculated_tolerance
tol_min_val = target + calculated_tolerance

df = st.session_state[state_key].copy()
current_subgroups = len(df)

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

# --- PANEL 2: LATERAL MATRIX DISPLAY ---
st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:2px;'>📊 LIVE PROCESS SUMMARY PARAMETERS MATRIX</p>", unsafe_allow_html=True)
st.markdown(f"""
<table class="lateral-table">
    <tr>
        <td class="lateral-cell"><div class="cell-label">Target Center</div><div class="cell-value">{target:.4f}</div><div class="cell-desc">A. Nominal design center weight for product blueprint accuracy.</div></td>
        <td class="lateral-cell"><div class="cell-label">USL</div><div class="cell-value">{usl:.4f}</div><div class="cell-desc">B. Upper Spec Limit. Absolute max value allowed by PI & QA.</div></td>
        <td class="lateral-cell"><div class="cell-label">LSL</div><div class="cell-value">{lsl:.4f}</div><div class="cell-desc">C. Lower Spec Limit. Absolute min value allowed before scrap.</div></td>
        <td class="lateral-cell"><div class="cell-label">Range Mean (R̄)</div><div class="cell-value">{average_range:.4f}</div><div class="cell-desc">D. Average internal subgroup spread (Max - Min variance index).</div></td>
        <td class="lateral-cell"><div class="cell-label">Total Observations</div><div class="cell-value">{total_obs} / 100</div><div class="cell-desc">E. Combined count of individual measurement entries recorded.</div></td>
    </tr>
    <tr>
        <td class="lateral-cell"><div class="cell-label">Grand Mean (X̄̄)</div><div class="cell-value">{grand_mean:.4f}</div><div class="cell-desc">F. Double bar process center weight across all recorded data.</div></td>
        <td class="lateral-cell"><div class="cell-label">Gen. Movement</div><div class="cell-value">{gen_movement:.4f}</div><div class="cell-desc">G. Stepwise standard error change value between subgroups.</div></td>
        <td class="lateral-cell"><div class="cell-label">Span Total</div><div class="cell-value">{span_obs:.4f}</div><div class="cell-desc">H. Absolute width between single highest and lowest point.</div></td>
        <td class="lateral-cell"><div class="cell-label">Grand Median</div><div class="cell-value">{grand_median:.4f}</div><div class="cell-desc">I. Midpoint value splitting the sorted observation array.</div></td>
        <td class="lateral-cell"><div class="cell-label">Obs Variance</div><div class="cell-value">{variance_obs:.6f}</div><div class="cell-desc">J. Statistical variance (Sigma squared) of all active points.</div></td>
    </tr>
    <tr>
        <td class="lateral-cell"><div class="cell-label">Obs Max Value</div><div class="cell-value">{obs_max:.4f}</div><div class="cell-desc">K. Highest single raw component measurement found.</div></td>
        <td class="lateral-cell"><div class="cell-label">Obs Min Value</div><div class="cell-value">{obs_min:.4f}</div><div class="cell-desc">L. Lowest single raw component measurement found.</div></td>
        <td class="lateral-cell"><div class="cell-label">Standard Dev (σ)</div><div class="cell-value">{std_dev:.4f}</div><div class="cell-desc">M. Estimated process sigma computed via Shewhart R̄/d2 formula.</div></td>
        <td class="lateral-cell"><div class="cell-label">X̄ UCL / LCL</div><div class="cell-value">{ucl_x:.4f} / {lcl_x:.4f}</div><div class="cell-desc">N. Shewhart control boundaries for subgroup averages.</div></td>
        <td class="lateral-cell"><div class="cell-label">R UCL / LCL</div><div class="cell-value">{ucl_r:.4f} / {lcl_r:.4f}</div><div class="cell-desc">O. Upper variability boundaries tracking machine stability.</div></td>
    </tr>
</table>
""", unsafe_allow_html=True)

st.markdown("---")

# --- UNBROKEN STREAM LAYOUT SPLIT ---
split_col1, split_col2 = st.columns([1.1, 1.9])

with split_col1:
    st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:1px;'>📥 LIVE SUBGROUP DATASTREAM ENTRY</p>", unsafe_allow_html=True)
    if current_subgroups >= 20:
        st.error(f"🛑 MAXIMUM CAP REACHED: Engine contains {current_subgroups} Subgroups ({total_obs} samples). Entry closed.")
        if st.button("🔄 Reset Dataset to Baseline"):
            del st.session_state[state_key]
            st.rerun()
    else:
        st.markdown(f"<div class='sop-card'><b>📋 SOP:</b> Record 5 inputs. Target Limit: <b>{current_subgroups}/20 Subgroups</b></div>", unsafe_allow_html=True)
        with st.form(key=f"form_{state_key}", clear_on_submit=True):
            next_id = current_subgroups + 1
            st.markdown(f"<span style='color:#FFFFFF; font-weight:bold;'>Target Subgroup Sequential Index: Subgroup #{next_id} / 20</span>", unsafe_allow_html=True)
            v1 = st.number_input("Sub-Sample Measurement X1", value=float(df.iloc[-1]['X1']), format="%.4f", key=f"x1_{state_key}")
            v2 = st.number_input("Sub-Sample Measurement X2", value=float(df.iloc[-1]['X2']), format="%.4f", key=f"x2_{state_key}")
            v3 = st.number_input("Sub-Sample Measurement X3", value=float(df.iloc[-1]['X3']), format="%.4f", key=f"x3_{state_key}")
            v4 = st.number_input("Sub-Sample Measurement X4", value=float(df.iloc[-1]['X4']), format="%.4f", key=f"x4_{state_key}")
            v5 = st.number_input("Sub-Sample Measurement X5", value=float(df.iloc[-1]['X5']), format="%.4f", key=f"x5_{state_key}")
            
            if st.form_submit_button(label="⚡ APPEND SUBGROUP TO ENGINE BASE"):
                new_row = pd.DataFrame([[next_id, v1, v2, v3, v4, v5]], columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])
                st.session_state[state_key] = pd.concat([st.session_state[state_key], new_row], ignore_index=True)
                st.rerun()

with split_col2:
    st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:1px;'>📋 UNBROKEN ACTIVE DATASTORE STORAGE ENGINE (RAW + CALCULATED ANALYSIS)</p>", unsafe_allow_html=True)
    # Displays raw sample columns alongside calculated values side-by-side
    st.dataframe(
        df.style.format("{:.4f}", subset=['X1', 'X2', 'X3', 'X4', 'X5', 'Mean', 'Range']),
        height=270,
        use_container_width=True
    )

st.markdown("---")

# --- SIDE-BY-SIDE ANALYTICS CONTROL PLOTS ---
st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:2px;'>📊 PARALLEL PROCESS DIAGNOSTICS CONTROL GRAPHS (LOCKED VIEWMODE)</p>", unsafe_allow_html=True)
g_col1, g_col2, g_col3 = st.columns([1.4, 1.4, 1.2])

with g_col1:
    f_x = go.Figure()
    f_x.add_trace(go.Scatter(x=df['Sample'], y=df['Mean'], mode='lines+markers', name='Mean', line=dict(color='#00FF66', width=2)))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=grand_mean, x1=df['Sample'].max(), y1=grand_mean, line=dict(color="white", width=1.5))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_x, x1=df['Sample'].max(), y1=ucl_x, line=dict(color="red", dash="dash", width=1.5))
    f_x.add_shape(type="line", x0=df['Sample'].min(), y0=lcl_x, x1=df['Sample'].max(), y1=lcl_x, line=dict(color="red", dash="dash", width=1.5))
    f_x.update_layout(title="<b>X-Bar Process Control Chart</b>", paper_bgcolor='#0A0A0C', plot_bgcolor='#0F1214', font_color="#00FF66", height=240, margin=dict(l=10, r=10, t=50, b=10))
    # config={'staticPlot': True} completely freezes the chart to block human manipulation or zooming
    st.plotly_chart(f_x, use_container_width=True, config={'staticPlot': True})

with g_col2:
    f_r = go.Figure()
    f_r.add_trace(go.Scatter(x=df['Sample'], y=df['Range'], mode='lines+markers', name='Range', line=dict(color='#00FFFF', width=2)))
    f_r.add_shape(type="line", x0=df['Sample'].min(), y0=average_range, x1=df['Sample'].max(), y1=average_range, line=dict(color="white", width=1.5))
    f_r.add_shape(type="line", x0=df['Sample'].min(), y0=ucl_r, x1=df['Sample'].max(), y1=ucl_r, line=dict(color="red", dash="dash", width=1.5))
    f_r.update_layout(title="<b>R-Bar Range Variability Chart</b>", paper_bgcolor='#0A0A0C', plot_bgcolor='#0F1214', font_color="#00FF66", height=240, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(f_r, use_container_width=True, config={'staticPlot': True})

with g_col3:
    f_s = go.Figure()
    f_s.add_trace(go.Histogram(x=flattened, histnorm='probability density', marker_color='#1A2620', opacity=0.85, marker_line=dict(width=1, color='#00FF66')))
    xs = np.linspace(min(flattened.min(), lsl, tol_max_val), max(flattened.max(), usl, tol_min_val), 100)
    ys = norm.pdf(xs, grand_mean, std_dev)
    f_s.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='#FFBB00', width=2)))
    
    f_s.add_vline(x=lsl, line_dash="dot", line_color="red", line_width=1.5)
    f_s.add_vline(x=usl, line_dash="dot", line_color="red", line_width=1.5)
    f_s.add_vline(x=target, line_color="#00FF66", line_width=1.5)
    f_s.add_vline(x=tol_max_val, line_dash="dash", line_color="#FF3333", line_width=1.5)
    f_s.add_vline(x=tol_min_val, line_dash="dash", line_color="#FF3333", line_width=1.5)
    
    f_s.update_layout(title="<b>Process Curve vs Specs & Tol</b>", paper_bgcolor='#0A0A0C', plot_bgcolor='#0F1214', font_color="#00FF66", height=240, margin=dict(l=10, r=10, t=50, b=10), showlegend=False)
    st.plotly_chart(f_s, use_container_width=True, config={'staticPlot': True})
