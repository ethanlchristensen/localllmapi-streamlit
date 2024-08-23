import os
import json

import streamlit as st

st.info("Welcome! Please use the sidebar to login!", icon=":material/arrow_back:")

with st.sidebar:
    with st.form(key="login", clear_on_submit=True):
        username = st.text_input(label="Username", type="default")
        password = st.text_input(label="Password", type="password")
        submit = st.form_submit_button()
    
    if submit:
        users = json.loads(open(os.path.join(os.getcwd(), "db", "users.json"), "r").read())
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.display_name = username
            st.rerun()
        else:
            st.error(body="Incorrect username or password provided. Please try again!", icon=":material/error:")