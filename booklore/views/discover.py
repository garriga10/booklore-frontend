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

pcols = st.columns([5, 1])

with pcols[0]:
    # Set title and subtitle of the page
    st.title("Explore")
    st.markdown("*Find book recommendations inspired by your chosen title*")
    with st.form('test'):
        # Create two columns reduce space of search bar
        qcol1, qcol2, qcol3 = st.columns([5, 1, 1])

        with qcol1:
            # Text input for title search
            text = f"Enter title to search"
            query = st.text_input(
                text,
                placeholder= text,
                label_visibility= 'collapsed',
                key= 'dis_text_input'
            )

        # Place buttons in separate columns
        with qcol2:
            # Button to searach button. On click removes any book id already selected
            search_button = st.form_submit_button("Search", type= 'primary')
        with qcol3:
            clear_button = st.form_submit_button("Clear", on_click= clear_search, type= 'primary')

        result = st.empty()

if search_button and query:
    if st.session_state.sel_book_id is None:
        with st.spinner("Finding books..."):
            search_results = fetch_api_books(query, url = f"{API_URL}/recommendations")
        if isinstance(search_results, list):
            result.info(f"**{len(search_results)}** books found")
            st.write("")
            for book in search_results:
                book_id = book.get('bookId', '') # Get book id
                title = book.get("title", "No Title") # Get title

                gcol1, gcol2 = st.columns([4, 1])

                with gcol1:
                    st.subheader(title)
                    #st.write(book_id)

                with gcol2:
                    sel_button = st.button(
                        "Get recommendations",
                        key= book_id,
                        on_click= sel_book,
                        args= (book_id,),
                        type= 'primary'
                    )
                    #if sel_book:
                        #st.session_state.sel_book_id = book_id
                        #book_details = fetch_api_book_suggest(query)
                st.write("---")
        else:
            result.warning("No books found.")

# If a book has been selected, fetch and display its details
if st.session_state.sel_book_id:
    book_details = fetch_api_book_suggest(st.session_state.sel_book_id, url = f"{API_URL}/model-suggest")
    if book_details:
        # Convert suggestions list to a DataFrame
        #df = pd.DataFrame(book_details)
        st.write("---")
        #st.write(df)
        # Loop over each suggestion and display its information
        for index, book in enumerate(book_details, start= 1):
            scol1, scol2 = st.columns([6, 1])

            with scol1:
                st.caption(f"*Distance: {book['distance']:.4f}*")
                st.subheader(f"{book['title']}")
                st.write(f"{book['author']}")
            #with st.expander("View detail"):
            #st.write(f"Publisher: {book['publisher']}")
            #st.write(f"Rating: {book['rating']}")
            with scol2:
                st.write("")
                st.metric("Rating", f"{book['rating']}")
            #st.write("---")
            st.divider()
