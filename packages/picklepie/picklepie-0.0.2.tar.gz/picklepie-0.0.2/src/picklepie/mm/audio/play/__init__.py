import playsound as __ps
import sounddevice as __sd
import soundfile as __sf

def mp3 (a_file) :
    __ps.playsound(a_file,True)
    
def wav (a_file='',b_wait=True) :
    loc_data,loc_fs = __sf.read(a_file,dtype='float32')
    __sd.play(loc_data,loc_fs)
    if (b_wait) :
        loc_status = __sd.wait()  # Wait until file is done playing
    
