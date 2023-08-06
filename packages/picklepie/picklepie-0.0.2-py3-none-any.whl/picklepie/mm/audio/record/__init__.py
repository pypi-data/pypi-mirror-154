import sounddevice as __sd
from scipy.io.wavfile import write as __write
import speech_recognition as __sr
import os as __os

def wav (a_file,b_second=3) :
    # record only in a specific seconds
    loc_fs = 44100  # Sample rate
    b_second = 3  # Duration of recording
    myrecording = __sd.rec(int(b_second*loc_fs),samplerate=loc_fs,channels=2)
    __sd.wait()  # Wait until recording is finished
    __write(a_file,loc_fs,myrecording)  # Save as WAV file 

def mic (a_file) : # mp3
    # record until break of sound
    loc_input = __sr.Recognizer()
    with __sr.Microphone() as loc_source :
        loc_audio = loc_input.listen(loc_source)
    loc_file = open(a_file, 'wb')
    loc_file.write(loc_audio.get_wav_data(convert_rate=16000))

