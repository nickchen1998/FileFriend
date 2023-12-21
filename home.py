import streamlit as st
from env_settings import EnvSettings
from utils import get_authenticator

env_settings = EnvSettings()
authenticator = get_authenticator()
name, authentication_status, username = authenticator.login(
    'Login', 'main')

if authentication_status:
    with st.sidebar:
        st.write(f'Welcome *{name}*')
        authenticator.logout('Logout', 'main')

    st.title('Some content')
    with st.expander("See explanation"):
        st.write(
            """
        The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random."""
        )
        st.image("https://static.streamlit.io/examples/dice.jpg")

    with st.expander("See explanation"):
        st.write(
            """
        The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random."""
        )
        st.image("https://static.streamlit.io/examples/dice.jpg")

elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
