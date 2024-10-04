import streamlit as st
import re

def get_youtube_id(youtube_url):
    """
    Extract the video ID from a YouTube URL.
    Supports standard URLs (e.g., https://www.youtube.com/watch?v=VIDEO_ID)
    and shortened URLs (e.g., https://youtu.be/VIDEO_ID).
    """
    # Check for standard YouTube URL format (e.g., https://www.youtube.com/watch?v=VIDEO_ID)
    if "v=" in youtube_url:
        return youtube_url.split("v=")[1].split("&")[0]  # Handle query parameters after the video ID

    # Check for shortened YouTube URL format (e.g., https://youtu.be/VIDEO_ID)
    elif "youtu.be/" in youtube_url:
        return youtube_url.split("youtu.be/")[1].split("?")[0]  # Handle any query parameters

    else:
        return None  # Return None if the URL doesn't match the expected formats



# Page for embedding YouTube videos with start and end times
def embed_video():
    # Get query parameters from URL
    query_params = st.experimental_get_query_params()

    # Parse the video ID, start time, and end time from the query parameters
    video_id = query_params.get('video', [None])[0]
    start_time = query_params.get('start', [0])[0]  # Default to 0 if no start time
    end_time = query_params.get('end', [0])[0]      # Default to 0 if no end time

    # Ensure the video ID exists
    if video_id:
        st.title(f"Embedding YouTube Video: {video_id}")

        # Generate the YouTube embed iframe
        iframe_code = f'''
        <iframe width="100%" height="500"
            src="https://www.youtube.com/embed/{video_id}?start={start_time}&end={end_time}"
            title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
        </iframe>
        '''

        # Display the iframe
        st.markdown(iframe_code, unsafe_allow_html=True)
    else:
        st.error("Invalid or missing video ID.")

embed_video()

