# services/srt_parser.py
import re

def parse_srt(srt_content):
    """
    Parses the content of an .srt file and extracts the subtitle text with timestamps.
    :param srt_content: The raw content of the .srt file as a string.
    :return: A list of dictionaries containing 'text', 'start_time', and 'end_time' for each subtitle.
    """
    # Split the content by new lines
    lines = srt_content.splitlines()

    # Initialize variables to collect parsed subtitles
    subtitles = []
    subtitle_text = ""
    start_time = ""
    end_time = ""

    # Regular expression to match timestamps
    timestamp_pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2}),\d{3} --> (\d{2}):(\d{2}):(\d{2}),\d{3}')

    for line in lines:
        match = timestamp_pattern.match(line)
        if match:
            # Extract start and end times in seconds
            start_time = int(match.group(1)) * 3600 + int(match.group(2)) * 60 + int(match.group(3))
            end_time = int(match.group(4)) * 3600 + int(match.group(5)) * 60 + int(match.group(6))
        elif not line.strip():  # Skip empty lines
            if subtitle_text:  # If we have collected text, add it to subtitles
                subtitles.append({
                    'text': subtitle_text.strip(),
                    'start_time': start_time,
                    'end_time': end_time
                })
                subtitle_text = ""
        else:  # If the line is not a timestamp, add it to the current subtitle
            subtitle_text += " " + line.strip()

    # Catch any remaining text after the loop
    if subtitle_text:
        subtitles.append({
            'text': subtitle_text.strip(),
            'start_time': start_time,
            'end_time': end_time
        })

    return subtitles