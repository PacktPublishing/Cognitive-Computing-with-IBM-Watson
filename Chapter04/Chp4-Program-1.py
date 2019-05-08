import json
from ibm_watson import TextToSpeechV1

def textSpeech():
    
    # Create session with the Text to Speech service
    text_to_speech = TextToSpeechV1(
            iam_apikey='THPYijj30qodXeAl4UnT4bIDyKSZzmrtnBXWve1tg9kX',
            url='https://stream.watsonplatform.net/text-to-speech/api'
        )
        
    # Use Text to Speech to create mp3 file
    with open('glad_to_be_here.mp3', 'wb') as audio_file:
        audio_file.write(
                ext_to_speech.synthesize(
                    'I\'m so glad you\'re here with me today.',
                    'audio/mp3',
                    'en-US_MichaelVoice'
                ).get_result().content)

