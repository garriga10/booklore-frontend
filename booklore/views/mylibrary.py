import streamlit as st
import requests
from bigquery import get_books

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.write("")
    st.write("")
    st.warning("Please, log in to access")
else:
    st.title("Library")

    if 'library' not in st.session_state:
        st.session_state['library'] = get_books(st.session_state.username)

    if st.session_state.library:
        st.markdown("*Books in your library*")
        for book in st.session_state.library:
            st.subheader(book)
            st.write("---")
    else:
        st.write("*Your library is empty...*")
