import requests
import pandas as pd
import streamlit as st
import base64
from datetime import datetime

from bigquery import save_book, get_library

# Function to fecth list of books from a user query
def fetch_api_books(query, url):
    """
    Fetch a list of possible matches from the API

    Parameters:
    - query: text input from the user
    - url: API main url

    Return a list of dictionaries
    """

    params = {
        "input_title": query
    }
    response = requests.get(url, params= params)
    if response.status_code == 200:
        return response.json().get("possible matches", [])
    else:
        st.error("Error fetching data from API.")
        return []

# Function to fetch list of recomendations
def fetch_api_book_suggest(book_id, url):
    """
    Fetch list of suggested books for specific book_id from the API

    Parameters:
    - book_id: book_id
    - url: API main url

    Return a list of dictionaries with detalied information for each book
    """

    params = {
        "bookid": book_id
    }
    response = requests.get(url, params= params)
    if response.status_code == 200:
        return response.json().get("suggestions", [])
    else:
        st.error("Error fetching data from API.")
        return []

# Function to fetch list of recomendations
def fetch_api_book_detail(book_id, url):
    """
    Fetch details of specific book for specific book_id from the API

    Parameters:
    - query: book_id
    - url: API main url

    Return a dictionaries with detalied information for the book
    """

    params = {
        "bookid": book_id
    }
    response = requests.get(url, params= params)
    if response.status_code == 200:
        return response.json().get("book-info", [])
    else:
        st.error("Error fetching data from API.")
        return []


# Simulate a confirmation dialog using placeholder elements
@st.dialog("Add a book to your library")
def add_to_library(book_id, url):
    """
    Add new book to the library. Checks if the book is already in the list of books.
    If not, it reads all the inputs and save it in the database

    Parameters:
    - book_id: book_id

    Return success or warning
    """

    # Check if the book is already in the library
    if book_id not in [book['book_id'] for book in st.session_state.library]:
        options = ['Read', 'I want to read it']
        book_type = st.radio("Select", options, label_visibility= "collapsed")
        book_date = None
        book_rating = None
        book_comment = None
        if book_type == 'Read':
            book_date = st.date_input("When did you read it?", datetime.today().date())
            book_rating = st.feedback("stars")
            book_comment = st.text_area("Comments")

        confirm_button = st.button("Confirm")
        # Add the book if confirmed
        if confirm_button:
            with st.spinner("Saving book..."):
                # Fetch details info of the book
                book_details = fetch_api_book_detail(book_id, url)[0]

                # Save info the database
                save_book(
                    st.session_state.username,
                    book_id,
                    book_type,
                    book_details['title'],
                    book_details['author'],
                    book_date,
                    book_comment,
                    book_details['rating'],
                    book_details['description'],
                    book_details['coverImg'],
                )
                #st.success("Book added to your library!")
                st.session_state['library'] = get_library(st.session_state.username)
                if book_id in [book['book_id'] for book in st.session_state.library]:
                    st.success("Book added to your library!")
                else:
                    st.warning("Failed to verify book addition.")
    else:
        st.warning("This book is already in your library")


def load_library(username, url):

    mylibrary = []

    books_db = get_library(username)
    for book in books_db:
        book_id = book.get('book_id', '')
        book_details = fetch_api_book_detail(book_id, url)

        if isinstance(book_details, list) and book_details:
            book_info = book_details[0]
            if book_info:
                # Merge API data with DB data
                book_combined = {
                    "title": book_info["title"],
                    "genres": book_info["genres"],
                    "author": book_info["author"],
                    "publisher": book_info["publisher"],
                    "description": book_info["description"],
                    "rating": book_info["rating"],
                    "coverImg": book_info["coverImg"],
                    # Add the fields from the database
                    "book_date": book["book_date"],
                    "book_type": book["book_type"],
                    "book_rating": book["book_rating"],
                    "book_comment": book["book_comment"],
                }
                mylibrary.append(book_combined)

    return mylibrary


@st.cache_data
def load_image(path):
    """
    Load local image

    Parameters:
    - path: path of the image

    Return encoded image
    """

    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

def background_image_style(path):
    """
    Load local image calling load_image function and add the html style

    Parameters:
    - path: path of the image

    Return econded and styled image
    """

    encoded = load_image(path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    '''
    return style
