with open('glad_to_be_here.mp3', 'wb') as audio_file:
    audio_file.write(
            text_to_speech.synthesize(
                    ‘Doctor! I believe I have Familial Dysautonomia',
                    'audio/mp3',
                    'en-US_MichaelVoice',
                    customization_id
                ).get_result().content)
