# SRT to Anki Flashcards with Video Clips

This project allows users to upload a video file and an SRT subtitle file to automatically generate Anki flashcards with embedded video clips for each subtitle line.

## Features

- Upload `.mp4` video files and `.srt` subtitle files.
- Automatically split the video into clips based on the timestamps in the subtitle file.
- Generate Anki flashcards with embedded video clips on one side and the subtitle text on the other side.
- A progress bar that shows the progress of video splitting.
- Compress video files to 360p for faster processing.

## Installation

To run this project locally, make sure you have Python installed. Clone this repository and install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
