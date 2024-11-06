import streamlit as st
import requests

# Example usage in my_library.py to display saved books in the library
st.title("My Library")

if 'library' in st.session_state and st.session_state.library:
    book_ids = st.session_state.library
    st.markdown("*Books in your library*")

    for book in st.session_state.library:
        st.subheader(book)
        st.write("---")
else:
    st.write("*Your library is empty...*")
