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


class audio_environment:
   # curr_vol = collections.deque(maxlen=100)

   curr_vol = RingBuffer(capacity=100, dtype=np.float)


   init_duration = 2000 #in milliseconds
   ambient = 0

   def record_one_phrase():
      currentlyRecording = False
      stop_event = threading.Event()
      t = Thread(target=record, args=[stop_event])

      while(1):

         audio_environment.set_vol(initialize=False, duration=10)

         if audio_environment.valid_to_start(currentlyRecording):
            # spawn thread 
            print("starting recording thread")
            t.start()
            currentlyRecording = True
         elif audio_environment.valid_to_stop(currentlyRecording):
            # send signal to stop
            print("stopping recording thread")
            stop_event.set()
            currentlyRecording = False
            return

   def valid_to_start(inProgress, hyperparamVolume = 1):
      return (inProgress == False and \
         (audio_environment.get_vol() > (audio_environment.ambient + hyperparamVolume)))       
   def valid_to_stop(inProgress, hyperparamVolume = 1):
          return (inProgress and \
         (audio_environment.get_vol() < audio_environment.ambient))  

   def set_vol(initialize=False, duration=init_duration):
      stream = sd.InputStream(callback=audio_environment._audio_callback)
      with stream:
         sd.sleep(duration)  
      if initialize:           
         audio_environment.ambient = audio_environment.get_vol()         

   def get_vol():
      return mean(audio_environment.curr_vol)

   def _audio_callback(indata, frames, time, status):
      volume_norm = np.linalg.norm(indata) * 10
      audio_environment.curr_vol.append(volume_norm)

if __name__== "__main__":
   audio_environment.set_vol(initialize=True)
   print(audio_environment.get_vol())
   audio_environment.record_one_phrase()



def rms( data ):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
        sum_squares += n*n
    return math.sqrt( sum_squares / count )


def decibel(rms):
    return 20 * math.log(rms, 10)

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

if __name__ == "__main__":
    record()