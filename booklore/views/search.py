import streamlit as st
import requests

from utils.utils import fetch_api_books, add_to_library

# Read API url from secrets
API_URL = st.secrets['API_URL']

# Function to clean variable in session_state
def clear_search():
    st.session_state.library = None
    st.session_state['search_text_input'] = ''

# Initialize session state for library if not already done
if 'library' not in st.session_state:
    st.session_state['library'] = []

# Initialize session state for the input field if it doesn't exist
if 'search_text_input' not in st.session_state:
    st.session_state['search_text_input'] = ''

# Create 2 columns in the page
pcols = st.columns([5, 1])

with pcols[0]:
    # Set title and subtitle of the page
    st.title("Search")
    # Set subtitle
    st.markdown("*Find books and add them to your library*")
    # Create a search form
    with st.form('searchbar'):
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
            search_button = st.form_submit_button("Search", type= 'primary')
        with qcol3:
            clear_button = st.form_submit_button("Clear", on_click= clear_search, type= 'primary')

        result = st.empty()

if search_button and query:
    with st.spinner("Finding books..."):
        search_results = fetch_api_books(query, url = f"{API_URL}/recommendations")
    if isinstance(search_results, list):
        result.info(f"**{len(search_results)}** books found. Which one are you looking for?")
        st.write("")
        for book in search_results:
            book_id = book.get('bookId', '') # Get book id
            title = book.get("title", "No Title") # Get title

            gcol1, gcol2 = st.columns([4, 1])

            with gcol1:
                st.subheader(title)

            with gcol2:
                add_button = st.button(
                    "Add to My Library",
                    key=book_id,
                    on_click= add_to_library,
                    args=(book_id,),
                    type= 'primary'
                )
            st.write("---")
    else:
        result.warning("No books found.")
