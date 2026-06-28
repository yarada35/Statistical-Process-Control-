import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as bg

# --- DASHBOARD CONFIGURATION & MATTE BLACK DESIGN ---
st.set_page_config(page_title="Horizon Addis Tyre - SPC Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #121212; color: #FFFFFF; }
    div[data-testid="stSidebar"] { background-color: #1E1E1E; }
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #333333; color: white; border: 1px solid #555555; }
    .stTabs [data-baseweb="tab"] { color: #888888; }
    .stTabs [data-baseweb="tab"]:hover { color: #FFD700; }
    .stTabs [aria-selected="true"] { color: #FF4B4B !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🏭 HORIZON ADDIS TYRE S.C.")
st.subheader("Statistical Process Control (SPC) Interactive Dashboard")

# --- CONTROL CHARTS CONSTANTS ---
SHEWHART_CONSTANTS = {
    5: {"A2": 0.580, "D3": 0.0, "D4": 2.115}
}

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("⚙️ Data Control Deck")
process_area = st.sidebar.selectbox(
    "Select Component Section", 
    ["Preparation (Tread/Sidewall Variables)", "Assembly Building Section (Variables)", "Tire Curing Section (Attributes)"]
)

# Active Component Setup
if process_area != "Tire Curing Section (Attributes)":
    component_type = st.sidebar.selectbox("Active Component Model", ["750-16 HT-99 Treadweight", "400-8 HT-60 Treadweight"])
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Process Specifications Setup")
    if "750-16" in component_type:
        usl = st.sidebar.number_input("Upper Specification Limit (USL)", value=11.4948)
        target = st.sidebar.number_input("Standard Target (Center)", value=11.16)
        lsl = st.sidebar.number_input("Lower Specification Limit (LSL)", value=10.8252)
    else:
        usl = st.sidebar.number_input("Upper Specification Limit (USL)", value=2.0806)
        target = st.sidebar.number_input("Standard Target (Center)", value=2.02)
        lsl = st.sidebar.number_input("Lower Specification Limit (LSL)", value=1.9594)
else:
    attribute_type = st.sidebar.selectbox("Attribute Chart Type", ["P-Chart (Defect Fraction)", "C-Chart (Number of Defects)"])

# --- DATA GENERATION & SEED FEEDING SYSTEM ---
@st.cache_data
def generate_base_data(comp_type):
    np.random.seed(42)
    base_val = 11.0137 if "750-16" in comp_type else 1.9990
    std_dev = 0.0395 if "750-16" in comp_type else 0.0216
    
    samples = []
    for i in range(1, 26):
        measurements = np.random.normal(base_val, std_dev, 5).tolist()
        samples.append({"Sample_No": i, **{f"X{j+1}": measurements[j] for j in range(5)}})
    return pd.DataFrame(samples)

# --- EXECUTION PATHWAY ---
if process_area != "Tire Curing Section (Attributes)":
    df = generate_base_data(component_type)
    
    # Active Live Data Injector Forms
    with st.expander("📥 Active Component Stream Entry"):
        col1, col2, col3, col4, col5 = st.columns(5)
        v1 = col1.number_input("Point X1", value=float(df.iloc[-1]["X1"]))
        v2 = col2.number_input("Point X2", value=float(df.iloc[-1]["X2"]))
        v3 = col3.number_input("Point X3", value=float(df.iloc[-1]["X3"]))
        v4 = col4.number_input("Point X4", value=float(df.iloc[-1]["X4"]))
        v5 = col5.number_input("Point X5", value=float(df.iloc[-1]["X5"]))
        
        if st.button("Commit Stream Sample to Engine"):
            new_row = {"Sample_No": len(df) + 1, "X1": v1, "X2": v2, "X3": v3, "X4": v4, "X5": v5}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Sample {len(df)} safely committed to live stack.")

    # Mathematical Core Engine
    n = 5
    A2 = SHEWHART_CONSTANTS[n]["A2"]
    D3 = SHEWHART_CONSTANTS[n]["D3"]
    D4 = SHEWHART_CONSTANTS[n]["D4"]

    df['Mean'] = df[['X1', 'X2', 'X3', 'X4', 'X5']].mean(axis=1)
    df['Range'] = df[['X1', 'X2', 'X3', 'X4', 'X5']].max(axis=1) - df[['X1', 'X2', 'X3', 'X4', 'X5']].min(axis=1)

    grand_mean = df['Mean'].mean()
    average_range = df['Range'].mean()

    # Control Limits Calculations
    ucl_x = grand_mean + (A2 * average_range)
    lcl_x = grand_mean - (A2 * average_range)
    ucl_r = D4 * average_range
    lcl_r = D3 * average_range

    # Process Capability Evaluation
    estimated_sigma = average_range / 2.326  # d2 for n=5 is 2.326
    cp = (usl - lsl) / (6 * estimated_sigma)
    cpk = min((usl - grand_mean)/(3 * estimated_sigma), (grand_mean - lsl)/(3 * estimated_sigma))

    # Metric Dashboard Layout
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Grand Mean (X-DoubleBar)", f"{grand_mean:.4f}")
    m2.metric("Average Range (R-Bar)", f"{average_range:.4f}")
    m3.metric("Process Capability Cp", f"{cp:.2f}")
    m4.metric("Process Capability Cpk", f"{cpk:.2f}")

    # --- RANGES ENGINE (PLOTLY VISUALS) ---
    tab1, tab2, tab3 = st.tabs(["📉 X-Bar Process Chart", "📏 R-Bar Range Chart", "📊 Process Specification Graph"])

    with tab1:
        fig_x = bg.Figure()
        fig_x.add_trace(bg.Scatter(x=df['Sample_No'], y=df['Mean'], mode='lines+markers', name='Subgroup Mean', line=dict(color='#FFFF00', width=2)))
        fig_x.add_shape(type="line", x0=df['Sample_No'].min(), y0=grand_mean, x1=df['Sample_No'].max(), y1=grand_mean, line=dict(color="white", width=2))
        fig_x.add_shape(type="line", x0=df['Sample_No'].min(), y0=ucl_x, x1=df['Sample_No'].max(), y1=ucl_x, line=dict(color="#FF0000", dash="dash"))
        fig_x.add_shape(type="line", x0=df['Sample_No'].min(), y0=lcl_x, x1=df['Sample_No'].max(), y1=lcl_x, line=dict(color="#FF0000", dash="dash"))
        
        # Out of control detection (Rule 1: Outside Limits, Rule 2: 7 Points Run)
        df['OOC_X'] = (df['Mean'] > ucl_x) | (df['Mean'] < lcl_x)
        ooc_points_x = df[df['OOC_X']]
        fig_x.add_trace(bg.Scatter(x=ooc_points_x['Sample_No'], y=ooc_points_x['Mean'], mode='markers', marker=dict(color='#FF0000', size=10), name='Out of Control'))
        
        fig_x.update_layout(title="X-Bar Shewhart Chart", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white", xaxis_title="Sample Block Set")
        st.plotly_chart(fig_x, use_container_width=True)

    with tab2:
        fig_r = bg.Figure()
        fig_r.add_trace(bg.Scatter(x=df['Sample_No'], y=df['Range'], mode='lines+markers', name='Subgroup Range', line=dict(color='#00FFFF', width=2)))
        fig_r.add_shape(type="line", x0=df['Sample_No'].min(), y0=average_range, x1=df['Sample_No'].max(), y1=average_range, line=dict(color="white", width=2))
        fig_r.add_shape(type="line", x0=df['Sample_No'].min(), y0=ucl_r, x1=df['Sample_No'].max(), y1=ucl_r, line=dict(color="#FF0000", dash="dash"))
        fig_r.add_shape(type="line", x0=df['Sample_No'].min(), y0=lcl_r, x1=df['Sample_No'].max(), y1=lcl_r, line=dict(color="#FF0000", dash="dash"))
        
        fig_r.update_layout(title="R-Bar Control Chart", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white", xaxis_title="Sample Block Set")
        st.plotly_chart(fig_r, use_container_width=True)

    with tab3:
        # Histogram vs Engineering Specification limits
        fig_spec = bg.Figure()
        all_measurements = df[['X1', 'X2', 'X3', 'X4', 'X5']].values.flatten()
        fig_spec.add_trace(bg.Histogram(x=all_measurements, nbinsx=20, name='Measurements', marker_color='#888888'))
        fig_spec.add_shape(type="line", x0=lsl, y0=0, x1=lsl, y1=15, line=dict(color="#FF0000", width=3, dash="dot"), name="LSL")
        fig_spec.add_shape(type="line", x0=usl, y0=0, x1=usl, y1=15, line=dict(color="#FF0000", width=3, dash="dot"), name="USL")
        fig_spec.add_shape(type="line", x0=target, y0=0, x1=target, y1=15, line=dict(color="#00FF00", width=2), name="Target")
        
        fig_spec.update_layout(title="Process Specification Graph vs. Tolerance Limits", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white")
        st.plotly_chart(fig_spec, use_container_width=True)

else:
    # --- SECTION FOR ATTRIBUTE TRACKING (P/C CHARTS) ---
    st.subheader(f"Curing Production Optimization Section ({attribute_type})")
    
    # Mock data stream for defect parameters
    attr_data = pd.DataFrame({
        "Lot_ID": np.arange(1, 21),
        "Inspected": [100]*20 if "P-Chart" in attribute_type else [1]*20,
        "Defects": [2, 3, 1, 4, 0, 2, 5, 1, 2, 3, 2, 1, 0, 7, 2, 1, 3, 2, 1, 0]
    })
    
    if "P-Chart" in attribute_type:
        attr_data['Fraction'] = attr_data['Defects'] / attr_data['Inspected']
        p_bar = attr_data['Defects'].sum() / attr_data['Inspected'].sum()
        attr_data['UCL'] = p_bar + 3 * np.sqrt((p_bar * (1 - p_bar)) / attr_data['Inspected'])
        attr_data['LCL'] = np.maximum(0, p_bar - 3 * np.sqrt((p_bar * (1 - p_bar)) / attr_data['Inspected']))
        
        fig_attr = bg.Figure()
        fig_attr.add_trace(bg.Scatter(x=attr_data['Lot_ID'], y=attr_data['Fraction'], mode='lines+markers', name='Defect Fraction', line=dict(color='#FF00FF')))
        fig_attr.add_trace(bg.Scatter(x=attr_data['Lot_ID'], y=attr_data['UCL'], mode='lines', line=dict(color='red', dash='dash'), name='UCL'))
        fig_attr.add_trace(bg.Scatter(x=attr_data['Lot_ID'], y=attr_data['LCL'], mode='lines', line=dict(color='red', dash='dash'), name='LCL'))
        fig_attr.update_layout(title="Curing Fraction Defective (P-Chart)", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white")
        st.plotly_chart(fig_attr, use_container_width=True)
        
    else:
        c_bar = attr_data['Defects'].mean()
        ucl_c = c_bar + 3 * np.sqrt(c_bar)
        lcl_c = max(0, c_bar - 3 * np.sqrt(c_bar))
        
        fig_attr = bg.Figure()
        fig_attr.add_trace(bg.Scatter(x=attr_data['Lot_ID'], y=attr_data['Defects'], mode='lines+markers', name='Defect Count', line=dict(color='#FFAA00')))
        fig_attr.add_shape(type="line", x0=1, y0=c_bar, x1=20, y1=c_bar, line=dict(color="white"))
        fig_attr.add_shape(type="line", x0=1, y0=ucl_c, x1=20, y1=ucl_c, line=dict(color="red", dash="dash"))
        fig_attr.add_shape(type="line", x0=1, y0=lcl_c, x1=20, y1=lcl_c, line=dict(color="red", dash="dash"))
        fig_attr.update_layout(title="Curing Defect Count (C-Chart)", paper_bgcolor='#121212', plot_bgcolor='#1E1E1E', font_color="white")
        st.plotly_chart(fig_attr, use_container_width=True)
