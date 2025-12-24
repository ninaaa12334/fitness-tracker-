import streamlit as st
import requests

def login_page(api_url):
    # --- CONNECTION OVERRIDE ---
    # Ensuring Streamlit points exactly where the FastAPI 'Online' message is
    target_url = "http://127.0.0.1:8000" 

    # --- UI Header ---
    st.markdown("<h2 style='text-align: center;'>Welcome to FitTracker Pro</h2>", unsafe_allow_html=True)
    
    # Check connection status immediately
    try:
        requests.get(target_url, timeout=1)
        st.sidebar.success("📡 System Online")
    except:
        st.sidebar.error("📡 System Offline - Check Terminal 1")

    login_tab, signup_tab = st.tabs(["🔒 Secure Login", "🚀 Create Account"])

    # --- Login Tab ---
    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            submit_button = st.form_submit_button("UNLEASH PERFORMANCE")

            if submit_button:
                try:
                    # Added trailing slash for route compatibility
                    response = requests.post(
                        f"{target_url}/users/login/", 
                        json={"username": username, "password": password},
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.logged_in = True
                        st.session_state.user_id = data['user_id']
                        st.session_state.username = data['username']
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

    # --- Sign Up Tab ---
    with signup_tab:
        with st.form("signup_form"):
            st.markdown("### Profile Details")
            col1, col2 = st.columns(2)
            with col1:
                new_username = st.text_input("Username*")
                new_password = st.text_input("Password*", type="password")
                age = st.number_input("Age", min_value=12, value=25)
            with col2:
                height = st.number_input("Height (cm)", value=175.0)
                weight = st.number_input("Weight (kg)", value=70.0)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])

            goal = st.selectbox("Your Primary Goal", ["lose weight", "gain muscle", "maintain"])
            signup_button = st.form_submit_button("START YOUR JOURNEY")
            
            if signup_button:
                # Packaging data carefully
                user_data = {
                    "username": new_username, 
                    "password": new_password, 
                    "age": int(age), 
                    "height": float(height), 
                    "weight": float(weight), 
                    "gender": gender, 
                    "goal": goal.lower()
                }
                
                try:
                    # POST request with trailing slash and explicit headers
                    response = requests.post(
                        f"{target_url}/users/signup/", 
                        json=user_data,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 201:
                        st.balloons()
                        st.success("🎯 Journey Activated! Switch to the Login tab.")
                        
                        # Show the plan summary immediately
                        days = {"lose weight": 5, "gain muscle": 4, "maintain": 3}.get(goal.lower(), 3)
                        st.info(f"Your custom plan is set for {days} days per week.")
                        
                    elif response.status_code == 400:
                        st.error(f"Account error: {response.json().get('detail')}")
                    else:
                        # Fallback if response isn't JSON
                        st.error(f"Server sent an unexpected response (Status: {response.status_code})")
                        
                except Exception as e:
                    st.error(f"Backend unreachable. Debug: {e}")