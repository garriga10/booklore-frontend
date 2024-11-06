import streamlit as st
from booklore.utils.utils import background_image_style

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
    icon= "🔍",
    default= True
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
    icon= "🧭"
)

about = st.Page(
    page= "views/about.py",
    title= "About",
    icon= "🎓"
)

pg = st.navigation(pages = [discover, library, search, upload, about])

pg.run()
