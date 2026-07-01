import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
import os
from datetime import datetime, timedelta

# --- ARCHITECTURAL VISUAL MASTER MATRIX (PREMIUM INDUSTRIAL SPEC) ---
st.set_page_config(page_title="Horizon Addis Tyre - SPC Center", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght=400;700&family=Share+Tech+Mono&display=swap');
    
    /* GLOBAL LAYOUT & HIGH-CONTRAST EDGING SPECIFICATIONS */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0A0A0C !important;
        font-family: 'Share Tech Mono', monospace !important;
        color: #00FF66 !important;
    }
    
    /* SHARP DUAL RED/WHITE OUTER BORDER MATRIX FRAMEWORK */
    [data-testid="stAppViewContainer"] > section {
        border-left: 5px solid #FF3333 !important;
        border-right: 5px solid #FF3333 !important;
        box-shadow: inset 4px 0 0 0 #FFFFFF, inset -4px 0 0 0 #FFFFFF, 0 0 20px rgba(255, 51, 51, 0.3);
    }
    
    [data-testid="stHeader"] {
        border-bottom: 3px dashed #FFFFFF !important;
        background-color: #0A0A0C !important;
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
    
    .stSelectbox div[data-baseweb="select"], .stNumberInput input, .stTextInput input, .stDateInput input, .stTimeInput input {
        background-color: #1A221E !important;
        color: #00FF66 !important;
        border: 1px solid #00FF66 !important;
    }

    /* SPECIFICATION PLATES: Read-only high visibility styles */
    .spec-plate-box {
        background: #141916 !important;
        border: 2px solid #00FF66 !important;
        border-radius: 4px;
        padding: 10px;
        text-align: center;
    }
    .spec-plate-label {
        font-size: 11px !important;
        color: #FFFFFF !important;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .spec-plate-value {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 20px !important;
        color: #FFBB00 !important;
        font-weight: bold !important;
        text-shadow: 0 0 10px rgba(255, 187, 0, 0.3);
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
        border: 2px dashed #00FF66 !important;
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

# --- DIRECTORY ISOLATION GUARDRAIL ---
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# --- AUTHORIZATION GATEWAY PROPERTIES ---
MANAGER_PASSTOKEN = "ADDIS_QA_2026"
REGISTRY_FILE = os.path.join(DATA_DIR, "profile_registry_config.csv")

MASTER_FACTORY_BASICS = {
    "750-16 HT-99 Treadweight": {"target": 11.1600, "usl": 11.4948, "lsl": 10.8252, "seed_mean": 11.1600, "seed_sigma": 0.0395},
    "400-8 HT-60 Treadweight": {"target": 2.0200, "usl": 2.0806, "lsl": 1.9594, "seed_mean": 2.0200, "seed_sigma": 0.0216},
    "195 R15 Treadweight": {"target": 5.5000, "usl": 5.6650, "lsl": 5.3350, "seed_mean": 5.5000, "seed_sigma": 0.0310},
    "205 Treadweight": {"target": 6.8000, "usl": 7.0040, "lsl": 6.5960, "seed_mean": 6.8000, "seed_sigma": 0.0400},
    "700-16 HT-40 Treadweight": {"target": 9.8000, "usl": 10.0940, "lsl": 9.5060, "seed_mean": 9.8000, "seed_sigma": 0.0500},
    "Rubberizing KIP Coating Gauge": {"target": 1.2000, "usl": 1.2600, "lsl": 1.1400, "seed_mean": 1.2000, "seed_sigma": 0.0100},
    "LTR Coating Gauge": {"target": 1.5000, "usl": 1.5750, "lsl": 1.4250, "seed_mean": 1.5000, "seed_sigma": 0.0120},
    "Size 3 Model Profile": {"target": 5.0000, "usl": 5.1500, "lsl": 4.8500, "seed_mean": 5.0000, "seed_sigma": 0.0300}
}

def save_profile_registry(registry_dict):
    rows = []
    for name, data in registry_dict.items():
        rows.append({
            'profile_name': name, 'target': data['target'], 'usl': data['usl'], 'lsl': data['lsl'], 'seed_mean': data['seed_mean'], 'seed_sigma': data['seed_sigma']
        })
    pd.DataFrame(rows).to_csv(REGISTRY_FILE, index=False)

def load_profile_registry():
    current_registry = {}
    if os.path.exists(REGISTRY_FILE):
        try:
            df_reg = pd.read_csv(REGISTRY_FILE)
            for _, row in df_reg.iterrows():
                p_name = str(row['profile_name'])
                current_registry[p_name] = {
                    "target": float(row['target']), "usl": float(row['usl']), "lsl": float(row['lsl']), "seed_mean": float(row['seed_mean']), "seed_sigma": float(row['seed_sigma'])
                }
        except Exception:
            pass
    updated = False
    for master_key, master_val in MASTER_FACTORY_BASICS.items():
        if master_key not in current_registry:
            current_registry[master_key] = master_val
            updated = True
    if updated or not os.path.exists(REGISTRY_FILE):
        save_profile_registry(current_registry)
    return current_registry

st.session_state["COMPONENT_REGISTRY"] = load_profile_registry()
options_list = list(st.session_state["COMPONENT_REGISTRY"].keys())

if "active_profile_name" not in st.session_state or st.session_state["active_profile_name"] not in options_list:
    st.session_state["active_profile_name"] = options_list[0]

if "previous_unique_datakey" not in st.session_state:
    st.session_state["previous_unique_datakey"] = ""

# --- ACTIVE COMPONENT SELECTION & SHIFT MATRIX METADATA BAR ---
st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:2px;'>⚙️ 1. COMPONENT SELECTION & ACTIVE LINE SHIFT TRACKING REGISTRY</p>", unsafe_allow_html=True)
row_sel1, row_sel2, row_sel3, row_sel4 = st.columns([2, 1, 1, 1])

with row_sel1:
    try:
        current_idx = options_list.index(st.session_state["active_profile_name"])
    except ValueError:
        current_idx = 0
        st.session_state["active_profile_name"] = options_list[0]
    component_size = st.selectbox("📂 Active Profile Target Size Blueprint", options=options_list, index=current_idx)
    st.session_state["active_profile_name"] = component_size

with row_sel2:
    active_date = st.date_input("Production Operation Date", value=datetime.now().date())

with row_sel3:
    active_shift = st.selectbox("Active Operational Shift Rotation", ["Shift A (Morning)", "Shift B (Afternoon)", "Shift C (Night)"])

with row_sel4:
    tolerance_pct = st.number_input("Given Tolerance (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.1, format="%.1f")

clean_size_str = component_size.replace(' ', '_').replace('-', '_').replace('.', '_').replace('/', '_')
clean_shift_str = active_shift.split(' ')[1].lower()  
unique_data_key = f"{clean_size_str}_{active_date}_{clean_shift_str}"
CSV_FILE_PATH = os.path.join(DATA_DIR, f"spc_datastore_{unique_data_key}.csv")

state_key = f"dataset_{unique_data_key}"
archive_key = f"archive_{unique_data_key}"

def generate_fresh_baseline():
    return pd.DataFrame(columns=['Sample', 'Timestamp', 'Supervisor', 'Shift', 'X1', 'X2', 'X3', 'X4', 'X5'])

if st.session_state["previous_unique_datakey"] != unique_data_key:
    st.session_state["previous_unique_datakey"] = unique_data_key
    st.session_state.pop(state_key, None)

if state_key not in st.session_state:
    if os.path.exists(CSV_FILE_PATH):
        try: df_active = pd.read_csv(CSV_FILE_PATH)
        except Exception: df_active = generate_fresh_baseline()
    else:
        df_active = generate_fresh_baseline()
        df_active.to_csv(CSV_FILE_PATH, index=False)
    st.session_state[state_key] = df_active

current_config = st.session_state["COMPONENT_REGISTRY"][component_size]

# --- AUTHORIZED SPECIFICATION MODIFICATION & CORRECTION MODULE ---
with st.expander("🔐 Manager Authorization Center: Modify Specifications & Correct Faulty Shift Entries"):
    st.markdown("<div class='management-card' style='border: 1px solid #FFBB00;'>", unsafe_allow_html=True)
    st.markdown("⚠️ *Supervisors do not have authorization keys. Master key verification required for amendments.*")
    
    auth_key_input = st.text_input("🔑 Enter Master Management Authorization Passcode", type="password")
    
    if auth_key_input == MANAGER_PASSTOKEN:
        st.success("🔓 Authorization verified successfully. Management tools unlocked.")
        st.markdown("---")
        st.markdown("🛠️ **2. BACK-DATABLE ENTRY CORRECTION ENGINE**")
        
        c_col1, c_col2, c_col3 = st.columns(3)
        with c_col1: edit_target_profile = st.selectbox("Select Profile To Correct", options=options_list, key="corr_prof")
        with c_col2: edit_target_date = st.date_input("Select Mistaken Entry Date", value=active_date, key="corr_date")
        with c_col3: edit_target_shift = st.selectbox("Select Shift Rotation", ["Shift A (Morning)", "Shift B (Afternoon)", "Shift C (Night)"], key="corr_shift")
        
        c_size_str = edit_target_profile.replace(' ', '_').replace('-', '_').replace('.', '_').replace('/', '_')
        c_shift_str = edit_target_shift.split(' ')[1].lower()
        target_corr_file = os.path.join(DATA_DIR, f"spc_datastore_{c_size_str}_{edit_target_date}_{c_shift_str}.csv")
        
        if os.path.exists(target_corr_file):
            try:
                df_corr = pd.read_csv(target_corr_file)
                st.write(f"📂 Active Loaded Dataset: `{os.path.basename(target_corr_file)}` ({len(df_corr)} subgroups loaded)")
                
                with st.form(key="row_correction_form"):
                    subgroup_to_fix = st.number_input("Enter Subgroup ID to modify", min_value=1, max_value=int(max(len(df_corr), 1)), step=1)
                    matching_rows = df_corr[df_corr['Sample'] == subgroup_to_fix]
                    old_x = [float(current_config["target"])] * 5
                    if not matching_rows.empty:
                        old_x = [matching_rows.iloc[0][f'X{i}'] for i in range(1, 6)]
                    
                    cx1 = st.number_input("Corrected X1", value=old_x[0], format="%.4f")
                    cx2 = st.number_input("Corrected X2", value=old_x[1], format="%.4f")
                    cx3 = st.number_input("Corrected X3", value=old_x[2], format="%.4f")
                    cx4 = st.number_input("Corrected X4", value=old_x[3], format="%.4f")
                    cx5 = st.number_input("Corrected X5", value=old_x[4], format="%.4f")
                    
                    if st.form_submit_button("💾 REWRITE & COMMIT CORRECTION TO CSV"):
                        df_corr.loc[df_corr['Sample'] == subgroup_to_fix, ['X1', 'X2', 'X3', 'X4', 'X5']] = [cx1, cx2, cx3, cx4, cx5]
                        df_corr.to_csv(target_corr_file, index=False)
                        st.session_state.pop(f"dataset_{c_size_str}_{edit_target_date}_{c_shift_str}", None)
                        st.success("✓ Subgroup updated successfully!")
                        st.rerun()
            except Exception as e: st.error(f"Error executing sheet adjustment: {str(e)}")
        else: st.warning("No datastore log file exists matching selection.")
        
        st.markdown("---")
        with st.form(key=f"authorized_edit_form_{clean_size_str}"):
            edit_name = st.text_input("Modify Profile Display Identifier Name", value=component_size)
            ec1, ec2, ec3 = st.columns(3)
            with ec1: edit_target = ec1.number_input("Modify Target Weight Center", value=float(current_config["target"]), format="%.4f")
            with ec2: edit_usl = ec2.number_input("Modify Upper Spec Limit (USL)", value=float(current_config["usl"]), format="%.4f")
            with ec3: edit_lsl = ec3.number_input("Modify Lower Spec Limit (LSL)", value=float(current_config["lsl"]), format="%.4f")
            
            if st.form_submit_button("⚡ COMMIT TARGET CHANGES & SAVE CONFIG"):
                temp_registry = load_profile_registry()
                temp_registry.pop(component_size, None)
                temp_registry[edit_name.strip()] = {"target": edit_target, "usl": edit_usl, "lsl": edit_lsl, 'seed_mean': edit_target, 'seed_sigma': max((edit_usl - edit_lsl) / 10.0, 0.001)}
                save_profile_registry(temp_registry)
                st.session_state["COMPONENT_REGISTRY"] = temp_registry
                st.session_state["active_profile_name"] = edit_name.strip()
                st.success("✓ Profile blueprint committed.")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- LOOKAHEAD ENGINE: CASCADING NEXT-DAY BORROWING PROTOCOL ---
def compile_lookahead_dataset(base_df, start_date, profile_str, shift_str):
    combined_df = base_df.copy()
    borrowed_logs = []
    
    # 20 Subgroups * 5 measurements per Subgroup = 100 Total Samples
    if len(combined_df) >= 20:
        return combined_df, borrowed_logs

    current_scan_date = start_date
    max_lookahead_days = 15  # Limit check depth to prevent endless disk searching
    
    for _ in range(max_lookahead_days):
        current_scan_date += timedelta(days=1)
        scan_key = f"{profile_str}_{current_scan_date}_{shift_str}"
        scan_file = os.path.join(DATA_DIR, f"spc_datastore_{scan_key}.csv")
        
        if os.path.exists(scan_file):
            try:
                next_df = pd.read_csv(scan_file)
                if not next_df.empty:
                    needed_subgroups = 20 - len(combined_df)
                    available_subgroups = len(next_df)
                    
                    take_count = min(needed_subgroups, available_subgroups)
                    if take_count > 0:
                        rows_to_borrow = next_df.head(take_count).copy()
                        borrowed_logs.append({
                            'date': current_scan_date.strftime('%Y-%m-%d'),
                            'subgroups': take_count
                        })
                        combined_df = pd.concat([combined_df, rows_to_borrow], ignore_index=True)
                        
                        if len(combined_df) >= 20:
                            break
            except Exception: pass
            
    # Normalize index sequencing for the calculation arrays
    if not combined_df.empty:
        combined_df['Sample'] = range(1, len(combined_df) + 1)
    return combined_df, borrowed_logs

# Generate aggregated dynamic dataset 
df_raw = st.session_state[state_key].copy()
df, lookahead_history = compile_lookahead_dataset(df_raw, active_date, clean_size_str, clean_shift_str)
current_subgroups = len(df_raw)
total_subgroups_calculated = len(df)

config = st.session_state["COMPONENT_REGISTRY"][component_size]
usl, target, lsl = config["usl"], config["target"], config["lsl"]
d2, A2, D4 = 2.3330, 0.5770, 2.1150
absolute_min_allowed, absolute_max_allowed = lsl * 0.96, usl * 1.04

if not df.empty:
    df['Mean'] = df[['X1', 'X2', 'X3', 'X4', 'X5']].mean(axis=1)
    df['Range'] = df[['X1', 'X2', 'X3', 'X4', 'X5']].max(axis=1) - df[['X1', 'X2', 'X3', 'X4', 'X5']].min(axis=1)
    flattened = df[['X1', 'X2', 'X3', 'X4', 'X5']].values.flatten()
    total_obs = len(flattened)
    grand_mean = df['Mean'].mean()
    average_range = df['Range'].mean()
    span_obs = float(flattened.max() - flattened.min())
    grand_median = float(np.median(flattened))
    variance_obs = float(np.var(flattened))
    std_dev = average_range / d2 if average_range > 0 else 0.001
    overall_std = float(np.std(flattened, ddof=1)) if len(flattened) > 1 else 0.001
    ucl_x, lcl_x = grand_mean + (A2 * average_range), grand_mean - (A2 * average_range)
    ucl_r, lcl_r = D4 * average_range, 0.0
    gen_movement = float(np.std(df['Mean'].diff().dropna())) if len(df) > 1 else 0.0
else:
    total_obs = 0; grand_mean = target; average_range = 0.0; span_obs = 0.0; grand_median = target
    variance_obs = 0.0; std_dev = 0.001; overall_std = 0.001; ucl_x = target; lcl_x = target; ucl_r = 0.0; gen_movement = 0.0
    flattened = np.array([target])

# --- PROCESS SPECIFICATION STANDARDS EXPOSED VIA ULTRA-BRIGHT READ-ONLY CUSTOM HTML PLATES ---
st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:2px;'>🛠️ 2. PROCESS SPECIFICATION STANDARDS & TARGET BOUNDARIES [SECURED READ-ONLY]</p>", unsafe_allow_html=True)
sc1, sc2, sc3, sc4, sc5, sc6 = st.columns(6)
sc1.markdown(f'<div class="spec-plate-box"><div class="spec-plate-label">USL (Upper Spec)</div><div class="spec-plate-value">{usl:.4f}</div></div>', unsafe_allow_html=True)
sc2.markdown(f'<div class="spec-plate-box"><div class="spec-plate-label">Target Center</div><div class="spec-plate-value">{target:.4f}</div></div>', unsafe_allow_html=True)
sc3.markdown(f'<div class="spec-plate-box"><div class="spec-plate-label">LSL (Lower Spec)</div><div class="spec-plate-value">{lsl:.4f}</div></div>', unsafe_allow_html=True)
sc4.markdown(f'<div class="spec-plate-box"><div class="spec-plate-label">Shewhart d2</div><div class="spec-plate-value">{d2:.4f}</div></div>', unsafe_allow_html=True)
sc5.markdown(f'<div class="spec-plate-box"><div class="spec-plate-label">Shewhart A2</div><div class="spec-plate-value">{A2:.4f}</div></div>', unsafe_allow_html=True)
sc6.markdown(f'<div class="spec-plate-box"><div class="spec-plate-label">Shewhart D4</div><div class="spec-plate-value">{D4:.4f}</div></div>', unsafe_allow_html=True)

# --- GRAPHING SUB-ENGINE WITH GLOWING DIODE YELLOW TITLES ---
def build_plots(data_frame, flat_array):
    diode_yellow_title = dict(color='#FFBB00', family='Orbitron, Share Tech Mono, monospace', size=15)
    x_min, x_max = (data_frame['Sample'].min(), data_frame['Sample'].max()) if not data_frame.empty else (1, 20)

    fig_x = go.Figure()
    if not data_frame.empty:
        fig_x.add_trace(go.Scatter(x=data_frame['Sample'], y=data_frame['Mean'], mode='lines+markers', name='Mean', line=dict(color='#00FF66', width=2)))
    fig_x.add_shape(type="line", x0=x_min, y0=grand_mean, x1=x_max, y1=grand_mean, line=dict(color="white", width=1.5))
    fig_x.add_shape(type="line", x0=x_min, y0=ucl_x, x1=x_max, y1=ucl_x, line=dict(color="red", dash="dash", width=1.5))
    fig_x.add_shape(type="line", x0=x_min, y0=lcl_x, x1=x_max, y1=lcl_x, line=dict(color="red", dash="dash", width=1.5))
    fig_x.update_layout(title=dict(text="<b>⚡ 1=> X-BAR PROCESS CONTROL CHART</b>", font=diode_yellow_title, x=0.02), paper_bgcolor='#0A0A0C', plot_bgcolor='#0F1214', font_color="#00FF66", height=230, margin=dict(l=10, r=10, t=55, b=10))
    
    fig_r = go.Figure()
    if not data_frame.empty: fig_r.add_trace(go.Scatter(x=data_frame['Sample'], y=data_frame['Range'], mode='lines+markers', name='Range', line=dict(color='#00FFFF', width=2)))
    fig_r.add_shape(type="line", x0=x_min, y0=average_range, x1=x_max, y1=average_range, line=dict(color="white", width=1.5))
    fig_r.add_shape(type="line", x0=x_min, y0=ucl_r, x1=x_max, y1=ucl_r, line=dict(color="red", dash="dash", width=1.5))
    fig_r.update_layout(title=dict(text="<b>⚡ 2=> R-BAR RANGE VARIABILITY CHART</b>", font=diode_yellow_title, x=0.02), paper_bgcolor='#0A0A0C', plot_bgcolor='#0F1214', font_color="#00FF66", height=230, margin=dict(l=10, r=10, t=55, b=10))
    
    fig_s = go.Figure()
    fig_s.add_trace(go.Histogram(x=flat_array, histnorm='probability density', marker_color='#1A2620', opacity=0.85, marker_line=dict(width=1, color='#00FF66')))
    xs = np.linspace(min(flat_array.min(), lsl), max(flat_array.max(), usl), 100)
    fig_s.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='#FFBB00', width=2))) if not data_frame.empty else None
    fig_s.add_vline(x=lsl, line_dash="dot", line_color="red", line_width=1.5)
    fig_s.add_vline(x=usl, line_dash="dot", line_color="red", line_width=1.5)
    fig_s.add_vline(x=target, line_color="#00FF66", line_width=1.5)
    fig_s.update_layout(title=dict(text="<b>📊 3=> PROCESS CURVE -VS- SPEC.</b>", font=diode_yellow_title, x=0.02), paper_bgcolor='#0A0A0C', plot_bgcolor='#0F1214', font_color="#00FF66", height=230, margin=dict(l=10, r=10, t=55, b=10), showlegend=False)
    return fig_x, fig_r, fig_s

