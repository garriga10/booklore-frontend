import streamlit as st
import requests
import pandas as pd

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.write("")
    st.write("")
    st.warning("Log in to access")
else:
    st.title("Library ⚠️")

    # Create 3 tabs
    tab1, tab2, tab3 = st.tabs(["Read", "Whishlist", "Metrics"])

    # Tab 1: Read
    with tab1:
        if st.session_state.library:
            st.markdown("*Books in your library*")
            books_readed = pd.DataFrame(st.session_state.library)
            books_readed = books_readed[books_readed['book_type'] == 'Read']
            for index, row in books_readed.iterrows():
                book_id = row.get('book_id', '')
                book_comment = row.get('book_comment', 'No comments')
                st.subheader(book_id)
                st.write(book_comment)
                st.write("---")
        else:
            st.write("*Your library is empty...*")

    # Tab 2: Whishlist
    with tab2:
        if st.session_state.library:
            st.markdown("*Books in your whishlist*")
            books_whishlist = pd.DataFrame(st.session_state.library)
            books_whishlist = books_whishlist[books_whishlist['book_type'] == 'I want to read it']
            for index, row in books_whishlist.iterrows():
                book_id = row.get('book_id', '')
                book_comment = row.get('book_comment', 'No comments')
                st.subheader(book_id)
                st.write(book_comment)
                st.write("---")
        else:
            st.write("*Your library is empty...*")

    # Tab 3: Metrics
    with tab3:
        if st.session_state.library:
            st.metric("Library", len(st.session_state.library))
