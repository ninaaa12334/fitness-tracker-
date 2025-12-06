import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🏋️ Fitness Tracker")

menu = st.sidebar.selectbox("Menu", ["Add User", "Calculate BMI"])

if menu == "Add User":
    st.subheader("Register User")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    height = st.number_input("Height (m)", min_value=0.1, format="%.2f")
    weight = st.number_input("Weight (kg)", min_value=1.0, format="%.1f")

    if st.button("Save"):
        response = requests.post(f"{API_URL}/users", json={
            "name": name, "age": age, "height": height, "weight": weight
        })
        st.success(response.json()["message"])

elif menu == "Calculate BMI":
    st.subheader("Check BMI")
    user_id = st.number_input("User ID", min_value=1)
    if st.button("Calculate"):
        response = requests.post(f"{API_URL}/bmi/{user_id}")
        if "error" in response.json():
            st.error(response.json()["error"])
        else:
            st.write(f"BMI: {response.json()['bmi']}")
            st.write(f"Category: {response.json()['category']}")
