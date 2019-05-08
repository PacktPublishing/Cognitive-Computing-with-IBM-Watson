import pyaudio
import wave

# Set the standard Chunk-size constant
CHUNK = 1024

# Open the wave file containing the audio stream you want played
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
while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

# Upon completion, stop and close the audio stream,
# and terminate the Audio service
stream.stop_stream()
stream.close()
p.terminate()
