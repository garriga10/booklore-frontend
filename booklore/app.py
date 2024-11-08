import streamlit as st
from utils.utils import background_image_style
from bigquery import add_user, authenticate_user

st.set_page_config(
    layout= "wide",
    initial_sidebar_state= "auto"
)

with open('www/style.css') as css:
    st.markdown(f"<style>{css.read()}<style>", unsafe_allow_html= True)

st.markdown(background_image_style(st.secrets['BACKGROUND_IMG']), unsafe_allow_html=True)

search = st.Page(
    page= "views/search.py",
    title= "Search",
    icon= "🔍"
)

library = st.Page(
    page= "views/mylibrary.py",
    title= "Library",
    icon= "📚"
)

upload = st.Page(
    page= "views/upload.py",
    title= "Upload",
    icon= "📸"
)

discover = st.Page(
    page= "views/discover.py",
    title= "Explore",
    icon= "🧭",
    default= True
)

about = st.Page(
    page= "views/about.py",
    title= "About",
    icon= "🎓"
)

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
        username = st.sidebar.text_input("Username", placeholder= "Username", label_visibility= 'collapsed')
        password = st.sidebar.text_input("Password", type="password", placeholder= "Password", label_visibility= 'collapsed')

        if st.sidebar.button("Login"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.sidebar.success(f"Welcome {username}")
                st.rerun()
            else:
                st.sidebar.error("Invalid Username/Password")

    elif choice == "Sign Up":
        new_user = st.sidebar.text_input("Create a new account", placeholder= "Username")
        new_password = st.sidebar.text_input("Password", type="password", placeholder= "Password", label_visibility= 'collapsed')

        if st.sidebar.button("Sign Up"):
            add_user(new_user, new_password)
            st.sidebar.success("Account created successfully! Please login.")
else:
    st.sidebar.write(f"Welcome **{st.session_state.username}**!")
    if st.sidebar.button("Log out"):
        st.session_state.clear()
        st.rerun()
