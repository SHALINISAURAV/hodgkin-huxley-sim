import streamlit as st

def apply_custom_theme():
    st.markdown("""
        <style>
        /* Main page background & text styling */
        .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
        }
        
        /* Metric cards custom styling */
        div[data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            font-weight: 700;
            color: #58a6ff;
        }
        
        /* Custom section card styling */
        .bio-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .bio-title {
            color: #79c0ff;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 8px;
        }
        </style>
    """, unsafe_allow_html=True)