# --- PANEL 2: LATERAL MATRIX DISPLAY ---
st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:2px;'>📊 LIVE PROCESS SUMMARY PARAMETERS MATRIX (AGGREGATED DATA)</p>", unsafe_allow_html=True)
st.markdown(f"""
<table class="lateral-table">
    <tr>
        <td class="lateral-cell"><div class="cell-label">Target Center</div><div class="cell-value">{target:.4f}</div><div class="cell-desc">Nominal blueprint dimension center weight.</div></td>
        <td class="lateral-cell"><div class="cell-label">USL</div><div class="cell-value">{usl:.4f}</div><div class="cell-desc">Upper Spec Limit max threshold.</div></td>
        <td class="lateral-cell"><div class="cell-label">LSL</div><div class="cell-value">{lsl:.4f}</div><div class="cell-desc">Lower Spec Limit scrap threshold.</div></td>
        <td class="lateral-cell"><div class="cell-label">Range Mean (R̄)</div><div class="cell-value">{average_range:.4f}</div><div class="cell-desc">Average subgroup internal dispersion spread.</div></td>
        <td class="lateral-cell"><div class="cell-label">Total Subgroups</div><div class="cell-value">{total_subgroups_calculated} / 20</div><div class="cell-desc">Subgroups compiled (Retained + Lookahead).</div></td>
    </tr>
</table>
""", unsafe_allow_html=True)

