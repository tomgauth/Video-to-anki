import streamlit as st
from services.youtube_embed import embed_video

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "YouTube Embed"])


embed_video()  # Example video with start and end times