import streamlit as st
import components.authenticate as authenticate
import boto3

client = boto3.client('cognito-idp')

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
        client = boto3.client('milynnus-auth-client-name')

        response = client.update_user_attributes(
            UserAttributes=[
                {
                    'Name': 'custom:status',
                    'Value': 'active'
                },
            ],
            AccessToken=st.session_state['access_token'],
    
        )

        if st.button("1_📈_Plotting_Demo"):
            st.switch_page("pages/Plotting_Demo.py")

    else:
        authenticate.button_login()
