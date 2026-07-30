import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.model import HodgkinHuxleyModel
from src.styles import apply_custom_theme

st.set_page_config(
    page_title="Hodgkin-Huxley Simulator",
    page_icon="⚡",
    layout="wide"
)

apply_custom_theme()

# Header Section
st.title("⚡ Hodgkin-Huxley Action Potential Simulator")
st.caption("A mathematical model simulating ionic mechanism of nerve action potentials (Nobel Prize in Physiology, 1963).")

# Sidebar Controls
st.sidebar.header("🛠️ Simulation Parameters")

st.sidebar.subheader("Stimulus Current Injection")
I_inj = st.sidebar.slider("Current Amplitude (µA/cm²)", 0.0, 40.0, 10.0, 0.5)
t_start = st.sidebar.slider("Start Time (ms)", 0.0, 50.0, 10.0, 1.0)
t_stop = st.sidebar.slider("End Time (ms)", t_start, 100.0, 40.0, 1.0)

st.sidebar.subheader("Max Conductances (mS/cm²)")
g_Na = st.sidebar.slider("g_Na (Sodium)", 0.0, 200.0, 120.0, 5.0)
g_K  = st.sidebar.slider("g_K (Potassium)", 0.0, 100.0, 36.0, 2.0)
g_L  = st.sidebar.slider("g_L (Leak)", 0.0, 5.0, 0.3, 0.1)

st.sidebar.subheader("Simulation Config")
t_max = st.sidebar.number_input("Total Duration (ms)", 10.0, 200.0, 60.0, 10.0)

# Run Simulation
model = HodgkinHuxleyModel(g_Na=g_Na, g_K=g_K, g_L=g_L)
res = model.simulate(t_max=t_max, I_inj=I_inj, t_start=t_start, t_stop=t_stop)

# Summary Key Metrics
col1, col2, col3, col4 = st.columns(4)
peak_v = max(res["V"])
min_v = min(res["V"])
num_spikes = sum(1 for i in range(1, len(res["V"])) if res["V"][i-1] < 0 and res["V"][i] >= 0)

col1.metric("Peak Voltage", f"{peak_v:.1f} mV")
col2.metric("Hyperpolarization", f"{min_v:.1f} mV")
col3.metric("Spike Count", f"{num_spikes}")
col4.metric("Injected Current", f"{I_inj} µA/cm²")

st.markdown("---")

# Plotting Interactive Charts with Plotly
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    subplot_titles=(
        "Membrane Potential V(t)",
        "Gating Variables: m (Na+ act), h (Na+ inact), n (K+ act)",
        "Injected Current I_ext(t) & Ionic Currents"
    )
)

# Row 1: Voltage
fig.add_trace(go.Scatter(x=res["t"], y=res["V"], mode="lines", name="V_m (mV)", line=dict(color="#58a6ff", width=2.5)), row=1, col=1)

# Row 2: Gating Variables
fig.add_trace(go.Scatter(x=res["t"], y=res["m"], mode="lines", name="m (Na+ activation)", line=dict(color="#ff7b72")), row=2, col=1)
fig.add_trace(go.Scatter(x=res["t"], y=res["h"], mode="lines", name="h (Na+ inactivation)", line=dict(color="#ffa657")), row=2, col=1)
fig.add_trace(go.Scatter(x=res["t"], y=res["n"], mode="lines", name="n (K+ activation)", line=dict(color="#7ee787")), row=2, col=1)

# Row 3: Currents
fig.add_trace(go.Scatter(x=res["t"], y=res["I_inj"], mode="lines", name="I_inj", line=dict(color="#d2a8ff", dash="dash")), row=3, col=1)
fig.add_trace(go.Scatter(x=res["t"], y=res["I_Na"], mode="lines", name="I_Na", line=dict(color="#ff7b72", width=1.5)), row=3, col=1)
fig.add_trace(go.Scatter(x=res["t"], y=res["I_K"], mode="lines", name="I_K", line=dict(color="#7ee787", width=1.5)), row=3, col=1)

fig.update_layout(
    height=750,
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#161b22",
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.update_xaxes(title_text="Time (ms)", row=3, col=1, gridcolor="#30363d")
fig.update_yaxes(title_text="mV", row=1, col=1, gridcolor="#30363d")
fig.update_yaxes(title_text="Probability", row=2, col=1, gridcolor="#30363d")
fig.update_yaxes(title_text="µA/cm²", row=3, col=1, gridcolor="#30363d")

st.plotly_chart(fig, use_container_width=True)

# Educational Breakdown Section
st.markdown("""
<div class="bio-card">
    <div class="bio-title">🧠 Biological Mechanics</div>
    <ul>
        <li><b>Depolarization:</b> Injected current raises $V_m$ above threshold, causing $m$-gates to open rapidly ($Na^+$ influx).</li>
        <li><b>Repolarization:</b> $h$-gates close ($Na^+$ inactivation) while $n$-gates open ($K^+$ efflux).</li>
        <li><b>Refractory Period:</b> $V_m$ hyperpolarizes below rest level until $n$ and $h$ return to equilibrium.</li>
    </ul>
</div>
""", unsafe_allow_html=True)  # <-- Fixed parameter name