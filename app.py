import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
import os

# --- ARCHITECTURAL VISUAL MASTER MATRIX (PREMIUM INDUSTRIAL SPEC) ---
st.set_page_config(page_title="Horizon Addis Tyre - SPC Center", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght=400;700&family=Share+Tech+Mono&display=swap');
    
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
    
    .stSelectbox div[data-baseweb="select"], .stNumberInput input, .stTextInput input {
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

    .print-frame {
        background-color: #050507 !important;
        border: 2px dashed #FF3333 !important;
        padding: 25px;
        border-radius: 6px;
        margin-top: 40px;
    }
    
    .capability-metric {
        background: #0E1112;
        border: 1px solid #FF3333;
        border-radius: 4px;
        padding: 10px;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Custom sizing addition area layout */
    .management-card {
        background-color: #0D1117 !important;
        border: 1px solid #FFBB00 !important;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
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

# --- IN-MEMORY REGISTRY SYNC PLATFORM ---
if "COMPONENT_REGISTRY" not in st.session_state:
    st.session_state["COMPONENT_REGISTRY"] = {
        "750-16 HT-99 Treadweight": {"target": 11.1600, "usl": 11.4948, "lsl": 10.8252, "seed_mean": 11.0137, "seed_sigma": 0.0395},
        "400-8 HT-60 Treadweight": {"target": 2.0200, "usl": 2.0806, "lsl": 1.9594, "seed_mean": 1.9989, "seed_sigma": 0.0216},
        "Size 3 Model Profile": {"target": 5.5000, "usl": 5.6650, "lsl": 5.3350, "seed_mean": 5.4850, "seed_sigma": 0.0310},
        "Size 4 Model Profile": {"target": 8.2000, "usl": 8.4460, "lsl": 7.9540, "seed_mean": 8.1920, "seed_sigma": 0.0280},
        "Size 5 Model Profile": {"target": 3.1500, "usl": 3.2445, "lsl": 3.0555, "seed_mean": 3.1410, "seed_sigma": 0.0190}
    }

if "selected_size_index" not in st.session_state:
    st.session_state["selected_size_index"] = 0

if "previous_component_selection" not in st.session_state:
    st.session_state["previous_component_selection"] = ""

options_list = list(st.session_state["COMPONENT_REGISTRY"].keys())

# --- ACTIVE COMPONENT SELECTION MATRIX ---
col_sel1, col_sel2 = st.columns([2, 1])
with col_sel1:
    if st.session_state["selected_size_index"] >= len(options_list):
        st.session_state["selected_size_index"] = 0
        
    component_size = st.selectbox(
        "📂 Active Component Model & Dimension Selector",
        options=options_list,
        index=st.session_state["selected_size_index"],
        key="component_selector_widget"
    )
    st.session_state["selected_size_index"] = options_list.index(component_size)

with col_sel2:
    tolerance_pct = st.number_input("Given Tolerance Percentage (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.1, format="%.1f")

if st.session_state["previous_component_selection"] != component_size:
    st.session_state["previous_component_selection"] = component_size
    old_clean = component_size.replace(' ', '_').replace('-', '_').replace('.', '_').replace('/', '_')
    st.session_state.pop(f"dataset_{old_clean}", None)

current_config = st.session_state["COMPONENT_REGISTRY"][component_size]

# --- RE-ENGINEERED UNBROKEN PROFILE EDIT & RENAMING MATRIX ENGINE ---
with st.expander("📝 Keyboard Writing: Rename Active Selection & Rewrite Core Specifications"):
    st.markdown("<div class='management-card' style='border: 1px solid #00FF66;'>", unsafe_allow_html=True)
    
    with st.form(key=f"rename_specification_form_{component_size.replace(' ', '_')}"):
        st.markdown(f"<p style='color:#FFFFFF; font-weight:bold;'>Editing Profile Target: <span style='color:#00FF66;'>{component_size}</span></p>", unsafe_allow_html=True)
        
        edit_name = st.text_input("✏️ Keyboard Change Name String", value=component_size)
        
        ec1, ec2, ec3 = st.columns(3)
        with ec1: edit_target = ec1.number_input("Modify Target Center", value=float(current_config["target"]), format="%.4f")
        with ec2: edit_usl = ec2.number_input("Modify Upper Spec Limit (USL)", value=float(current_config["usl"]), format="%.4f")
        with ec3: edit_lsl = ec3.number_input("Modify Lower Spec Limit (LSL)", value=float(current_config["lsl"]), format="%.4f")
        
        submit_spec_changes = st.form_submit_button("⚡ EXECUTE PROFILE REWRITE & FILE RE-LINK")
        
        if submit_spec_changes:
            new_clean_name = edit_name.strip()
            if new_clean_name != "":
                old_csv_clean = component_size.replace(' ', '_').replace('-', '_').replace('.', '_').replace('/', '_')
                new_csv_clean = new_clean_name.replace(' ', '_').replace('-', '_').replace('.', '_').replace('/', '_')
                
                st.session_state.pop(f"dataset_{old_csv_clean}", None)
                st.session_state.pop(f"dataset_{new_csv_clean}", None)
                st.session_state["COMPONENT_REGISTRY"].pop(component_size, None)
                
                st.session_state["COMPONENT_REGISTRY"][new_clean_name] = {
                    "target": edit_target,
                    "usl": edit_usl,
                    "lsl": edit_lsl,
                    "seed_mean": edit_target,
                    "seed_sigma": max((edit_usl - edit_lsl) / 10.0, 0.001)
                }
                
                if old_csv_clean != new_csv_clean:
                    if os.path.exists(f"spc_datastore_{old_csv_clean}.csv"):
                        try:
                            os.rename(f"spc_datastore_{old_csv_clean}.csv", f"spc_datastore_{new_csv_clean}.csv")
                        except Exception:
                            pass
                
                updated_options_list = list(st.session_state["COMPONENT_REGISTRY"].keys())
                st.session_state["selected_size_index"] = updated_options_list.index(new_clean_name)
                st.session_state["component_selector_widget"] = new_clean_name
                st.success(f"✓ Profile successfully updated to '{new_clean_name}'")
                st.rerun()
            else:
                st.error("⚠️ Keyboard entry error: Field target validation string blank.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- EXPANDABLE: CREATE NEW SIZE CONTROL PANEL INTERFACE ---
with st.expander("➕ Define & Type Brand New Custom Component Size Profile"):
    st.markdown("<div class='management-card'>", unsafe_allow_html=True)
    new_size_name = st.text_input(
        "⌨️ Setup Initial Profile Unique Name Signature String", 
        placeholder="e.g., 195 R 15",
        key="keyboard_size_input"
    )
    
    nc1, nc2, nc3 = st.columns(3)
    with nc1: new_target = nc1.number_input("Design Target Blueprint Value", value=10.0000, format="%.4f")
    with nc2: new_usl = nc2.number_input("Upper Specification Limit (USL)", value=10.3000, format="%.4f")
    with nc3: new_lsl = nc3.number_input("Lower Specification Limit (LSL)", value=9.7000, format="%.4f")
    
    if st.button("💾 SAVE CUSTOM STRING TO DROP-DOWN"):
        cleaned_input_name = new_size_name.strip()
        if cleaned_input_name != "":
            if cleaned_input_name not in st.session_state["COMPONENT_REGISTRY"]:
                st.session_state["COMPONENT_REGISTRY"][cleaned_input_name] = {
                    "target": new_target,
                    "usl": new_usl,
                    "lsl": new_lsl,
                    "seed_mean": new_target,
                    "seed_sigma": max((new_usl - new_lsl) / 10.0, 0.001)
                }
                
                # FIX: Pre-clear stale dataset session structures and sync components instantly
                new_clean = cleaned_input_name.replace(' ', '_').replace('-', '_').replace('.', '_').replace('/', '_')
                st.session_state.pop(f"dataset_{new_clean}", None)
                st.session_state.pop(f"archive_{new_clean}", None)
                
                updated_options = list(st.session_state["COMPONENT_REGISTRY"].keys())
                st.session_state["selected_size_index"] = updated_options.index(cleaned_input_name)
                st.session_state["component_selector_widget"] = cleaned_input_name
                
                st.success(f"✓ '{cleaned_input_name}' recorded dynamically. Dropdown shifted.")
                st.rerun()
            else:
                st.warning(f"⚠️ Component sizing tag designation '{cleaned_input_name}' already exists in current registry configuration.")
        else:
            st.error("⚠️ Keyboard entry error: The text input field cannot be left blank.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- ISO-BALANCED EXPANDED DANGER ZONE CONTROL ---
with st.expander("⚠️ DANGER ZONE: CORE RECORD PURGE & HISTORY WIPE"):
    st.markdown("<div class='management-card' style='border: 1px solid #FF3333;'>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#FFFFFF;'>You are about to completely wipe all active history data logs and files for: <b style='color:#FF3333;'>{component_size}</b></p>", unsafe_allow_html=True)
    
    if st.button("🗑️ PURGE CRITICAL DATASTORE HISTORY & RESTART AT SAMPLE #1", key="isolated_danger_purge_btn"):
        purge_clean = component_size.replace(' ', '_').replace('-', '_').replace('.', '_').replace('/', '_')
        target_csv_file = f"spc_datastore_{purge_clean}.csv"
        
        if os.path.exists(target_csv_file):
            os.remove(target_csv_file)
            
        st.session_state.pop(f"dataset_{purge_clean}", None)
        st.session_state.pop(f"archive_{purge_clean}", None)
        st.success(f"💥 Datastore history for '{component_size}' cleared completely. Counter reset to 1.")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Reload active specifications cleanly to allow instant global UI rendering update
config = st.session_state["COMPONENT_REGISTRY"][component_size]
default_target = config["target"]
default_usl = config["usl"]
default_lsl = config["lsl"]

# --- FILE HARDWARE PERSISTENCE ENGINE ---
clean_name = component_size.replace(' ', '_').replace('-', '_').replace('.', '_').replace('/', '_')
CSV_FILE_PATH = f"spc_datastore_{clean_name}.csv"

# FIX: Return a completely empty dataframe schema (0 rows) so Sample #1 must be manually typed
def generate_fresh_baseline():
    return pd.DataFrame(columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])

state_key = f"dataset_{clean_name}"
archive_key = f"archive_{clean_name}"

if state_key not in st.session_state:
    if os.path.exists(CSV_FILE_PATH):
        try:
            df_active = pd.read_csv(CSV_FILE_PATH)
        except Exception:
            df_active = generate_fresh_baseline()
            df_active.to_csv(CSV_FILE_PATH, index=False)
    else:
        df_active = generate_fresh_baseline()
        df_active.to_csv(CSV_FILE_PATH, index=False)
    st.session_state[state_key] = df_active
else:
    df_active = st.session_state[state_key]

# --- PANEL 1: SPECIFICATION CONSTANTS BAR ---
st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:2px;'>🛠️ PROCESS SPECIFICATION STANDARDS & CONSTANTS</p>", unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: usl = st.number_input("USL (Upper Spec)", value=default_usl, format="%.4f")
with c2: target = st.number_input("Target Value", value=default_target, format="%.4f")
with c3: lsl = st.number_input("LSL (Lower Spec)", value=default_lsl, format="%.4f")
with c4: d2 = st.number_input("Shewhart d2", value=2.3330, format="%.4f")
with c5: A2 = st.number_input("Shewhart A2", value=0.5770, format="%.4f")
with c6: D4 = st.number_input("Shewhart D4", value=2.1150, format="%.4f")

calculated_tolerance = target * (tolerance_pct / 100.0)
tol_max_val = target - calculated_tolerance
tol_min_val = target + calculated_tolerance

df = st.session_state[state_key].copy()
current_subgroups = len(df)

# --- CALCULATE STATISTICS LOGIC ONLY IF DATA EXISTS ---
if not df.empty:
    df['Sample'] = df['Sample'].astype(int)
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
    std_dev = average_range / d2 if average_range > 0 else 0.001
    overall_std = float(np.std(flattened, ddof=1)) if len(flattened) > 1 else 0.001

    ucl_x = grand_mean + (A2 * average_range)
    lcl_x = grand_mean - (A2 * average_range)
    ucl_r = D4 * average_range
    lcl_r = 0.0
    gen_movement = float(np.std(df['Mean'].diff().dropna())) if len(df) > 1 else 0.0000
else:
    # Safe fallback constants for empty registries
    total_obs = 0
    grand_mean = target
    average_range = 0.0000
    span_obs = 0.0000
    grand_median = target
    variance_obs = 0.0000
    obs_max = target
    obs_min = target
    std_dev = 0.001
    overall_std = 0.001
    ucl_x = target
    lcl_x = target
    ucl_r = 0.0
    lcl_r = 0.0
    gen_movement = 0.0000
    flattened = np.array([target])

def build_plots(data_frame, flat_array):
    fig_x = go.Figure()
    if not data_frame.empty:
        fig_x.add_trace(go.Scatter(x=data_frame['Sample'], y=data_frame['Mean'], mode='lines+markers', name='Mean', line=dict(color='#00FF66', width=2)))
        x_min, x_max = data_frame['Sample'].min(), data_frame['Sample'].max()
    else:
        x_min, x_max = 1, 20
        
    fig_x.add_shape(type="line", x0=x_min, y0=grand_mean, x1=x_max, y1=grand_mean, line=dict(color="white", width=1.5))
    fig_x.add_shape(type="line", x0=x_min, y0=ucl_x, x1=x_max, y1=ucl_x, line=dict(color="red", dash="dash", width=1.5))
    fig_x.add_shape(type="line", x0=x_min, y0=lcl_x, x1=x_max, y1=lcl_x, line=dict(color="red", dash="dash", width=1.5))
    fig_x.update_layout(title="<b>X-Bar Process Control Chart</b>", paper_bgcolor='#0A0A0C', plot_bgcolor='#0F1214', font_color="#00FF66", height=230, margin=dict(l=10, r=10, t=40, b=10))
    
    fig_r = go.Figure()
    if not data_frame.empty:
        fig_r.add_trace(go.Scatter(x=data_frame['Sample'], y=data_frame['Range'], mode='lines+markers', name='Range', line=dict(color='#00FFFF', width=2)))
    fig_r.add_shape(type="line", x0=x_min, y0=average_range, x1=x_max, y1=average_range, line=dict(color="white", width=1.5))
    fig_r.add_shape(type="line", x0=x_min, y0=ucl_r, x1=x_max, y1=ucl_r, line=dict(color="red", dash="dash", width=1.5))
    fig_r.update_layout(title="<b>R-Bar Range Variability Chart</b>", paper_bgcolor='#0A0A0C', plot_bgcolor='#0F1214', font_color="#00FF66", height=230, margin=dict(l=10, r=10, t=40, b=10))
    
    fig_s = go.Figure()
    fig_s.add_trace(go.Histogram(x=flat_array, histnorm='probability density', marker_color='#1A2620', opacity=0.85, marker_line=dict(width=1, color='#00FF66')))
    xs = np.linspace(min(flat_array.min(), lsl, tol_max_val), max(flat_array.max(), usl, tol_min_val), 100)
    ys = norm.pdf(xs, grand_mean, std_dev if std_dev > 0 else 0.001)
    fig_s.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='#FFBB00', width=2)))
    fig_s.add_vline(x=lsl, line_dash="dot", line_color="red", line_width=1.5)
    fig_s.add_vline(x=usl, line_dash="dot", line_color="red", line_width=1.5)
    fig_s.add_vline(x=target, line_color="#00FF66", line_width=1.5)
    fig_s.add_vline(x=tol_max_val, line_dash="dash", line_color="#FF3333", line_width=1.5)
    fig_s.add_vline(x=tol_min_val, line_dash="dash", line_color="#FF3333", line_width=1.5)
    fig_s.update_layout(title="<b>Process Curve vs Specs & Tol</b>", paper_bgcolor='#0A0A0C', plot_bgcolor='#0F1214', font_color="#00FF66", height=230, margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    
    return fig_x, fig_r, fig_s

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
        
        if st.button("💾 Archive, Print and Reset to Sample #1"):
            cp = (usl - lsl) / (6 * std_dev) if std_dev > 0 else 0
            cpu = (usl - grand_mean) / (3 * std_dev) if std_dev > 0 else 0
            cpl = (grand_mean - lsl) / (3 * std_dev) if std_dev > 0 else 0
            cpk = min(cpu, cpl)
            
            pp = (usl - lsl) / (6 * overall_std) if overall_std > 0 else 0
            ppu = (usl - grand_mean) / (3 * overall_std) if overall_std > 0 else 0
            ppl = (grand_mean - lsl) / (3 * overall_std) if overall_std > 0 else 0
            ppk = min(ppu, ppl)
            
            st.session_state[archive_key] = {
                'df': df.copy(),
                'flat': flattened.copy(),
                'metrics': {'cp': cp, 'cpk': cpk, 'pp': pp, 'ppk': ppk, 'mean': grand_mean, 'sigma': std_dev}
            }
            
            df_fresh = generate_fresh_baseline()
            df_fresh.to_csv(CSV_FILE_PATH, index=False)
            st.session_state[state_key] = df_fresh
            st.rerun()
    else:
        st.markdown(f"<div class='sop-card'><b>📋 SOP:</b> Record 5 inputs. Current Batch Count: <b>{current_subgroups}/20 Subgroups</b></div>", unsafe_allow_html=True)
        
        with st.form(key=f"data_entry_form_{clean_name}_{current_subgroups}"):
            next_id = current_subgroups + 1
            st.markdown(f"<div style='color:#FFFFFF; font-weight:bold;'>Target Subgroup Sequential Index: Subgroup #{next_id} / 20</div>", unsafe_allow_html=True)
            
            v1 = st.number_input("Sub-Sample Measurement X1", value=float(default_target), format="%.4f")
            v2 = st.number_input("Sub-Sample Measurement X2", value=float(default_target), format="%.4f")
            v3 = st.number_input("Sub-Sample Measurement X3", value=float(default_target), format="%.4f")
            v4 = st.number_input("Sub-Sample Measurement X4", value=float(default_target), format="%.4f")
            v5 = st.number_input("Sub-Sample Measurement X5", value=float(default_target), format="%.4f")
            
            if st.form_submit_button(label="⚡ APPEND SUBGROUP TO ENGINE BASE"):
                new_row = pd.DataFrame([[next_id, v1, v2, v3, v4, v5]], columns=['Sample', 'X1', 'X2', 'X3', 'X4', 'X5'])
                if df.empty:
                    df_updated = new_row
                else:
                    df_updated = pd.concat([df[['Sample', 'X1', 'X2', 'X3', 'X4', 'X5']], new_row], ignore_index=True)
                
                df_updated.to_csv(CSV_FILE_PATH, index=False)
                st.session_state[state_key] = df_updated
                st.rerun()

with split_col2:
    st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:1px;'>📋 UNBROKEN ACTIVE DATASTORE STORAGE ENGINE (RAW + CALCULATED ANALYSIS)</p>", unsafe_allow_html=True)
    if not df.empty:
        st.dataframe(
            df.style.format("{:.4f}", subset=['X1', 'X2', 'X3', 'X4', 'X5', 'Mean', 'Range']),
            height=270,
            use_container_width=True
        )
    else:
        st.info("💡 Storage engine empty. Please append Subgroup #1 to start data aggregation.")

st.markdown("---")

# --- PARALLEL PROCESS DIAGNOSTICS CONTROL GRAPHS ---
st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:2px;'>📊 PARALLEL PROCESS DIAGNOSTICS CONTROL GRAPHS (LOCKED VIEWMODE)</p>", unsafe_allow_html=True)
g1, g2, g3 = st.columns([1.4, 1.4, 1.2])
fx, fr, fs = build_plots(df, flattened)
g1.plotly_chart(fx, use_container_width=True, config={'staticPlot': True})
g2.plotly_chart(fr, use_container_width=True, config={'staticPlot': True})
g3.plotly_chart(fs, use_container_width=True, config={'staticPlot': True})

# --- FINAL HISTORICAL RESULTS & PROCESS CAPABILITY STUDY PRINT LEDGER ---
if archive_key in st.session_state:
    arch = st.session_state[archive_key]
    st.markdown("<div class='print-frame'>", unsafe_allow_html=True)
    st.markdown("## 🖨️ FINAL CONSOLIDATED SPECIFICATION & CAPABILITY REPORT")
    st.markdown(f"#### PI & QA Division — Shift Performance Verification Ledger ({component_size})")
    
    m = arch['metrics']
    
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.markdown(f'<div class="capability-metric"><p style="color:#8A9A92;font-size:11px;margin:0;">POTENTIAL CAPABILITY (Cp)</p><h3 style="color:#00FF66;margin:5px 0;">{m["cp"]:.4f}</h3></div>', unsafe_allow_html=True)
    mc2.markdown(f'<div class="capability-metric"><p style="color:#8A9A92;font-size:11px;margin:0;">MINIMUM PROCESS INDEX (Cpk)</p><h3 style="color:#00FF66;margin:5px 0;">{m["cpk"]:.4f}</h3></div>', unsafe_allow_html=True)
    mc3.markdown(f'<div class="capability-metric"><p style="color:#8A9A92;font-size:11px;margin:0;">TOTAL PERFORMANCE (Pp)</p><h3 style="color:#00FF66;margin:5px 0;">{m["pp"]:.4f}</h3></div>', unsafe_allow_html=True)
    mc4.markdown(f'<div class="capability-metric"><p style="color:#8A9A92;font-size:11px;margin:0;">PERFORMANCE INDEX (Ppk)</p><h3 style="color:#00FF66;margin:5px 0;">{m["ppk"]:.4f}</h3></div>', unsafe_allow_html=True)
    
    st.markdown("#### 📝 CRITICAL QUALITY PERFORMANCE AUDIT OBSERVATIONS:")
    if m['cpk'] >= 1.33:
        st.markdown(f"🟢 **Process Status: HIGHLY CAPABLE ($C_{{pk}}$ = {m['cpk']:.4f}).** The extrusion variant dispersion profile sits safely inside specification boundaries. System exhibits complete statistical stability.")
    elif m['cpk'] >= 1.00:
        st.markdown(f"🟡 **Process Status: MARGINALLY CAPABLE ($C_{{pk}}$ = {m['cpk']:.4f}).** Center shifts detected. Increase close die pressure maintenance monitoring loops immediately.")
    else:
        st.markdown(f"🔴 **Process Status: CRITICAL NON-COMPLIANT ($C_{{pk}}$ = {m['cpk']:.4f}).** Variance profile exceeds standard deviation ceiling. Immediate mechanical verification required on head temperatures.")
        
    st.markdown("---")
    st.markdown("**Archived Raw Data and Computed Limits:**")
    st.dataframe(
        arch['df'].style.format("{:.4f}", subset=['X1', 'X2', 'X3', 'X4', 'X5', 'Mean', 'Range']),
        use_container_width=True
    )
    st.markdown("---")
    st.markdown("**Archived Analytical Control Graphs:**")
    p1, p2, p3 = st.columns([1.4, 1.4, 1.2])
    afx, afr, afs = build_plots(arch['df'], arch['flat'])
    p1.plotly_chart(afx, use_container_width=True, config={'staticPlot': True})
    p2.plotly_chart(afr, use_container_width=True, config={'staticPlot': True})
    p3.plotly_chart(afs, use_container_width=True, config={'staticPlot': True})
    st.markdown("</div>", unsafe_allow_html=True)
