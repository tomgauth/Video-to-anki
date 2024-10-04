import streamlit as st

def get_youtube_id(youtube_url):
    """
    Extract the video ID from a YouTube URL.
    Example URL: https://www.youtube.com/watch?v=VIDEO_ID
    """
    if "v=" in youtube_url:
        return youtube_url.split("v=")[1]
    else:
        return None

# Streamlit app for embedding YouTube videos
st.title("Custom YouTube Video Embedder")

# Input for YouTube video URL
youtube_url = st.text_input("Enter YouTube Video URL")

# Input for start and end times
start_time = st.number_input("Start time (in seconds)", min_value=0, value=0)
end_time = st.number_input("End time (in seconds)", min_value=0, value=0)

if youtube_url:
    video_id = get_youtube_id(youtube_url)
    
    if video_id:
        # If video ID is valid, create an iframe with start and end times
        if end_time > 0:
            iframe_code = f'''
            <iframe width="100%" height="500"
                src="https://www.youtube.com/embed/{video_id}?start={start_time}&end={end_time}"
                frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
            '''
        else:
            # If no end time is provided, omit it from the embed code
            iframe_code = f'''
            <iframe width="100%" height="500"
                src="https://www.youtube.com/embed/{video_id}?start={start_time}"
                frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
            '''
        
        # Display the iframe with the video
        st.markdown(iframe_code, unsafe_allow_html=True)
    else:
        st.warning("Invalid YouTube URL.")