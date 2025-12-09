import streamlit as st
import requests

# NOTE: Ensure your FastAPI backend is running at this URL (e.g., using uvicorn)
API_URL = "http://127.0.0.1:8000"

st.title("🏋️ Fitness Tracker")

# --- Function to fetch all users ---
def get_users():
    """Fetches a list of all users from the backend API."""
    try:
        # Assuming your API has an endpoint like GET /users that returns a list of user dictionaries
        response = requests.get(f"{API_URL}/users")
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        
        # Handle cases where the API is running but returns an empty list or an error
        st.warning(f"API returned status code {response.status_code}. Check backend response.")
        return []
        
    except requests.exceptions.ConnectionError:
        st.error(f"⚠️ Cannot connect to API at {API_URL}. Ensure the backend service is running.")
        return []

# -----------------------------------

menu = st.sidebar.selectbox("Menu", ["Add User", "Calculate BMI"])

if menu == "Add User":
    st.subheader("Register User")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    height = st.number_input("Height (m)", min_value=0.1, format="%.2f")
    weight = st.number_input("Weight (kg)", min_value=1.0, format="%.1f")

    if st.button("Save"):
        try:
            response = requests.post(f"{API_URL}/users", json={
                "name": name, "age": age, "height": height, "weight": weight
            })
            
            if response.status_code == 200:
                st.success(f"User saved successfully: {response.json().get('message', 'No specific message returned.')}")
            else:
                st.error(f"Error saving user (Status {response.status_code}): {response.json().get('detail', 'Unknown error')}")
                
        except requests.exceptions.ConnectionError:
            st.error(f"⚠️ Cannot connect to API at {API_URL}.")

# -------------------------------------------------------------------------------------------------

elif menu == "Calculate BMI":
    st.subheader("Check BMI")
    
    # 1. Fetch user data at the start
    users_data = get_users() 

    if users_data:
        # Create a dictionary to map the visible option string to the actual user_id
        # Example: { "Alice (ID: 1)": 1, "Bob (ID: 2)": 2 }
        user_options = {
            f"{user['name']} (ID: {user['user_id']})": user['user_id'] 
            for user in users_data if 'name' in user and 'user_id' in user
        }

        # 2. Use a select box for a better user experience
        selected_option = st.selectbox("Select User", list(user_options.keys()))
        
        # Get the actual ID from the selected name string
        user_id = user_options[selected_option]

        if st.button("Calculate BMI"):
            try:
                # 3. Use the correct GET method for calculation/retrieval
                # NOTE: You must update your FastAPI endpoint to handle this GET path
                response = requests.get(f"{API_URL}/users/{user_id}/bmi")

                if response.status_code == 200:
                    bmi_data = response.json()
                    st.success(f"BMI: **{bmi_data['bmi']:.2f}**")
                    st.info(f"Category: **{bmi_data['category']}**")
                elif response.status_code == 404:
                    st.error(f"Error: User with ID {user_id} not found.")
                else:
                    st.error(f"An error occurred (Status {response.status_code}): {response.json().get('error', 'Unknown error')}")
            
            except requests.exceptions.ConnectionError:
                st.error(f"⚠️ Cannot connect to API at {API_URL}.")
    else:
        st.warning("No users available or failed to connect to the API. Please ensure the backend is running and users have been added.")