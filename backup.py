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