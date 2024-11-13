import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

# Access the credentials from Streamlit secrets
credentials_dict = st.secrets["gcp_service_account"]

# Use from_service_account_info to load credentials from the dictionary
credentials = service_account.Credentials.from_service_account_info(credentials_dict)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# Add user
def add_user(username, password):
    """
    Add a new user to the data base by adding a new row with username and password

    Parameters:
    - username: user login
    - password: password

    Don't return anything
    """

    query = f"""
    INSERT INTO `booklore_db.users` (user_login, user_password)
    VALUES (@username, @password)
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("password", "STRING", password)
        ]
    )

    try:
        client.query(query, job_config= job_config).result()
    except Exception as e:
        print(f"An error occurred: {e}")

def authenticate_user(username, password):
    """
    Authentificate a user login comparing the input with the data base info

    Parameters:
    - username: user login
    - password: password

    Return True or False
    """

    query = f"""
    SELECT COUNT(*) AS count
    FROM `booklore_db.users`
    WHERE user_login = @username AND user_password = @password
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("password", "STRING", password)
        ]
    )

    try:
        result = client.query(query, job_config= job_config).result()
        count = list(result)[0].count
        return count > 0
    except Exception as e:
        print(f"An error occurred: {e}")

def save_book(username, book_id, book_type, book_date=None, book_comment=None):
    """
    Add a new book to the data base

    Parameters:
    - username: user login
    - book_id: id of the book
    - book_type: Read / I want to read it
    - book_date: read date
    - book_comment: comment of the book

    Don't return anything
    """

    query = """
    INSERT INTO `booklore_db.libraries` (user_login, book_id, book_type, book_date, book_comment)
    VALUES (@username, @book_id, @book_type, @book_date, @book_comment)
    """

    # Configure query parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("book_id", "STRING", book_id),
            bigquery.ScalarQueryParameter("book_type", "STRING", book_type),
            bigquery.ScalarQueryParameter("book_date", "DATE", book_date if book_type == 'Read' else None),
            bigquery.ScalarQueryParameter("book_comment", "STRING", book_comment if book_type == 'Read' else None),
        ]
    )

    try:
        # Execute the query with the configured parameters
        client.query(query, job_config= job_config).result()
    except Exception as e:
        print(f"An error occurred: {e}")

def remove_book(username, book_id):
    """
    Remove a book from the database

    Parameters:
    - username: user login
    - book_id: book_id

    Don't return anything
    """

    query = f"""
    DELETE FROM `booklore_db.libraries`
    WHERE user_login = @username AND book_id = @book_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("username", "STRING", book_id)
        ]
    )

    try:
        result = client.query(query, job_config= job_config).result()
        return [dict(row) for row in result]
    except Exception as e:
        print(f"An error occurred: {e}")


def get_library(username):
    """
    Get all the libraries table from the input user

    Parameters:
    - username: user login

    Dictionary with libraries table
    """

    query = f"""
    SELECT *
    FROM `booklore_db.libraries`
    WHERE user_login = @username
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username)
        ]
    )

    try:
        result = client.query(query, job_config= job_config).result()
        return [dict(row) for row in result]
    except Exception as e:
        print(f"An error occurred: {e}")