# --- LOOKAHEAD NOTIFICATION ALERT SYSTEMS ---
if lookahead_history:
    st.info(f"🔄 **LOOKAHEAD STATUS ACTIVE:** Found only {current_subgroups} native subgroups. Borrowed remaining subgroups sequentially from: " + 
            ", ".join([f"`{item['date']}` (+{item['subgroups']} groups)" for item in lookahead_history]))

st.markdown("---")
split_col1, split_col2 = st.columns([1.1, 1.9])

with split_col1:
    st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:1px;'>📥 NATIVE DAY SUBGROUP ENTRY</p>", unsafe_allow_html=True)
    if current_subgroups >= 20:
        st.error(f"🛑 MAXIMUM CAP REACHED: Native shift sheet is full with {current_subgroups} Subgroups.")
    else:
        st.markdown(f"<div class='sop-card'><b>📋 STORAGE REGISTER:</b> {active_shift}<br>Retained Native Count: <b>{current_subgroups}/20 Subgroups</b></div>", unsafe_allow_html=True)
        with st.form(key=f"data_entry_form_{unique_data_key}"):
            next_id = current_subgroups + 1
            supervisor_name = st.text_input("Supervisor Signature", value="Supervisor 1")
            v1 = st.number_input("Measurement X1", value=float(target), format="%.4f")
            v2 = st.number_input("Measurement X2", value=float(target), format="%.4f")
            v3 = st.number_input("Measurement X3", value=float(target), format="%.4f")
            v4 = st.number_input("Measurement X4", value=float(target), format="%.4f")
            v5 = st.number_input("Measurement X5", value=float(target), format="%.4f")
            
            if st.form_submit_button(label="⚡ APPEND SUBGROUP TO ENGINE BASE"):
                input_array = np.array([v1, v2, v3, v4, v5])
                if supervisor_name.strip() == "":
                    st.error("❌ Identification blank error.")
                elif np.any(input_array < absolute_min_allowed) or np.any(input_array > absolute_max_allowed):
                    st.error("🛑 METROLOGY BLOCK: Entry rejected! Input outside safety boundary.")
                else:
                    now_timestamp = datetime.now().strftime("%H:%M:%S")
                    new_row = pd.DataFrame([[next_id, now_timestamp, supervisor_name.strip(), active_shift, v1, v2, v3, v4, v5]], 
                                           columns=['Sample', 'Timestamp', 'Supervisor', 'Shift', 'X1', 'X2', 'X3', 'X4', 'X5'])
                    df_updated = pd.concat([df_raw, new_row], ignore_index=True)
                    df_updated.to_csv(CSV_FILE_PATH, index=False)
                    st.session_state[state_key] = df_updated
                    st.rerun()

