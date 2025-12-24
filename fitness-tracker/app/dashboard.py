import streamlit as st
import requests
import pandas as pd

def show_dashboard(api_url):
    """The main entry point for the dashboard UI."""
    
    # --- Sidebar Navigation ---
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.username}! 👋")
        menu = st.radio("Navigation", ["Overview", "Log Workout", "Progress Charts", "Settings"])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # --- Dashboard Views ---
    if menu == "Overview":
        render_overview(api_url)
    elif menu == "Log Workout":
        render_workout_form(api_url)
    elif menu == "Progress Charts":
        st.info("Charts feature coming soon!")
    elif menu == "Settings":
        st.write("Account settings and goals.")

def render_overview(api_url):
    st.markdown("## 📊 Fitness Analytics")
    
    # 1. Top Row: Advanced Metrics
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric(label="Active Streak", value="5 Days", delta="🔥 +1")
    with m_col2:
        st.metric(label="Total Workouts", value="12", delta="20%")
    with m_col3:
        st.metric(label="Last Weight", value="72.5 kg", delta="-0.5 kg", delta_color="inverse")
    with m_col4:
        st.metric(label="Hydration", value="85%", delta="Target: 3L")

    st.markdown("---")

    # 2. Main Area: Activity Table
    st.markdown("### 🏃 Recent Activity")
    try:
        response = requests.get(f"{api_url}/workouts/{st.session_state.user_id}")
        if response.status_code == 200:
            workouts = response.json()
            if workouts:
                df = pd.DataFrame(workouts)
                # Cleaning up columns for the user
                df = df.rename(columns={
                    'exercise_name': 'Exercise',
                    'sets': 'Sets',
                    'reps': 'Reps',
                    'weight': 'Weight (kg)',
                    'date': 'Date'
                })
                st.dataframe(df[['Date', 'Exercise', 'Sets', 'Reps', 'Weight (kg)']], 
                             use_container_width=True, hide_index=True)
            else:
                st.info("No workouts found. Time to hit the gym!")
    except Exception as e:
        st.error(f"Could not load activity: {e}")

def render_workout_form(api_url):
    st.markdown("### 🏋️ Log Your Session")
    
    with st.form("workout_entry", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            exercise = st.selectbox("Exercise", ["Bench Press", "Squats", "Deadlift", "Running", "Yoga"])
            sets = st.number_input("Sets", min_value=1, value=3)
        with col2:
            reps = st.number_input("Reps", min_value=1, value=10)
            weight = st.number_input("Weight (kg)", min_value=0.0, value=20.0)
            
        submit = st.form_submit_button("SAVE WORKOUT")
        
        if submit:
            workout_data = {
                "exercise_name": exercise,
                "sets": int(sets),
                "reps": int(reps),
                "weight": float(weight),
                "date": str(pd.Timestamp.now().date())
            }
            # Sending user_id as a query parameter as defined in your FastAPI route
            res = requests.post(f"{api_url}/workouts/?user_id={st.session_state.user_id}", json=workout_data)
            if res.status_code == 201:
                st.toast("Workout Saved!", icon="✅")
                st.balloons()
            else:
                st.error("Failed to save workout.")

def render_calendar_view():
    st.markdown("### 📅 Weekly Activity Tracker")
    
    # Create 7 columns for the days of the week
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = st.columns(7)
    
    # Logic: We check if a workout exists for today
    # (Mock data for now, but ready for your database)
    completed_days = ["Mon", "Wed"] 
    
    for i, day in enumerate(days):
        with cols[i]:
            is_done = day in completed_days
            bg_color = "rgba(0, 255, 136, 0.2)" if is_done else "rgba(255, 255, 255, 0.05)"
            border = "1px solid #00ff88" if is_done else "1px solid rgba(255, 255, 255, 0.1)"
            status_icon = "✅" if is_done else "⭕"
            
            st.markdown(f"""
                <div style="background: {bg_color}; border: {border}; padding: 10px; border-radius: 10px; text-align: center;">
                    <p style="margin: 0; font-size: 0.8em; color: #ccc;">{day}</p>
                    <p style="margin: 5px 0 0 0; font-size: 1.2em;">{status_icon}</p>
                </div>
            """, unsafe_allow_html=True)