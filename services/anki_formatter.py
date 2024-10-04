from services.video_formatter import lower_video_quality, split_video_by_subtitles, convert_video_to_gif, extract_audio
import genanki
import random
import os


def generate_deck_with_clips(subtitles, video_file_path, st_progress, total_clips):
    """
    Generates an Anki deck with embedded GIFs and audio for each subtitle.
    :param subtitles: A list of subtitle dictionaries with 'start_time', 'end_time', and 'text'.
    :param video_file_path: The path to the uploaded video file.
    :param st_progress: Streamlit progress bar instance.
    :param total_clips: Total number of subtitle entries (clips to be created).
    :return: A genanki Deck object.
    """
    output_dir = "video_clips"
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Split the video into clips based on the subtitle timestamps
    clip_paths = split_video_by_subtitles(video_file_path, subtitles, output_dir, st_progress, total_clips)

    model_id = random.randrange(1 << 30, 1 << 31)
    deck_id = random.randrange(1 << 30, 1 << 31)

    my_model = genanki.Model(
        model_id,
        'GIF and Audio Model',
        fields=[
            {'name': 'Recto'},
            {'name': 'Verso'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Recto}}',
                'afmt': '{{Verso}}',
            },
        ])

    my_deck = genanki.Deck(deck_id, 'GIF and Audio Flashcard Deck')

    media_files = []  # List to store all media file paths

    for i, subtitle in enumerate(subtitles):
        gif_filename = f"clip_{i}.gif"
        audio_filename = f"clip_{i}.aac"  # Using AAC as an example

        # Convert video to GIF and extract audio
        convert_video_to_gif(clip_paths[i], os.path.join(output_dir, gif_filename))
        extract_audio(clip_paths[i], os.path.join(output_dir, audio_filename))

        # Add the media file paths to the media_files list
        media_files.append(os.path.join(output_dir, gif_filename))
        media_files.append(os.path.join(output_dir, audio_filename))

        # Use the [sound] tag for Anki audio
        recto_content = f'<img src="{gif_filename}" alt="Video Clip"><br>[sound:{audio_filename}]'
        verso_content = subtitle['text']

        note = genanki.Note(
            model=my_model,
            fields=[recto_content, verso_content]
        )
        my_deck.add_note(note)

    # Package the deck and include media files
    package = genanki.Package(my_deck)
    package.media_files = media_files  # Add media files to the package
    package.write_to_file('output.apkg')

    return my_deck