with split_col2:
    st.markdown(f"<p style='font-size:13px; font-weight:bold; letter-spacing:1px;'>📋 WORKING ANALYSIS SPECIMENS (TOTAL: {total_subgroups_calculated} SUBGROUPS)</p>", unsafe_allow_html=True)
    if not df.empty:
        st.dataframe(df.style.format("{:.4f}", subset=['X1', 'X2', 'X3', 'X4', 'X5']), height=270, use_container_width=True)
    else: st.info("💡 Shift register completely blank.")

st.markdown("---")

# --- PARALLEL PROCESS DIAGNOSTICS CONTROL GRAPHS ---
st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:2px;'>📊 PARALLEL PROCESS DIAGNOSTICS CONTROL GRAPHS (LOCKED VIEWMODE)</p>", unsafe_allow_html=True)
g1, g2, g3 = st.columns([1.4, 1.4, 1.2])
fx, fr, fs = build_plots(df, flattened)
g1.plotly_chart(fx, use_container_width=True, config={'staticPlot': True})
g2.plotly_chart(fr, use_container_width=True, config={'staticPlot': True})
g3.plotly_chart(fs, use_container_width=True, config={'staticPlot': True})

# --- AUTO-TRIGGER COMPILING RE-CALCULATION CAPABILITY PRINT SHIELD ---
if total_subgroups_calculated >= 20:
    st.markdown("<div class='print-frame'>", unsafe_allow_html=True)
    st.markdown("## 🖨️ AUTO-COMPILED SPECIFICATION & CAPABILITY REPORT")
    st.markdown(f"#### PI & QA Division — Compiled Shift Performance Verification Ledger ({component_size})")
    
    cp = (usl - lsl) / (6 * std_dev) if std_dev > 0 else 0
    cpu = (usl - grand_mean) / (3 * std_dev) if std_dev > 0 else 0
    cpl = (grand_mean - lsl) / (3 * std_dev) if std_dev > 0 else 0
    cpk = min(cpu, cpl)
    pp = (usl - lsl) / (6 * overall_std) if overall_std > 0 else 0
    ppu = (usl - grand_mean) / (3 * overall_std) if overall_std > 0 else 0
    ppl = (grand_mean - lsl) / (3 * overall_std) if overall_std > 0 else 0
    ppk = min(ppu, ppl)
    
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.markdown(f'<div class="capability-metric"><p style="color:#8A9A92;font-size:11px;margin:0;">POTENTIAL CAPABILITY (Cp)</p><h3 style="color:#00FF66;margin:5px 0;">{cp:.4f}</h3></div>', unsafe_allow_html=True)
    mc2.markdown(f'<div class="capability-metric"><p style="color:#8A9A92;font-size:11px;margin:0;">MINIMUM PROCESS INDEX (Cpk)</p><h3 style="color:#00FF66;margin:5px 0;">{cpk:.4f}</h3></div>', unsafe_allow_html=True)
    mc3.markdown(f'<div class="capability-metric"><p style="color:#8A9A92;font-size:11px;margin:0;">TOTAL PERFORMANCE (Pp)</p><h3 style="color:#00FF66;margin:5px 0;">{pp:.4f}</h3></div>', unsafe_allow_html=True)
    mc4.markdown(f'<div class="capability-metric"><p style="color:#8A9A92;font-size:11px;margin:0;">PERFORMANCE INDEX (Ppk)</p><h3 style="color:#00FF66;margin:5px 0;">{ppk:.4f}</h3></div>', unsafe_allow_html=True)
    
    if cpk >= 1.33: st.markdown(f"🟢 **Process Status: HIGHLY CAPABLE ($C_{{pk}}$ = {cpk:.4f}).** Stable.")
    elif cpk >= 1.00: st.markdown(f"🟡 **Process Status: MARGINALLY CAPABLE ($C_{{pk}}$ = {cpk:.4f}).** Monitor variance.")
    else: st.markdown(f"🔴 **Process Status: CRITICAL NON-COMPLIANT ($C_{{pk}}$ = {cpk:.4f}).** Action required.")
    st.markdown("</div>", unsafe_allow_html=True)
