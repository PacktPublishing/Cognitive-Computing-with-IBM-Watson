from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread, current_thread
import pyaudio

from TextSpeechService import *


try:
    from Queue import Queue, Full
except ImportError:
    from queue import Queue, Full

# Variables for recording the speech
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 60
QUEUE = None

# create a connection to the Speech service
def initSpeechText():
    return SpeechToTextV1(
            iam_apikey='f6nEkrdAJdvluiBI74xhnlQ134HcHFxxrL21Krii_0Gg',
            url='https://stream.watsonplatform.net/speech-to-text/api')


# this function will serve as the main routine for a parallel thread.  it will initiate
# the Watson Speech recognize service and pass in the AudioSource that was created previously
# in the speechControl object
def recognizeUsingWebsocket(speechControl):
    speechControl.SPEECHSERVICE.recognize_using_websocket(
            audio=speechControl.AUDIO_SOURCE,
            content_type='audio/l16;rate='+str(RATE)+';channels='+str(CHANNELS),
            recognize_callback=speechControl.MYCALLBACK,
            interim_results=True,
            model='en-US_BroadbandModel',
            inactivity_timeout=RECORD_SECONDS,
            keywords=['transfer', 'dollars', 'checking', 'savings'],
            keywords_threshold=0.5,
            max_alternatives=3)
    print("Done recognition")
    speechControl.SESSION_ENDED = True


# define callback for pyaudio to store the recording in queue
def pyaudio_callback(in_data, frame_count, time_info, status):
    global QUEUE
    try:
        QUEUE.put(in_data)
    except Full:
        pass # discard
    return (None, pyaudio.paContinue)


# this is the streamControl helper object for initializing PyAudio, and creating a Queue object on
# which to communicate the microphone voice stream to the speech service.
class StreamSpeechControl:
 
    AUDIO = None
    AUDIO_SOURCE = None
    MYCALLBACK = None
    SPEECHSERVICE = None
    KEYBOARD_INPUT = None
    SESSION_ENDED = False

    def __init__(self):
        global QUEUE
        QUEUE = self.createQueue()
        self.AUDIO = pyaudio.PyAudio()
        self.AUDIO_SOURCE = AudioSource(QUEUE, is_recording=True, is_buffer=True)
        self.MYCALLBACK = MyRecognizeCallback()
        self.SPEECHSERVICE = initSpeechText()


    def createQueue(self):
        # Note: It will discard if the websocket client can't consumme fast enough
        # So, increase the max size as per your choice
        BUF_MAX_SIZE = CHUNK * 10
        return Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))
    
    def endQueue(self):
        global QUEUE
        QUEUE.task_done()
    
    def initAudio(self):
        audioStream = self.AUDIO.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=pyaudio_callback,
                start=False)
        audioStream.start_stream()
        return audioStream
    
    def terminateAudio(self, stream):
        stream.stop_stream()
        stream.close()


# define callback for the speech to text service
class MyRecognizeCallback(RecognizeCallback):
    
    IS_TEXT_TRANSCRIBED = False
    HYPOTHESIS_TEXT = " "
    TRANSCRIBED_TEXT = " "
    WINDOW = None
    
    def __init__(self):
        RecognizeCallback.__init__(self)
    
    def on_connected(self):
        # print('Connection was successful')
        pass

    def on_hypothesis(self, hypothesis):
        self.HYPOTHESIS_TEXT = hypothesis
        if self.WINDOW != None:
            self.WINDOW.addstr(3, 1, "Hypothesis: {}".format(hypothesis))
            self.WINDOW.refresh()
        else:
            # print("Hypothesis: {}".format(hypothesis))
            pass

    def on_transcription(self, transcript):
        confidence = transcript[0].get("confidence")
        text = transcript[0].get("transcript")
        self.TRANSCRIBED_TEXT = transcript
        self.IS_TEXT_TRANSCRIBED = True
        if self.WINDOW != None:
            self.WINDOW.addstr(5, 1, "Watson has " + str(round(float(confidence*100),1)) + "% confidence you said: " + text)
            self.WINDOW.refresh()
        else:
            # print("Watson has " + str(round(float(confidence*100),1)) + "% confidence you said: " + text)
            pass

    def on_error(self, error):
        print('Error received: {}'.format(error))
    
 
    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        # print('Service is listening')
        pass
    
    def on_data(self, data):
        self.result = data
    
    def on_close(self):
        # print('Connection closed')
        pass
    
    def isTextTranscribed(self):
        return self.IS_TEXT_TRANSCRIBED

    def getTranscription(self, reset=True):
        text = self.TRANSCRIBED_TEXT
        if reset:
            self.TRANSCRIBED_TEXT = " "
            self.IS_TEXT_TRANSCRIBED = False
        return text

    def setWindow(self, window):
        self.WINDOW = window
