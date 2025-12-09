import streamlit as st
import requests

def login_page(api_url):
    """Displays the login and sign-up interface."""
    st.sidebar.header("Account Access")
    
    # Use tabs for a clean switch between Login and Signup
    login_tab, signup_tab = st.tabs(["🔑 Login", "📝 Sign Up"])

    # --- Login Tab ---
    with login_tab:
        with st.form("login_form"):
            st.subheader("Welcome Back!")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            submit_button = st.form_submit_button("Log In")

            if submit_button:
                try:
                    response = requests.post(f"{api_url}/users/login", 
                                             json={"username": username, "password": password})
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.logged_in = True
                        st.session_state.user_id = data['user_id']
                        st.session_state.username = data['username']
                        st.success(f"Logged in as {data['username']}!")
                        st.experimental_rerun()
                    else:
                        st.error("Login failed. Check your username and password.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the backend API. Please ensure FastAPI is running.")

    # --- Sign Up Tab (Minimal form for quick start) ---
    with signup_tab:
        with st.form("signup_form"):
            st.subheader("Create a New Account")
            new_username = st.text_input("Choose Username")
            new_password = st.text_input("Choose Password", type="password")
            # Optional profile info
            goal = st.selectbox("Fitness Goal", ["Lose Weight", "Gain Muscle", "Maintain"])
            
            signup_button = st.form_submit_button("Sign Up")
            
            if signup_button:
                user_data = {
                    "username": new_username, 
                    "password": new_password, 
                    "goal": goal
                }
                try:
                    response = requests.post(f"{api_url}/users/signup", json=user_data)
                    
                    if response.status_code == 201:
                        st.success("Account created successfully! Please log in.")
                    else:
                        st.error(f"Sign up failed: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the backend API.")