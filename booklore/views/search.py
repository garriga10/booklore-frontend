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

    # Function to clean variable in session_state
    def clear_search():
        st.session_state['search_text_input'] = ''

    # Initialize session state for the input field if it doesn't exist
    if 'search_text_input' not in st.session_state:
        st.session_state['search_text_input'] = ''

    # Create 2 columns in the page
    pcols = st.columns([5, 2])

    with pcols[0]:
        # Set title and subtitle of the page
        st.title("Search")
        # Set subtitle
        st.markdown("*Find books and add them to your library*")
        # Create a search form
        with st.container(border= True):
            # Create 4 columns to have all the inputs in one line
            qcol1, qcol2, qcol3 = st.columns([5, 1, 1])

            with qcol1:
                # Text input for title search
                text = f"Enter text to search"
                query = st.text_input(
                    text,
                    placeholder= text,
                    label_visibility= 'collapsed',
                    key= 'search_text_input'
                )
            with qcol2:
                search_button = st.button("", key= "search", type= 'primary', icon= ":material/search:", use_container_width= True)
            with qcol3:
                clear_button = st.button("", key= "clear", on_click= clear_search, type= 'primary', icon= ":material/delete:", use_container_width = True)

            result = st.empty()

    if search_button and query:
        with st.spinner("Finding books..."):
            search_results = fetch_api_books(query, url = f"{API_URL}/recommendations")
        if isinstance(search_results, list):
            result.info(f"**{len(search_results)}** books found. Which one are you looking for?")
            st.write("")
            for book in search_results:
                book_id = book.get('bookId', '')
                title = book.get("title", "No Title")

                with st.container(border= True):
                    gcol1, gcol2 = st.columns([10, 1])

                    with gcol1:
                        st.subheader(title)

                    with gcol2:
                        add_button = st.button(
                            "",
                            key= book_id,
                            on_click= add_to_library,
                            args= (book_id,),
                            type= 'primary',
                            help= "Add this book to your library",
                            icon= ":material/add:",
                            use_container_width= True
                        )
        else:
            result.warning("No books found.")
