import streamlit as st
import requests

from utils.utils import fetch_api_books, add_to_library

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.write("")
    st.write("")
    st.warning("Log in to access")
else:
    # Read API url from secrets
    API_URL = st.secrets['API_URL']

    # Initialize session state for library if not already done
    if 'library' not in st.session_state:
        st.session_state['library'] = []

    # Initialize session state for the input field if it doesn't exist
    if 'upload_text_input' not in st.session_state:
        st.session_state['upload_text_input'] = ''

    pcols = st.columns([5, 1])

    with pcols[0]:
        # Set title and subtitle of the page
        st.title("Upload")
        st.markdown("## Upload a picture of the cover of a book")
        with st.container(border= True):
            picture = st.camera_input(
                "Take a picture",
                label_visibility= 'collapsed'
            )
            search_button = st.button(
                "Search",
                type= 'primary',
                use_container_width = True
            )
