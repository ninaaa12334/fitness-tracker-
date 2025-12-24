import streamlit as st
import requests
import auth
import dashboard

# Use the stable IP address
API_URL = "http://127.0.0.1:8000"

def main():
    st.set_page_config(
        page_title="FitTracker Pro",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # --- ADVANCED UI CSS ---
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #ffffff;
        }
        .st-emotion-cache-1r6slb0, .st-emotion-cache-6q9sum {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
        }
        .stButton>button {
            background: linear-gradient(45deg, #FF4B2B 0%, #FF416C 100%);
            color: white !important;
            border: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 75, 43, 0.3);
            width: 100%;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 75, 43, 0.5);
        }
        section[data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.3) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR HEALTH CHECK ---
    st.sidebar.title("🚀 FitTracker Pro")
    try:
        # Pinging the backend to see if it's healthy
        check = requests.get(API_URL, timeout=2)
        if check.status_code == 200:
            st.sidebar.success("📡 System: Online")
        else:
            st.sidebar.warning(f"📡 System: Error {check.status_code}")
    except:
        st.sidebar.error("📡 System: Offline")

    # --- SESSION MANAGEMENT ---
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        # Center the Login/Signup UI
        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            # We pass the API_URL to auth.py
            auth.login_page(API_URL)
    else:
        # Sidebar logout button
        if st.sidebar.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()
            
        dashboard.show_dashboard(API_URL)

if __name__ == "__main__":
    main()