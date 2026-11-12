
import streamlit as st
import pandas as pd

st.set_page_config(page_title="COCOMO Estimation Tool", page_icon="📊", layout="wide")

# COCOMO 81 coefficients
MODES = {
    "Organic": {"basic": (2.4, 1.05, 2.5, 0.38), "intermediate": (3.2, 1.05, 2.5, 0.38)},
    "Semi-detached": {"basic": (3.0, 1.12, 2.5, 0.35), "intermediate": (3.0, 1.12, 2.5, 0.35)},
    "Embedded": {"basic": (3.6, 1.20, 2.5, 0.32), "intermediate": (2.8, 1.20, 2.5, 0.32)}
}

# COCOMO 81 effort multipliers, ordered: Very Low, Low, Nominal, High, Very High, Extra High
DRIVERS = {
    "RELY - Required software reliability": [0.75, 0.88, 1.00, 1.15, 1.40, None],
    "DATA - Database size": [None, 0.94, 1.00, 1.08, 1.16, None],
    "CPLX - Product complexity": [0.70, 0.85, 1.00, 1.15, 1.30, 1.65],
    "TIME - Execution time constraint": [None, None, 1.00, 1.11, 1.30, 1.66],
    "STOR - Main storage constraint": [None, None, 1.00, 1.06, 1.21, 1.56],
    "VIRT - Virtual machine volatility": [None, 0.87, 1.00, 1.15, 1.30, None],
    "TURN - Computer turnaround time": [None, 0.87, 1.00, 1.07, 1.15, None],
    "ACAP - Analyst capability": [1.46, 1.19, 1.00, 0.86, 0.71, None],
    "AEXP - Applications experience": [1.29, 1.13, 1.00, 0.91, 0.82, None],
    "PCAP - Programmer capability": [1.42, 1.17, 1.00, 0.86, 0.70, None],
    "VEXP - Virtual machine experience": [1.21, 1.10, 1.00, 0.90, None, None],
    "LEXP - Language experience": [1.14, 1.07, 1.00, 0.95, None, None],
    "MODP - Modern programming practices": [1.24, 1.10, 1.00, 0.91, 0.82, None],
    "TOOL - Use of software tools": [1.24, 1.10, 1.00, 0.91, 0.83, None],
    "SCED - Required development schedule": [1.23, 1.08, 1.00, 1.04, 1.10, None],
}
RATINGS = ["Very Low", "Low", "Nominal", "High", "Very High", "Extra High"]
DEFAULT_PHASES = {
    "Planning & requirements": 6, "Product design": 16, "Detailed design": 24,
    "Code & unit testing": 38, "Integration & testing": 16
}

def calculate(loc, mode, model, eaf=1.0):
    kloc = loc / 1000.0
    if model == "Basic":
        a, b, c, d = MODES[mode]["basic"]
        effort = a * (kloc ** b)
    else:
        a, b, c, d = MODES[mode]["intermediate"]
        effort = a * (kloc ** b) * eaf
    time_months = c * (effort ** d)
    team = effort / time_months if time_months else 0
    productivity = loc / effort if effort else 0
    return {"KLOC": kloc, "Effort": effort, "Time": time_months,
            "Team": team, "Productivity": productivity, "EAF": eaf}

st.title("📊 COCOMO Estimation Tool")
st.caption("COCOMO 81 • Basic, Intermediate and Detailed estimation")
st.info("Enter project size in Lines of Code (LoC). Intermediate and Detailed models use the Effort Adjustment Factor (EAF), calculated from 15 cost drivers.")

with st.sidebar:
    st.header("Project inputs")
    project = st.text_input("Project name", "Online Food Ordering System")
    loc = st.number_input("Lines of Code (LoC)", min_value=100, max_value=1000000, value=30000, step=100)
    mode = st.selectbox("Project mode", list(MODES.keys()), index=1)
    st.divider()
    st.caption("COCOMO 81 project modes: Organic, Semi-detached and Embedded.")

tab1, tab2, tab3, tab4 = st.tabs(["Basic COCOMO", "Intermediate COCOMO", "Detailed COCOMO", "Test cases"])

with tab1:
    st.subheader("Basic COCOMO")
    st.write("Uses project size (KLOC) and project mode.")
    r = calculate(loc, mode, "Basic")
    st.metric("Estimated effort", f"{r['Effort']:.2f} Person-Months")
    c1,c2,c3 = st.columns(3)
    c1.metric("Development time", f"{r['Time']:.2f} Months")
    c2.metric("Average team size", f"{r['Team']:.2f} Persons")
    c3.metric("Productivity", f"{r['Productivity']:.2f} LOC/PM")
    st.caption(f"KLOC = {r['KLOC']:.2f} | Mode = {mode}")

