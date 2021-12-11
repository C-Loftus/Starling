import pyaudio
import wave
import struct
import math
from numpy.core.fromnumeric import mean
import sounddevice as sd
import threading
from threading import Thread
import numpy as np
from numpy_ringbuffer import RingBuffer




# create some sort of buffer for always recording then passing
# in the buffer audio recording
class env:
   curr_vol = RingBuffer(capacity=5, dtype=np.float)
   init_duration = 2000 #in milliseconds
   ambient = 0.0
   frames=[]
   
def record_one_phrase():
   # print(f'{env.ambient=}')    

   currentlyRecording = False
   stop_event = threading.Event()
   buffer_stop_event = threading.Event()
   
   
   
   bt = Thread(target=record_finish, args=[buffer_stop_event])
   # need to spawn a thread for this and kill it when valid to start.
   
   while(1):
      if not bt.is_alive:
         env.frames = []
         bt.start()

      set_vol(initialize=False, duration=10)

      if valid_to_start() and not currentlyRecording:
         if bt.is_alive():
            bt.join()
         t = Thread(target=record_finish, args=[stop_event])
         
         # spawn thread 
         print("starting recording thread")
         t.start()
         currentlyRecording = True
      elif valid_to_stop() and currentlyRecording:
         # send signal to stop
         print("stopping recording thread")
         stop_event.set()
         currentlyRecording = False
         return

def valid_to_start(hyperparamVolume = 1):
   return (get_vol() > (env.ambient + hyperparamVolume))       
def valid_to_stop(hyperparamVolume = 0.1):
   return (get_vol() < env.ambient + hyperparamVolume)

def set_vol(initialize=False, duration=env.init_duration):
   stream = sd.InputStream(callback=_audio_callback)
   with stream:
      sd.sleep(duration)  
   if initialize:      
      env.ambient = get_vol()

def get_vol():
   return mean(env.curr_vol)

def _audio_callback(indata, frames, time, status):
   volume_norm = np.linalg.norm(indata) * 10
   env.curr_vol.append(volume_norm)




def record_finish(event):
   # the file name output you want to record into
   filename = "Assets/recorded.wav"
   # set the chunk size of 1024 samples
   chunk = 1024
   # sample format
   FORMAT = pyaudio.paInt16
   # mono, change to 2 if you want stereo
   channels = 1
   # 44100 samples per second
   sample_rate = 44100
   record_seconds = 5
   # initialize PyAudio object
   p = pyaudio.PyAudio()
   
   # open stream object as input & output
   stream = p.open(format=FORMAT,
                   channels=channels,
                   rate=sample_rate,
                   input=True,
                   output=True,
                   frames_per_buffer=chunk)
   frames = env.frames
   for i in range(int(44100 / chunk * record_seconds)):
      if event.is_set():
            break
      # if signal: break else
      data = stream.read(chunk)
      # print(decibel(rms(data)))
      # if you want to hear your voice while recording
      # stream.write(data)
      frames.append(data)

    # stop and close stream
   stream.stop_stream()
   stream.close()
   # terminate pyaudio object
   p.terminate()
   # save audio file
   # open the file in 'write bytes' mode
   wf = wave.open(filename, "wb")
   # set the channels
   wf.setnchannels(channels)
   # set the sample format
   wf.setsampwidth(p.get_sample_size(FORMAT))
   # set the sample rate
   wf.setframerate(sample_rate)
   # write the frames as bytes
   wf.writeframes(b"".join(frames))
   # close the file
   wf.close()
   print("finished recording")       


def record_intermed():
   # set the chunk size of 1024 samples
   chunk = 1024
   # sample format
   FORMAT = pyaudio.paInt16
   # mono, change to 2 if you want stereo
   channels = 1
   # 44100 samples per second
   sample_rate = 44100
   record_seconds = .5
   # initialize PyAudio object
   p = pyaudio.PyAudio()
   
   # open stream object as input & output
   stream = p.open(format=FORMAT,
                   channels=channels,
                   rate=sample_rate,
                   input=True,
                   output=True,
                   frames_per_buffer=chunk)
   frames = []    
   
   for i in range(int(44100 / chunk * record_seconds)):
        # if signal: break else
        data = stream.read(chunk)
        # print(decibel(rms(data)))
        # if you want to hear your voice while recording
        # stream.write(data)
        frames.append(data)
   stream.stop_stream()
   stream.close()
   # terminate pyaudio object
   p.terminate()

   env.frames = frames

if __name__== "__main__":
   set_vol(initialize=True)
   print(get_vol())
   record_one_phrase()


def record(event):
    # the file name output you want to record into
    filename = "Assets/recorded.wav"
    # set the chunk size of 1024 samples
    chunk = 1024
    # sample format
    FORMAT = pyaudio.paInt16
    # mono, change to 2 if you want stereo
    channels = 1
    # 44100 samples per second
    sample_rate = 44100
    record_seconds = 5
    # initialize PyAudio object
    p = pyaudio.PyAudio()
    
    # open stream object as input & output
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []

    for i in range(int(44100 / chunk * record_seconds)):
        if event.is_set():
            break
        # if signal: break else
        data = stream.read(chunk)
        # print(decibel(rms(data)))
        # if you want to hear your voice while recording
        # stream.write(data)
        frames.append(data)

    # stop and close stream
    stream.stop_stream()
    stream.close()
    # terminate pyaudio object
    p.terminate()
    # save audio file
    # open the file in 'write bytes' mode
    wf = wave.open(filename, "wb")
    # set the channels
    wf.setnchannels(channels)
    # set the sample format
    wf.setsampwidth(p.get_sample_size(FORMAT))
    # set the sample rate
    wf.setframerate(sample_rate)
    # write the frames as bytes
    wf.writeframes(b"".join(frames))
    # close the file
    wf.close()
    print("finished recording")