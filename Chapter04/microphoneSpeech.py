import curses
from threading import Thread

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from StreamSpeechService import initSpeechText, recognizeUsingWebsocket, StreamSpeechControl, MyRecognizeCallback
from TextSpeechService import initTextSpeech, textSpeech

try:
    from Queue import Queue, Full
except ImportError:
    from queue import Queue, Full



# Prep speech output
textSpeechSession  = initTextSpeech()
voice = 'en-US_AllisonVoice'

# Create a control object
SPEECH_CONTROL = StreamSpeechControl()

# Prepare a thread to recognize the input from the microphone input
recognize_thread = Thread(target=recognizeUsingWebsocket, args=(SPEECH_CONTROL,))
recognize_thread.start()

# Create a terminal window for presenting the stream processing results, and initialize that in
# the control object
termWindow = curses.initscr()
SPEECH_CONTROL.MYCALLBACK.setWindow(termWindow)


# Iterate until done
while True:

    if termWindow != None:
        termWindow.erase()
        termWindow.addstr(1, 1, "Say something and Watson will attempt to recognize it. Say 'Quit' to end.")
        termWindow.refresh()
    else:
        print("Say something and Watson will attempt to recognize it. Say 'Quit' to end.")
    
    # Get instances of the needed microphone stream
    microphoneStream = SPEECH_CONTROL.initAudio()
    
    # Wait for the speech service to transcribe input from the user
    while not SPEECH_CONTROL.MYCALLBACK.isTextTranscribed():
        pass

    # Process the transcribed input
    transcript = SPEECH_CONTROL.MYCALLBACK.getTranscription(True)

    # Turn off the microphone while the transcribed text is being processed
    SPEECH_CONTROL.terminateAudio(microphoneStream)

    # Figure out the confidence of the resulting text
    confidence = int(round(100*transcript[0].get("confidence")))
    text = transcript[0].get("transcript")

    # Test for whether the user said 'quit' to determine when to terminate the program
    if text.startswith("quit"):
        break
    
    # And then produce different feedback responses based on the relative confidence of the service.
    if confidence > 90:
        response = "<express-as type=\"GoodNews\"> You said, </express-as> \" {} \".".format(text)
    elif confidence > 70:
        response = "I'm sure you said, {}".format(text)
    elif confidence > 50:
        response = "<express-as type=\"Uncertainty\">I think you said, \" {} \". </express-as>".format(text)
    else:
        response = "<express-as type=\"Apology\">I really wasn't able to understand that well. What I heard was, \"{}\". But what did you really mean to say? </express-as>".format(text)

    # Presenting the results through the Text-to-Speech service
    textSpeech(text=response, voice=voice, session=textSpeechSession)

# Clean up the terminal window and give your good-byes
if termWindow != None:
    curses.endwin()
textSpeech("Good-bye.", voice=voice, session=textSpeechSession)
print("Good-bye for now.")

# Flush the queue
SPEECH_CONTROL.endQueue()

# Shut down the input to the SpeechSocket
SPEECH_CONTROL.AUDIO.terminate()
SPEECH_CONTROL.AUDIO_SOURCE.completed_recording()
