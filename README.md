# ⚡ Hodgkin-Huxley Neuron Simulator

An interactive, web-based computational neuroscience dashboard that simulates the non-linear electrophysiological dynamics of action potential generation in the giant squid axon using the landmark **Hodgkin-Huxley model (1952)**.

[![Live App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?style=for-the-badge&logo=streamlit)](https://hodgkin-huxley-sim-hauhp2ktruigxcq7capkch.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/SHALINISAURAV/hodgkin-huxley-sim)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)

---

## 📌 Overview

This simulator models the membrane potential dynamics of a biological neuron governed by voltage-gated ion channels ($\text{Na}^+$ and $\text{K}^+$), membrane capacitance, and leak currents. It enables real-time exploration of threshold phenomena, refractory periods, and action potential trains under custom current injection profiles.

### 🌟 Key Features
- **4-Variable Non-Linear ODE Engine:** Integrates coupled ordinary differential equations using `SciPy`'s adaptive **Runge-Kutta 45 (RK45)** solver.
- **Dynamic Multi-Axis Visualizations:** Built with `Plotly` to display aligned, real-time subplots for membrane voltage ($V_m$), gating variables ($m, h, n$), and ionic currents ($I_{\text{Na}}, I_{\text{K}}$).
- **Interactive Control Sidebar:** Tweak current injection pulse, channel conductances ($g_{\text{Na}}, g_{\text{K}}, g_{\text{L}}$), and simulation runtimes on the fly.
- **Custom UI Design:** Custom dark-mode styling built with Streamlit and styled CSS.

---

## 🧮 Mathematical Model

The membrane potential ($V$) dynamics follow the fundamental Hodgkin-Huxley equation:

$$C_m \frac{dV}{dt} = I_{\text{ext}} - \bar{g}_{\text{Na}} m^3 h (V - E_{\text{Na}}) - \bar{g}_{\text{K}} n^4 (V - E_{\text{K}}) - g_{\text{L}} (V - E_{\text{L}})$$

Where kinetics for gating variables $x \in \{m, h, n\}$ follow first-order differential equations:

$$\frac{dx}{dt} = \alpha_x(V)(1-x) - \beta_x(V)x$$

- $m$: Sodium ($\text{Na}^+$) channel activation
- $h$: Sodium ($\text{Na}^+$) channel inactivation
- $n$: Potassium ($\text{K}^+$) channel activation

---

## 🏗️ Project Architecture

```text
hodgkin-huxley-sim/
├── src/
│   ├── __init__.py
│   ├── model.py        # ODE definition & RK45 integration solver
│   └── styles.py       # Streamlit CSS custom styling module
├── app.py              # Interactive Streamlit dashboard & Plotly renderer
├── requirements.txt    # Project dependencies
└── README.md           # Documentation

🛠️ Local Installation & Setup
Prerequisites
Python 3.10+
pip package manager
Run Locally
Clone the Repository:
Bash
git clone [https://github.com/SHALINISAURAV/hodgkin-huxley-sim.git](https://github.com/SHALINISAURAV/hodgkin-huxley-sim.git)
cd hodgkin-huxley-sim
Set Up Virtual Environment:
Bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
Install Dependencies:
Bash
pip install -r requirements.txt
Launch the Application:
Bash
streamlit run app.py
🌐 Live Deployment
Access the live interactive application directly in your browser:
🔗 Hodgkin-Huxley Web Simulator

🧪 Tech Stack
Language: Python
UI Framework: Streamlit
Numerical Computation: NumPy, SciPy (solve_ivp)
Data Visualization: Plotly Graph Objects
