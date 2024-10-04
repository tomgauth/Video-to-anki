import streamlit as st
from services.youtube_embed import embed_video

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "YouTube Embed"])


embed_video('zhWDdy_5v2w', 30, 33)  # Example video with start and end times