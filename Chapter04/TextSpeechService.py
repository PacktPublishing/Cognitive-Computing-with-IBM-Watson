import json
from ibm_watson import TextToSpeechV1
import pyaudio
import wave
import sys


def initTextSpeech():
    return TextToSpeechV1(
            iam_apikey='THPYijj30qodXeAl4UnT4bIDyKSZzmrtnBXWve1tg9kX',
            url='https://stream.watsonplatform.net/text-to-speech/api')


def textSpeech(text='Hello', voice='en-US_AllisonVoice', session=initTextSpeech()):
    
    # Synthesize the expressed text in the indicated voice
    audio_file=open('glad_to_be_here.wav', 'wb')
    audio_file.write(
            session.synthesize(
                    text,
                    accept='audio/wav',
                    voice=voice).get_result().content)
    audio_file.close()
                                        
    # Stream the resulting synthesis to the system speakers
    wf = wave.open('glad_to_be_here.wav', 'rb')
    CHUNK = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)
    data = wf.readframes(CHUNK)
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
