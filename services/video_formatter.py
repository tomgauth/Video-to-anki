# services/video_formatter.py
import ffmpeg
import os

def lower_video_quality(input_video, output_video):
    """
    Lowers the quality of the video to 360p max without changing the codec.
    :param input_video: The path to the original video file.
    :param output_video: The path where the lower-quality video will be saved.
    """
    try:
        (
            ffmpeg
            .input(input_video)
            .output(
                output_video,
                vcodec='libx264',  # Standard video codec
                acodec='aac',  # Standard audio codec
                video_bitrate="1M",  # Set the video bitrate to reduce quality
                vf="scale='-2:360'",  # Scale video to 360p max, preserving aspect ratio
                y=None  # Automatically overwrite the output file
            )
            .overwrite_output()  # Ensures it overwrites existing files
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode('utf8')}")
        raise e

def split_video_by_subtitles(input_video, subtitles, output_dir):
    """
    Splits the video into smaller clips based on the start and end times of the subtitles.
    :param input_video: The path to the original video file.
    :param subtitles: A list of subtitle dictionaries with 'start_time', 'end_time', and 'text'.
    :param output_dir: The directory where the video clips will be saved.
    :return: A list of paths to the created video clips.
    """
    clip_paths = []
    for i, subtitle in enumerate(subtitles):
        start_time = subtitle['start_time']
        end_time = subtitle['end_time']
        clip_filename = os.path.join(output_dir, f"clip_{i}.mp4")
        ffmpeg.input(input_video, ss=start_time, to=end_time).output(clip_filename).run()
        clip_paths.append(clip_filename)
    return clip_paths


def split_video_by_subtitles(input_video, subtitles, output_dir, st_progress, total_clips):
    """
    Splits the video into smaller clips based on the start and end times of the subtitles.
    Displays a progress bar in Streamlit during the process.
    :param input_video: The path to the original video file.
    :param subtitles: A list of subtitle dictionaries with 'start_time', 'end_time', and 'text'.
    :param output_dir: The directory where the video clips will be saved.
    :param st_progress: The Streamlit progress bar instance.
    :param total_clips: The total number of clips to be created.
    :return: A list of paths to the created video clips.
    """
    clip_paths = []

    for i, subtitle in enumerate(subtitles):
        start_time = subtitle['start_time']
        end_time = subtitle['end_time']
        clip_filename = os.path.join(output_dir, f"clip_{i}.mp4")
        
        # Split the video without changing the quality
        ffmpeg.input(input_video, ss=start_time, to=end_time).output(clip_filename).run()

        clip_paths.append(clip_filename)

        # Update progress bar based on the number of clips created
        progress = (i + 1) / total_clips  # Calculate progress as a float
        st_progress.progress(progress)  # Update progress in Streamlit
    
    return clip_paths