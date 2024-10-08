import streamlit as st
import os
import genanki
from services.srt_parser import parse_srt
from services.anki_formatter import generate_deck_with_clips
from services.generate_with_yt import generate_deck_with_youtube
import shutil


# Function to delete existing video files and videos in the video_clips folder
def delete_existing_videos():
    files_to_delete = ['uploaded_video.mp4', 'low_quality_video.mp4']
    
    # Delete the main video files
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            # st.write(f"Deleted {file}")
        else:
            # st.write(f"{file} does not exist")
            pass
    
    # Delete all files in the video_clips folder
    video_clips_folder = 'video_clips'
    if os.path.exists(video_clips_folder):
        # Use shutil to delete the entire folder with its content, and then recreate it
        shutil.rmtree(video_clips_folder)
        os.makedirs(video_clips_folder)
        st.write(f"Deleted all files in {video_clips_folder} and recreated the folder.")
    else:
        st.write(f"{video_clips_folder} folder does not exist.")

# Function to count the number of clips created in video_clips folder
def count_clips_created(total_clips, st_progress):
    video_clips_folder = 'video_clips'
    clip_count = len(os.listdir(video_clips_folder))
    
    # Update the progress bar based on the number of clips created
    progress = clip_count / total_clips
    st_progress.progress(progress)


# Streamlit app frontend
st.title("SRT to Anki Flashcards with Video Clips")

if st.button("Delete cache"):
    delete_existing_videos()

# Streamlit app frontend
st.title("YouTube to Anki Flashcards with Subtitles")

# Input for YouTube URL
youtube_url = st.text_input("Enter YouTube Video URL")

# File uploader for the .srt file
uploaded_srt = st.file_uploader("Upload your .srt file", type=["srt"])

if youtube_url and uploaded_srt:
    # Extract video ID from the YouTube URL
    video_id = youtube_url.split('v=')[-1]
    
    srt_content = uploaded_srt.read().decode("utf-8")
    
    # Parse the .srt file to extract subtitles and timestamps
    subtitles = parse_srt(srt_content)
    
    # Button to process the video and generate flashcards
    if st.button("Generate Anki Flashcards"):
        # Generate Anki deck with YouTube embeds
        my_deck = generate_deck_with_youtube(subtitles, video_id)

        # Save the Anki deck to a file
        deck_file = 'output.apkg'
        genanki.Package(my_deck).write_to_file(deck_file)

        # Provide a download button for the .apkg file
        with open(deck_file, "rb") as f:
            st.download_button(label="Download Anki Deck", data=f, file_name="flashcards.apkg", mime="application/octet-stream")
else:
    st.info("Please enter a YouTube URL and upload a subtitle file.")