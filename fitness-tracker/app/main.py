import streamlit as st
import requests
from datetime import datetime
import auth
import dashboard

# FastAPI URL (assuming it runs on localhost:8000)
API_URL = "http://localhost:8000"

def init_session_state():
    """Initializes necessary session state variables."""
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None

def main():
    st.set_page_config(
        page_title="💪 FitTracker Pro",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    init_session_state()

    # --- Attractive Header/Branding ---
    st.markdown("""
        <style>
        .stApp {
            background-color: #f0f2f6; /* Light gray background */
        }
        .main-header {
            font-size: 3em;
            color: #FF4B4B; /* Streamlit's primary color for a vibrant look */
            font-weight: bold;
            text-align: center;
            padding-bottom: 10px;
        }
        </style>
        <div class="main-header">🔥 FitTracker Pro</div>
        ---
    """, unsafe_allow_html=True)
    
    # --- Main App Logic ---
    if not st.session_state.logged_in:
        auth.login_page(API_URL)
    else:
        dashboard.show_dashboard(API_URL)

if __name__ == "__main__":
    main()