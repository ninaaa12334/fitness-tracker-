import streamlit as st
import requests
from datetime import datetime

def show_dashboard(api_url):
    """Displays the main user dashboard with all fitness metrics."""
    st.sidebar.success(f"Logged in as **{st.session_state.username}**")
    
    # Sidebar Navigation
    menu = st.sidebar.radio("Navigation", ["📊 Dashboard", "🏋️ Log Workout", "💧 Log Water", "🎯 Goals"])

    if menu == "📊 Dashboard":
        render_dashboard(api_url)
    elif menu == "🏋️ Log Workout":
        log_workout_form(api_url)
    # Add other views later
    
    if st.sidebar.button("Log Out", help="Click to securely log out."):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.experimental_rerun()

# --- Dashboard Component ---
def render_dashboard(api_url):
    st.title("Welcome to Your Fitness Hub! ⭐")
    
    # 1. Quick Stats (Mock Data for steps/calories - implement actual tracking later)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🚶 Steps Today", "8,500", "500") # Streak is a great idea for motivation!
    with col2:
        st.metric("🔥 Calories Burned", "550 kcal", "50")
    with col3:
        st.metric("💧 Water Intake", "1.5 L", "250 ml")
    with col4:
        st.metric("✅ Workout Streak", "7 Days", "New High!")
    
    st.markdown("---")

    # 2. Workout Progress History (Needs API to fetch data)
    st.subheader("Workout History & Progress")
    
    try:
        response = requests.get(f"{api_url}/workouts/{st.session_state.user_id}")
        if response.status_code == 200:
            workouts = response.json()
            if workouts:
                # Basic display of recent workouts
                st.dataframe(workouts, height=200, use_container_width=True)
            else:
                st.info("No workouts logged yet. Go log your first one!")
        else:
            st.error("Failed to fetch workout history.")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the backend API to fetch data.")

# --- Workout Logging Component ---
def log_workout_form(api_url):
    st.title("🏋️ Log Your Workout")
    st.markdown("Record your exercise details to track your gains!")

    with st.form("workout_log_form"):
        # Basic Workout Details
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", datetime.today())
            exercise_name = st.text_input("Exercise Name (e.g., Squat, Bench Press, Run)")
            duration_minutes = st.number_input("Duration (minutes)", min_value=1.0, step=5.0)
        
        with col2:
            intensity = st.selectbox("Intensity", ["Low", "Medium", "High", "Max Effort"])
            sets = st.number_input("Sets", min_value=1, step=1)
            reps = st.number_input("Reps (per set)", min_value=1, step=1)
            weight = st.number_input("Weight/Resistance (kg)", min_value=0.0, step=2.5)

        submit_button = st.form_submit_button("Record Workout")
        
        if submit_button:
            if not exercise_name or not duration_minutes:
                st.error("Please fill in the Exercise Name and Duration.")
                return

            workout_data = {
                "date": date.strftime("%Y-%m-%d"),
                "exercise_name": exercise_name,
                "sets": sets,
                "reps": reps,
                "weight": weight,
                "duration_minutes": duration_minutes,
                "intensity": intensity
            }

            try:
                response = requests.post(
                    f"{api_url}/workouts/?user_id={st.session_state.user_id}",
                    json=workout_data
                )
                
                if response.status_code == 201:
                    st.success(f"💪 Workout '{exercise_name}' successfully logged!")
                else:
                    st.error("Failed to log workout.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the backend API. Please check the server status.")