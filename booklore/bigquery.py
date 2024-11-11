import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

#credentials = service_account.Credentials.from_service_account_file('booklore-439916-16e0f6452e82.json')
#client = bigquery.Client(credentials=credentials)

# Access the credentials from Streamlit secrets
credentials_dict = st.secrets["gcp_service_account"]

# Use from_service_account_info to load credentials from the dictionary
credentials = service_account.Credentials.from_service_account_info(credentials_dict)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# Helper functions
def add_user(username, password):
    query = f"""
    INSERT INTO `booklore_db.users` (user_login, user_password)
    VALUES ('{username}', '{password}')
    """
    client.query(query).result()

def authenticate_user(username, password):
    query = f"""
    SELECT COUNT(*) AS count
    FROM `booklore_db.users`
    WHERE user_login = '{username}' AND user_password = '{password}'
    """
    result = client.query(query).result()
    return list(result)[0].count > 0

def save_book(username, book):
    query = f"""
    INSERT INTO `booklore_db.libraries` (user_login, book_id)
    VALUES ('{username}', '{book}')
    """
    client.query(query).result()

def remove_book(username, book):
    query = f"""
    DELETE FROM `booklore_db.libraries`
    WHERE user_login = '{username}' AND book_id = '{book}'
    """
    client.query(query).result()

def get_books(username):
    query = f"""
    SELECT book_id
    FROM `booklore_db.libraries`
    WHERE user_login = '{username}'
    """
    result = client.query(query).result()
    return [row['book_id'] for row in result]
