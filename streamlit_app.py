import streamlit as st
import components.authenticate as authenticate
import requests
import os

MILYNNUSCOGNITO_ST_SUPERUSER_USERNAME = os.environ.get('MILYNNUSCOGNITO_ST_SUPERUSER_USERNAME')
if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def check_subscription():
    st.session_state.clicked = True

st.set_page_config(
    page_title="Login",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)

    SavvyAI enables you to use AI on any websites, pdf file, Youtube videos and more...
"""
)

# Check authentication when user lands on the home page.
#authenticate.set_st_state_vars()

with st.sidebar:
    st.title("SavvyAI with AWS Cognito")
    st.info("This application is secured by AWS Cognito")
    authenticate.button_login()
    
    # Add login/logout buttons
    

    st.write(st.session_state)

