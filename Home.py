import streamlit as st
import components.authenticate as authenticate
import requests

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
with st.sidebar:
    st.title("SavvyAI on Cognito")
    st.info("This application is secured by AWS Cognito")
    st.write(st.session_state)
    # Add login/logout buttons
    if st.session_state["authenticated"]:
        authenticate.button_logout()
        user_info = authenticate.get_user_info(st.session_state['access_token'])
        st.write("Custom Attributes")
        st.write(user_info['custom:status'])
        st.write(user_info['custom:subscription_plan'])
        # using Boto3
        userinfo_url = "https://milynnus.auth.ap-southeast-1.amazoncognito.com/oauth2/update_user_attributes"
        headers = {
            #"Content-Type": "application/json;charset=UTF-8",
            "Content-Type": "application/x-amz-json-1.1",
            "Authorization": f"Bearer {st.session_state['access_token']}",
        }
        payload = {
            "UserAttributes" : [
                {
                    'Name': 'custom:status',
                    'Value': 'active'
                },
            ]}

        userinfo_response = requests.post(userinfo_url, json=payload, headers=headers)


        st.write(userinfo_response)
        


        if st.button("1_📈_Plotting_Demo"):
            st.switch_page("pages/Plotting_Demo.py")

    else:
        authenticate.button_login()
