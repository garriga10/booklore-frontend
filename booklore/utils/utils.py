import requests
import streamlit as st
import base64
from bigquery import save_book

# Function to fecth list of books from a user query
def fetch_api_books(query, url):
    params = {
        "input_title": query
    }
    response = requests.get(url, params= params)
    if response.status_code == 200:
        return response.json().get("possible matches", [])
    else:
        st.error("Error fetching data from API.")
        return []

# Function to fetch details of a specific book by its ID
def fetch_api_book_suggest(query, url):
    params = {
        "bookid": query
    }
    response = requests.get(url, params= params)
    if response.status_code == 200:
        return response.json().get("suggestions", [])
    else:
        st.error("Error fetching data from API.")
        return []

# Function to add books to the library
def add_to_library(book_id, placeholder):
    # Check if the book is already in the library
    if book_id not in st.session_state.library:
        #st.session_state.library.append(book_id)
        save_book(st.session_state.username, book_id)
        del st.session_state['library']
        placeholder.success("Book added to your library!")
    else:
        placeholder.warning("This book is already in your library.")


@st.cache_data
def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

def background_image_style(path):
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
