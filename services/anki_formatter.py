from services.video_formatter import lower_video_quality, split_video_by_subtitles
import genanki
import random
import os

def generate_deck_with_clips(subtitles, video_file_path, st_progress, total_clips):
    """
    Generates an Anki deck with embedded video clips for each subtitle.
    Updates the progress bar based on the number of clips created.
    :param subtitles: A list of subtitle dictionaries with 'start_time', 'end_time', and 'text'.
    :param video_file_path: The path to the uploaded video file.
    :param st_progress: Streamlit progress bar instance.
    :param total_clips: Total number of subtitle entries (clips to be created).
    :return: A genanki Deck object.
    """
    
    # Step 1: Lower video quality to 360p
    low_quality_video = "low_quality_video.mp4"
    lower_video_quality(video_file_path, low_quality_video)

    # Step 2: Split the video into clips based on the subtitle timestamps and update progress
    output_dir = "video_clips"
    os.makedirs(output_dir, exist_ok=True)
    clip_paths = split_video_by_subtitles(low_quality_video, subtitles, output_dir, st_progress, total_clips)

    # Step 3: Create Anki flashcards using the clips
    model_id = random.randrange(1 << 30, 1 << 31)
    deck_id = random.randrange(1 << 30, 1 << 31)

    my_model = genanki.Model(
        model_id,
        'Subtitle Video Clip Model',
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

    my_deck = genanki.Deck(deck_id, 'Video Clip Flashcard Deck')

    for i, subtitle in enumerate(subtitles):
        recto_content = f'<video controls><source src="{clip_paths[i]}" type="video/mp4"></video>'
        verso_content = subtitle['text']

        note = genanki.Note(
            model=my_model,
            fields=[recto_content, verso_content]
        )
        my_deck.add_note(note)

    return my_deck
