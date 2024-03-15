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
    page_title="Home",
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
authenticate.set_st_state_vars()

if st.session_state["authenticated"]:
    user_info = authenticate.get_user_info(st.session_state['access_token'])

with st.sidebar:
    st.title("SavvyAI with AWS Cognito")
    st.info("This application is secured by AWS Cognito")
    st.write(st.session_state)
    # Add login/logout buttons
    if st.session_state["authenticated"]:
        authenticate.button_logout()

        st.write('Welcome')

        st.write("SavvyAI enables you to use AI on any websites, pdf file, Youtube videos and more....")


        if user_info['custom:status'] == 'paid' :

            if st.button("Chat with Website 🌎"):
                if "chat_history" in st.session_state:
                    del st.session_state.chat_history
                st.switch_page("pages/web.py")

            if st.button("Ask your PDF 💬"):
                st.switch_page("pages/pdf.py")


            if st.button("Chat 💬 with PDF 💬") and user_info['username'] == MILYNNUSCOGNITO_ST_SUPERUSER_USERNAME:
                if "chat_history" in st.session_state:
                    del st.session_state.chat_history
                st.switch_page("pages/pdf_chat.py")
            
    else:
        authenticate.button_login()

        # using Boto3
if st.session_state['authenticated']:
    if user_info['custom:status'] == 'paid' :
        with st.expander(f"Your are a {user_info['custom:subscription_plan']} subscriber"):
            st.write("Howdy there")
    else:

        with st.expander("Please subscribe to use the SavvyAI services"):
        

            col1, col2, col3 = st.columns(3)
            
            if "subscribe" not in st.session_state:
                with col1: 
                    if st.button('Basic'):
                        st.session_state.subscribe = "savvyai_basic"
                with col2: 
                    if st.button('Standard'):
                        st.session_state.subscribe = "savvyai_standard"
                with col3: 
                    if st.button('Premium'):
                        st.session_state.subscribe = "savvyai_premium"

                st.info("Once you have selected your subscription plan, a customised checkout button will be presented for you make payment via Stripe.")
            else:
                res = requests.post("https://hook.eu2.make.com/02mc5fyg32kxqf1xl4ejs0v1lv9nb9fs", json={"name" : st_user['name'], "email" : st_user['email'], "subscription_name" : st.session_state.subscribe, "path" : "subscription", "return" : "url"})
                if res.status_code == 200:
                    checkout_url = res.json()['url']
                    st.link_button(":blue[Checkout]", f"{checkout_url}")
                    st.info("Once payment is made, you profile will be updated and, automatically, enabled for the services subscribed under the plan or you can clicked on the button below to check the status")

                    st.button('Check subscription status', on_click=check_subscription)
                    if st.session_state.clicked:
                        # The message and nested widget will remain on the page
                        st.write('Checking ....')
                        st.session_state.clicked = False
                        st.rerun()
else:
    st.write("Please login")
    


        


    