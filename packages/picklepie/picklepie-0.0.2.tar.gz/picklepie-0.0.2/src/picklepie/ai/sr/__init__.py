# https://gtts.readthedocs.io/en/latest/module.html
# https://www.programcreek.com/python/example/107719/speech_recognition.Microphone

import speech_recognition as __sr
import sounddevice as __sd
import soundfile as __sf
from scipy.io import wavfile as __wav

from gtts import gTTS as __gtts
from playsound import playsound as __ps
import random as __rnd
import os as __os

import time

import picklepie as __pp

# https://realpython.com/playing-and-recording-sound-python/
# https://realpython.com/python-speech-recognition/
# http://www.voiptroubleshooter.com/open_speech/index.html
# https://python-sounddevice.readthedocs.io/en/0.4.1/usage.html
# https://python-sounddevice.readthedocs.io/en/0.3.14/examples.html

# free time
# https://github.com/spatialaudio/python-sounddevice/blob/master/examples/rec_unlimited.py
# https://pythonprogramming.altervista.org/recording-your-voice-with-sounddevice/

def text (a_audio_file='',b_reduce_noise=False,b_reduce_noise_duration=0.5,b_show_all=False) :
    loc_recognizer = __sr.Recognizer()
    loc_audio_file = __sr.AudioFile(a_audio_file)
    with loc_audio_file as loc_source :
        if (b_reduce_noise == True) : # to reduce noise if needed
            loc_recognizer.adjust_for_ambient_noise(loc_source,duration=b_reduce_noise_duration)
        loc_audio = loc_recognizer.record(loc_source)
    return loc_recognizer.recognize_google(loc_audio,show_all=b_show_all)

def play (a_audio_file='',b_wait=True) :
    loc_data,loc_fs = __sf.read(a_audio_file,dtype='float32')
    __sd.play(loc_data,loc_fs)
    if (b_wait) :
        loc_status = __sd.wait()  # Wait until file is done playing
        
def record (a_save_to='') :        
    loc_fs = 44100  # Sample rate
    loc_duration = 3  # Duration of recording in seconds
    loc_my_recording = __sd.rec(int(loc_duration*loc_fs),samplerate=loc_fs,channels=2)
    __sd.wait()  # Wait until recording is finished
    __wav.write(a_save_to,loc_fs,loc_my_recording)  # Save as WAV file         
    
def speak (a_text='',b_lang='en') :
    #creating a super random named file
    r1 = __rnd.randint(1,10000000)
    r2 = __rnd.randint(1,10000000)
    randfile = str(r2)+"randomtext"+str(r1) +".mp3"
    tts = __gtts(text=a_text,lang=b_lang,slow=False)
    tts.save(randfile)
    __ps(randfile)
    __os.remove(randfile)   
    
def test_loop () :
    while True :
        try :
            print('$')
            time.sleep(2)    
        except (KeyboardInterrupt, SystemExit):
            print('\nkeyboardinterrupt caught (again)')
            print('\n...Program Stopped Manually!')
            raise