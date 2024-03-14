import streamlit as st
import components.authenticate as authenticate
import requests

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
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

# Check authentication when user lands on the home page.
authenticate.set_st_state_vars()

if st.session_state["authenticated"]:
    user_info = authenticate.get_user_info(st.session_state['access_token'])

with st.sidebar:
    st.title("SavvyAI on Cognito")
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


                if st.button("Chat 💬 with PDF 💬") and st_user['username'] == SAVVYAI_ST_SUPERUSER_USERNAME:
                    if "chat_history" in st.session_state:
                        del st.session_state.chat_history
                    st.switch_page("pages/pdf_chat.py")
            
            st.divider()

            with st.expander("Reset Password"):
                st.write("To be handled")
    else:
        authenticate.button_login()

        # using Boto3
if st.session_state['authenticated']:
    if user_info['custom.status'] == 'paid' :
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
    

"""
        
        userinfo_url = "https://cognito-idp.ap-southeast-1.amazonaws.com"
        headers = {
            #"Content-Type": "application/json;charset=UTF-8",
            "Content-Type": "application/x-amz-json-1.1",
            "Authorization": f"Bearer {st.session_state['access_token']}",
            "X-Amz-Target": "AWSCognitoIdentityProviderService.UpdateUserAttributes",
        }
        payload = {
            "AccessToken" : st.session_state['access_token'],
            "UserAttributes" : [
                {
                    'Name': 'custom:status',
                    'Value': 'active'
                },
            ]
        }

        userinfo_response = requests.post(userinfo_url, json=payload, headers=headers)


        st.write(userinfo_response.text)"""
        


    
