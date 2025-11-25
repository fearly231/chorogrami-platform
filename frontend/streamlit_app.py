import streamlit as st

pages = {
    "Home": [
        st.Page("pages/home.py", title="Home", icon=":material/home:"),
    ],
    "User": [
        st.Page(
            "pages/user.py",
            title="User",
            icon=":material/person:",
        ),
    ],
}

navigation = st.navigation(pages, position="top")
navigation.run()
