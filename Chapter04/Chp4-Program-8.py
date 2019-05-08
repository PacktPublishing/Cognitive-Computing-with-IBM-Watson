import pyaudio
import wave

# Set the constants that will be used in this program
FORMAT = pyaudio.paInt16    # The word size to get from the microphone
CHANNELS = 2                # Read the microphone in stereo
RATE = 44100                # Read the microphone at 44Khz
CHUNK = 1024                # Encode the audio in 1KB chunks
RECORD_SECONDS = 5          # Record for a maximum of 5 seconds

# Put the recorded sound in this file
WAVE_OUTPUT_FILENAME = "speechInput.wav"

#
# The getAudio() function will capture audio from the microphone and
# record in the file specified above.
def getAudio():
    
    # Create a PyAudio session object
    audio = pyaudio.PyAudio()
    
    # Open the microphone for recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            frames_per_buffer=CHUNK)
    
    # Indicate to the user they can start talking
    print("recording...")
    
    # Create an vector in which to append chunks of audio
    frames = []
    
    # Continue to read from the microphone and append chunks of audio
    # to the frames vector
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Tell the user the microphone is being turned off
    print("finished recording")

    # Stop the reecording and close the input stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Now write the audio frames vector out to a Wave file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # And return the resulting file
    return WAVE_OUTPUT_FILENAME

#
# This is the main body of the program that prompts the user to say
# something, and then invokes the getAudio() function to record them
# from the microphone.
#
print("Say what you want.")
audioFileName = getAudio()
