import streamlit as st
from utils.utils import background_image_style, load_library
from bigquery import add_user, authenticate_user, get_library

# Read API url from secrets
API_URL = st.secrets['API_URL']

# Set page configuration
st.set_page_config(
    layout= "wide",
    initial_sidebar_state= "auto"
)

# Add style from css file
with open('www/style.css') as css:
    st.markdown(f"<style>{css.read()}<style>", unsafe_allow_html= True)

# Add background image
#st.markdown(background_image_style(st.secrets['BACKGROUND_IMG']), unsafe_allow_html=True)

# Define pages
search = st.Page(
    page= "views/search.py",
    title= "Search",
    #icon= "🔍"
    icon= ":material/search:",
)

library = st.Page(
    page= "views/mylibrary.py",
    title= "Library",
    #icon= "📚"
    icon= ":material/book_2:",
)

upload = st.Page(
    page= "views/upload.py",
    title= "Upload",
    #icon= "📸",
    icon= ":material/photo_camera:"
)

discover = st.Page(
    page= "views/discover.py",
    title= "Explore",
    #icon= "🧭",
    icon= ":material/explore:",
    default= True
)

about = st.Page(
    page= "views/about.py",
    title= "About",
    #icon= "🎓"
    icon= ":material/school:"
)

# Create navigation structure
pg = st.navigation(pages = [discover, library, search, upload, about])
pg.run()

# User session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Display Login/Sign Up Page
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu, label_visibility= 'collapsed')

    if choice == "Login":
        # Input for user and password
        username = st.sidebar.text_input("Username", placeholder= "Username", label_visibility= 'collapsed')
        password = st.sidebar.text_input("Password", type="password", placeholder= "Password", label_visibility= 'collapsed')

        # Authenticate is user and password are correct
        if st.sidebar.button("Login", key= "login"):
            with st.spinner():
                if authenticate_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.sidebar.success(f"Welcome {username}")
                    st.session_state['library'] = get_library(st.session_state.username) # Load library of the user
                    st.rerun() # Rerun page
                else:
                    st.sidebar.error("Invalid Username/Password")

    elif choice == "Sign Up":
        # Input for user and password
        new_user = st.sidebar.text_input("Create a new account", placeholder= "Username", max_chars= 12)
        new_password = st.sidebar.text_input("Password", type="password", placeholder= "Password", max_chars= 20, label_visibility= 'collapsed')

        if st.sidebar.button("Sign Up"):
            add_user(new_user, new_password)
            st.sidebar.success("Account created successfully! Please login.")
else:
    st.sidebar.write(f"Welcome **:green[{st.session_state.username}]**!")
    if st.sidebar.button("Log out"):
        st.session_state.clear()
        st.rerun()