with tab2:
    st.subheader("Intermediate COCOMO")
    st.write("Select a rating for each cost driver. The product of all selected multipliers is EAF.")
    selected = {}
    cols = st.columns(3)
    for i, (driver, values) in enumerate(DRIVERS.items()):
        valid = [(rating, value) for rating, value in zip(RATINGS, values) if value is not None]
        with cols[i % 3]:
            choice = st.selectbox(driver, [x[0] for x in valid], index=[x[0] for x in valid].index("Nominal") if "Nominal" in [x[0] for x in valid] else 0, key="int_"+driver)
            selected[driver] = dict(valid)[choice]
    eaf = 1.0
    for value in selected.values():
        eaf *= value
    r = calculate(loc, mode, "Intermediate", eaf)
    st.metric("Effort Adjustment Factor (EAF)", f"{eaf:.4f}")
    st.metric("Estimated effort", f"{r['Effort']:.2f} Person-Months")
    c1,c2,c3 = st.columns(3)
    c1.metric("Development time", f"{r['Time']:.2f} Months")
    c2.metric("Average team size", f"{r['Team']:.2f} Persons")
    c3.metric("Productivity", f"{r['Productivity']:.2f} LOC/PM")
    st.caption("Cost-driver ratings and multipliers follow the COCOMO 81 Intermediate model. EAF is the product of the 15 multipliers.")

with tab3:
    st.subheader("Detailed COCOMO")
    st.write("Detailed COCOMO applies cost-driver-adjusted effort and distributes total effort across development phases.")
    selected_d = {}
    cols = st.columns(3)
    for i, (driver, values) in enumerate(DRIVERS.items()):
        valid = [(rating, value) for rating, value in zip(RATINGS, values) if value is not None]
        with cols[i % 3]:
            choice = st.selectbox(driver, [x[0] for x in valid], index=[x[0] for x in valid].index("Nominal") if "Nominal" in [x[0] for x in valid] else 0, key="det_"+driver)
            selected_d[driver] = dict(valid)[choice]
    eaf_d = 1.0
    for value in selected_d.values():
        eaf_d *= value
    r = calculate(loc, mode, "Detailed", eaf_d)
    st.metric("EAF", f"{eaf_d:.4f}")
    st.metric("Total estimated effort", f"{r['Effort']:.2f} Person-Months")
    st.caption("Set phase percentages below. The default split is an illustrative planning allocation; replace it with the phase distribution supplied by your course reference if specified.")
    phase_values = {}
    cols = st.columns(2)
    for i, (phase, default) in enumerate(DEFAULT_PHASES.items()):
        with cols[i % 2]:
            phase_values[phase] = st.number_input(phase+" (%)", min_value=0, max_value=100, value=default, step=1, key="phase_"+phase)
    total_pct = sum(phase_values.values())
    if total_pct != 100:
        st.warning(f"Phase percentages currently total {total_pct}%. Adjust them to exactly 100%.")
    else:
        df = pd.DataFrame([{"Development phase": k, "Allocation (%)": v, "Effort (Person-Months)": r["Effort"]*v/100} for k,v in phase_values.items()])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.metric("Development time", f"{r['Time']:.2f} Months")
        st.metric("Average team size", f"{r['Team']:.2f} Persons")

with tab4:
    st.subheader("Sample test cases")
    cases = [
        {"Project":"Library Management System","LoC":2000,"Mode":"Organic"},
        {"Project":"Online Food Ordering System","LoC":30000,"Mode":"Semi-detached"},
        {"Project":"Banking System","LoC":100000,"Mode":"Embedded"},
    ]
    rows=[]
    for case in cases:
        for model in ["Basic","Intermediate","Detailed"]:
            res=calculate(case["LoC"],case["Mode"],model,1.0)
            rows.append({"Project":case["Project"],"LoC":case["LoC"],"Mode":case["Mode"],"Model":model,
                         "Effort (PM)":round(res["Effort"],2),"Time (Months)":round(res["Time"],2),
                         "Team size":round(res["Team"],2),"Productivity (LOC/PM)":round(res["Productivity"],2)})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.caption("For this comparison table, EAF = 1.00 (all cost drivers set to Nominal).")
st.divider()
st.caption("Academic demonstration tool based on the original COCOMO 81 model. Estimates are model-based approximations, not guaranteed project commitments.")
