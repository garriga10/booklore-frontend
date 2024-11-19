import streamlit as st
from utils.utils import fetch_api_books, fetch_api_book_suggest

# Read API url from secrets
API_URL = st.secrets['API_URL']

# Function to change variable in session_state
def sel_book(book_id):
    st.session_state.sel_book_id = book_id

# Function to clean variable in session_state
def clear_search():
    st.session_state.sel_book_id = None
    st.session_state['dis_text_input'] = ''

# Initialize session state for the input field if it doesn't exist
if 'dis_text_input' not in st.session_state:
    st.session_state['dis_text_input'] = ''

# Initialize session state variables
if 'sel_book_id' not in st.session_state:
    st.session_state.sel_book_id = None

pcols = st.columns([5, 2])

with pcols[0]:
    # Set title and subtitle of the page
    st.title("Explore")
    st.markdown("## Find book recommendations inspired by your chosen title")

    with st.container(border= True, key= 'prova'):
        # Create two columns reduce space of search bar
        qcol1, qcol2, qcol3= st.columns([5, 1, 1])

        with qcol1:
            # Text input for title search
            text = f"Enter title to search"
            query = st.text_input(
                text,
                placeholder= text,
                label_visibility= 'collapsed',
                key= 'dis_text_input'
            )

        with qcol2:
            # Search button. On click removes any book id already selected
            search_button = st.button(
                "",
                key= "search",
                type= 'primary',
                icon= ":material/search:",
                use_container_width= True
            )
        with qcol3:
            # Clear results
            clear_button = st.button(
                "",
                key= "clear",
                on_click= clear_search,
                type= 'primary',
                icon= ":material/delete:",
                help= "Clear results",
                use_container_width = True
            )

        result = st.empty()

if search_button and query:
    if st.session_state.sel_book_id is None:
        with st.spinner("Finding books..."):
            search_results = fetch_api_books(query, url = f"{API_URL}/recommendations")
        if isinstance(search_results, list):
            result.info(f"**{len(search_results)}** books found that matches your query. Select one to get a your suggested list!")
            st.write("")
            for book in search_results:
                book_id = book.get('bookId', '') # Get book id
                title = book.get("title", "No Title") # Get title

                with st.container(border= True):
                    gcol1, gcol2 = st.columns([10, 1])

                    with gcol1:
                        st.subheader(title)

                    with gcol2:
                        sel_button = st.button(
                            "",
                            key= book_id,
                            on_click= sel_book,
                            args= (book_id,),
                            type= 'primary',
                            icon= ":material/explore:",
                            help= "Get recommendatios for this book",
                            use_container_width= True
                        )
            st.write("")
        else:
            result.warning("No books found.")

# If a book has been selected, fetch and display its details
if st.session_state.sel_book_id:
    book_details = fetch_api_book_suggest(st.session_state.sel_book_id, url = f"{API_URL}/DL_model-suggest")
    if book_details:
        st.write("")
        for index, book in enumerate(book_details, start= 1):
            with st.container(border= True):
                scol1, scol2 = st.columns([6, 1])
                with scol1:
                    star = "⭐" * int(round(book.get('rating', 0)))
                    st.caption(f"Rating: {book.get('rating', '-')}")
                    st.write(f"{star}")
                    st.subheader(f"{book.get('title', 'Not found')}")
                    st.markdown(f"## {book.get('author', 'Not found')}")
                with scol2:
                    st.image(book.get("coverImg", {}), width= 100)
                with st.expander("Description", icon= ":material/description:"):
                    st.write(f"{book.get('description', 'No details')}")
        st.write("")
