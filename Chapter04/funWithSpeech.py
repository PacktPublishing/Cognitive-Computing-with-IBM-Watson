import json
from ibm_watson import TextToSpeechV1
import pyaudio
import wave
import sys

# This program can optionally take 3 command line arguments
# Text = the string (in quotes) of the thing to synthesize
# Voice = the voice in which to speak the text
# Model = the custom model (customization_id) to use in the synthesis

# Set the default chunking size for wave file
CHUNK = 1024

# This function will initialize an instance of the TexttoSpeechV1 object
def initTextSpeech(): return TextToSpeechV1(
        iam_apikey='a3PkovTG8LCKfFzDY7tCIP6sF6VDONX2xrFXmD85KOiQ',
        url='https://stream.watsonplatform.net/text-to-speech/api'
    )


# This function will synthesize the text, and the play it through the speaker
def textSpeech(
        text='Hello',                # The text to synthesize; defaults to "Hello"
        voice='en-US_AllisonVoice',  # The voice to synthesize with
        session=initTextSpeech(),    # The Speech session object
        model=None):                 # The custom model to use, if any
 
    #
    # Synthesize the expressed text in the indicated voice
    #
    
    # Open an intermediate file in which to hold the synthesized form
    audio_file=open('glad_to_be_here.wav', 'wb')
    
    # Write the synthesized voice to the intermediate wave file
    audio_file.write(
            session.synthesize(
                    text,
                    accept='audio/wav',
                    voice=voice,
                    customization=model
                ).get_result().content)
                
    # Close the file
    audio_file.close()

    #
    # Stream the resulting synthesis to the system speakers
    #
    
    # Re-open the file as a wave source file
    wf = wave.open('glad_to_be_here.wav', 'rb')

    # Create an instance of the Audio service
    p = pyaudio.PyAudio()
 
    # Open a stream object to the speaker
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)

    # Get the first chunk of audio from the wave file
    data = wf.readframes(CHUNK)
        
    # Write the first chunk of data to the audio stream, and continue to
    # read the next chunk to the speaker audio stream until all of the data
    # has been read from the wave file.
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)

    # Upon completion, stop and close the audio stream,
    # and terminate the Audio service
    stream.stop_stream()
    stream.close()
    p.terminate()

#
# This is the main body of the program
#

# Check for whether the user supplied a text string to synthesize
if len(sys.argv) > 1:
    this_text=sys.argv[1]
# otherwise create a default string to synthesize
else:
    this_text='I\'m so glad you\'re working with me on this today. Tell me what to say.'

# Check for whether the user supplied a voice to use
if len(sys.argv) > 2:
    this_voice=sys.argv[2]
# otherwise use the Allison Voice
else:
    this_voice='en-US_AllisonVoice'

# Check for whether the user supplied a custom model to use
if len(sys.argv) > 3:
    this_model=sys.argv[3]
# otherwise don't use one
else:
    this_model=None

# Print out what this program will do
print("Say \"" + this_text + "\" in this voice: " + this_voice +
      " with this model: \"" + str(this_model) + "\"")

# Now call the textSpeech() function to synthesize and speak the text
textSpeech(text=this_text, voice=this_voice, model=this_model)

