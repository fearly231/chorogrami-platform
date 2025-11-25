import streamlit as st
from api.client import APIClient

st.title("📋 Users")
api = APIClient()

try:
    data = api.get("/users/")
    st.write(f"Total users: {data['count']}")
    st.table(data["data"])
except Exception as e:
    st.error(f"Failed to fetch users: {e}")

with st.form("create_user_form"):
    name = st.text_input("Name")
    surname = st.text_input("Surname")
    age = st.number_input("Age")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Create")

    if submitted:
        if not name or not surname or not age or not email or not password:
            st.warning("All fields are required.")
        else:
            payload = {
                "name": name,
                "surname": surname,
                "age": age,
                "email": email,
                "password": password,
            }
            result = api.post("/users/", json=payload)

            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                st.success(f"✅ User '{result['name']}' created successfully!")
                st.json(result)
