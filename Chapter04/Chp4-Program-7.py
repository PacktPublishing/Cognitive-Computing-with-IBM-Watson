import json
from ibm_watson import SpeechToTextV1

# Create a connection to the speech to text service
speech_to_text = SpeechToTextV1(
        iam_apikey='f6nEkrdAJdvluiBI74xhnlQ134HcHFxxrL21Krii_0Gg',
        url='https://stream.watsonplatform.net/speech-to-text/api')

# Identify the source audio file
file = 'Transfer request.mp3'

# Open the file in the local folder
with open(join(dirname(__file__), './.', file), 'rb') as audio_file:
    
    # Invoke the recognize() function on the speech service
    speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,                   # The file containing the audio
            content_type='audio/mp3',           # The codec for the file
            timestamps=True,                    # Whether to return timing markers
            word_alternatives_threshold=0.9,    # The minimum interpretation confidence
        ).get_result()

# Print out the resulting JSON produced from the translation
print(json.dumps(speech_recognition_results, indent=2))
