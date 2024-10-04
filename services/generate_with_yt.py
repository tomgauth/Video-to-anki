import random
import genanki


def generate_deck_with_youtube(subtitles, video_id):
    """
    Generates an Anki deck with embedded YouTube video clips for each subtitle.
    :param subtitles: A list of subtitle dictionaries with 'start_time', 'end_time', and 'text'.
    :param video_id: The YouTube video ID.
    :return: A genanki Deck object.
    """

    model_id = random.randrange(1 << 30, 1 << 31)
    deck_id = random.randrange(1 << 30, 1 << 31)

    my_model = genanki.Model(
        model_id,
        'YouTube Video Subtitle Model',
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

    my_deck = genanki.Deck(deck_id, 'YouTube Video Flashcard Deck')

    for subtitle in subtitles:
        start_time = subtitle['start_time']
        end_time = subtitle['end_time']
        subtitle_text = subtitle['text']

        # Generate the YouTube embed iframe using your own app logic
        recto_content = f'''
        <iframe width="100%" height="500"
            src="https://video2anki.streamlit.app/video/{video_id}/{start_time}/{end_time}"
            title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
        </iframe>
        '''

        # Subtitle text goes on the back of the card
        verso_content = subtitle_text

        note = genanki.Note(
            model=my_model,
            fields=[recto_content, verso_content]
        )
        my_deck.add_note(note)

    return my_deck