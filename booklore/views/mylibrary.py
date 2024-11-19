import streamlit as st
import requests
import pandas as pd
import math
import matplotlib.pyplot as plt

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.write("")
    st.write("")
    st.warning("Log in to access")
else:
    # Set title
    st.title("Library")

    # Create 3 tabs
    tab1, tab2, tab3 = st.tabs(["Read", "Whishlist", "Metrics"])

    # Tab 1: Read
    with tab1:
        # Check if library is loaded
        if st.session_state.library:

            # Filter by books readed
            books_readed = pd.DataFrame(st.session_state.library)
            books_readed = books_readed[books_readed['book_type'] == 'Read']

            # Iterate over books to fetch details
            for index, book in books_readed.iterrows():
                with st.container(border= True):
                    scol1, scol2 = st.columns([6, 1])
                    with scol1:
                        st.caption(f"{book.get('book_date', '-')}")
                        st.write("⭐" * 5)
                        st.subheader(f"{book.get('book_title', 'Not found')}")
                        st.markdown(f"## {book.get('book_author', 'Not found')}")
                    with scol2:
                        book_cover_img = book.get("book_cover_img", None)
                        # Check if book_cover_img is not None and is a valid image URL or path
                        if book_cover_img:
                            st.image(book_cover_img, width=100)
                        else:
                            # Optional: Display a placeholder image
                            st.image("https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg", width=100)
                    with st.expander("Comments", icon= ":material/description:"):
                        st.write(f"{book.get('book_comment', 'No comments')}")
            st.write("")
        else:
            st.info("*Your library is empty...*")

    # Tab 2: Whishlist
    with tab2:
        # Check if library is loaded
        if st.session_state.library:

            # Filter by books readed
            books_whishlist = pd.DataFrame(st.session_state.library)
            books_whishlist = books_whishlist[books_whishlist['book_type'] == 'I want to read it']

            # Check if there are book on the whishlist
            if not books_whishlist.empty:

                # Iterate over books to fetch details
                for index, book in books_whishlist.iterrows():
                    with st.container(border= True):
                        scol1, scol2 = st.columns([6, 1])
                        with scol1:
                            global_rating = book.get('book_global_rating', 0)
                            if global_rating is not None and not math.isnan(global_rating):
                                star = "⭐" * int(round(global_rating))
                            else:
                                star = ""
                            st.caption(f"Rating: {book.get('book_global_rating', '-')}")
                            st.write(f"{star}")
                            st.subheader(f"{book.get('book_title', 'Not found')}")
                            st.markdown(f"## {book.get('book_author', 'Not found')}")
                        with scol2:
                            book_cover_img = book.get("book_cover_img", None)
                            # Check if book_cover_img is not None and is a valid image URL or path
                            if book_cover_img:
                                st.image(book_cover_img, width=100)
                            else:
                                # Optional: Display a placeholder image
                                st.image("https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg", width=100)
                        with st.expander("Description", icon= ":material/description:"):
                            st.write(f"{book.get('book_description', 'No description')}")
                st.write("")
            else:
                st.info("Your whishlist is empty")
        else:
            st.info("*Your whishlist is empty...*")

    # Tab 3: Metrics
    with tab3:
        if st.session_state.library:
            st.write("⚠️")
            st.metric("Library", len(st.session_state.library))

        else:
            st.info("*Your library is empty...*")
